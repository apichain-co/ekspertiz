from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from ..database import db
from ..models import Report, Customer, Package, Staff
from datetime import datetime
from ..services.car_service import get_available_colors
from ..services.report_service import (
    create_report, get_or_create_agent, get_or_create_customer,
    get_or_create_vehicle_owner, get_or_create_vehicle
)
from sqlalchemy.exc import IntegrityError
from ..forms.forms import ReportForm

reports = Blueprint('reports', __name__)


@reports.route('/reports')
def report_list():
    page = request.args.get('page', 1, type=int)  # Get the current page, default is 1
    per_page = request.args.get('per_page', 10, type=int)  # Items per page, default is 10
    paginated_reports = Report.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('report/report_list.html', reports=paginated_reports.items, pagination=paginated_reports)



@reports.route('/report/add', methods=['GET', 'POST'])
def add_report():
    form = ReportForm()
    colors = get_available_colors()

    if form.validate_on_submit():
        form_data = form.data

        try:
            # Create or retrieve customer, vehicle owner, and agent
            customer = get_or_create_customer(form_data)
            vehicle_owner = get_or_create_vehicle_owner(form_data)
            agent = get_or_create_agent(form_data['agent_name'])

            # Create the report
            new_report = create_report(form_data, customer.id)

            # Link the vehicle owner and agent to the report
            vehicle_owner.report_id = new_report.id
            agent.report_id = new_report.id

            # Commit changes for vehicle owner and agent
            db.session.commit()

            # Now, check or create vehicle linked to the report
            get_or_create_vehicle(form_data, new_report.id)

            flash('Rapor başarıyla oluşturuldu!', 'success')
            return redirect(url_for('reports.report_list'))

        except IntegrityError as e:
            db.session.rollback()
            flash(f'Tüm değerleri doğru girdiğinize emin olun!', 'error')

        except Exception as e:
            db.session.rollback()
            flash(f'Beklenmedik bir hata oluştu!', 'error')

    # Retrieve data for the form and render the template
    return render_template('reports.html', form=form, colors=colors)




@reports.route('/report/update/<int:report_id>', methods=['GET', 'POST'])
def update_report(report_id):
    report = Report.query.get_or_404(report_id)

    if request.method == 'POST':
        report.vehicle_plate = request.form['vehicle_plate']
        report.chassis_number = request.form['chassis_number']
        report.brand = request.form['brand']
        report.model = request.form['model']
        report.model_year = int(request.form['model_year'])
        report.inspection_date = datetime.strptime(request.form['inspection_date'], '%Y-%m-%d').date()
        report.customer_id = int(request.form['customer_id'])
        report.package_id = int(request.form['package_id'])
        report.created_by = int(request.form['created_by'])
        report.registration_document_seen = bool(request.form['registration_document_seen'] == 'on') # check what it sends
        report.operation = request.form['operation']

        db.session.commit()
        flash('Report successfully updated!')
        return redirect(url_for('reports.report_list'))

    customers = Customer.query.all()
    packages = Package.query.all()
    staff_members = Staff.query.all()
    return render_template('report/update_report.html', report=report, customers=customers, packages=packages, staff=staff_members)


@reports.route('/report/delete/<int:report_id>', methods=['POST'])
def delete_report(report_id):
    report = Report.query.get_or_404(report_id)
    db.session.delete(report)
    db.session.commit()
    flash('Report successfully deleted!')
    return redirect(url_for('reports.report_list'))

