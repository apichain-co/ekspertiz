from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from ..database import db
from ..models import Report, Customer, Package, Staff
from datetime import datetime
from ..services.enum_service import COLOR_MAPPING, TRANSMISSION_TYPE_MAPPING, FUEL_TYPE_MAPPING, map_to_enum
from ..services.report_service import (get_or_create_customer, create_report, get_or_create_vehicle_owner,
                                       get_or_create_agent, get_or_create_vehicle)
from sqlalchemy.exc import IntegrityError
from ..forms.report_form import ReportForm

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

    # Populate the package_id choices dynamically
    form.package_id.choices = [(pkg.id, pkg.name) for pkg in Package.query.all()]

    if request.method == 'GET':
        form.created_at.data = datetime.now()
        packages = Package.query.all()
        return render_template('reports.html', form=form, packages=packages)
    # print(form.data)

    if form.validate_on_submit():
        try:
            gear_type = map_to_enum(form.gear_type.data, TRANSMISSION_TYPE_MAPPING)
            fuel_type = map_to_enum(form.fuel_type.data, FUEL_TYPE_MAPPING)
            color = map_to_enum(form.color.data, COLOR_MAPPING)

            # Create or get the Customer with all provided data
            customer_data = {
                'customer_name': form.customer_name.data,
                'customer_phone': form.customer_phone.data,
                'customer_tax_no': form.customer_tax_no.data,
                'customer_email': form.customer_email.data,
                'customer_address': form.customer_address.data
            }
            customer = get_or_create_customer(customer_data)
            # Optionally create or get the VehicleOwner if the data is provided
            vehicle_owner = None
            if form.owner_name.data:
                vehicle_owner_data = {
                    'owner_name': form.owner_name.data,
                    'owner_tax_no': form.owner_tax_no.data,
                    'owner_phone': form.owner_phone.data,
                    'owner_address': form.owner_address.data
                }
                vehicle_owner = get_or_create_vehicle_owner(vehicle_owner_data)

            # Optionally create or get the Agent if the name is provided
            agent = None
            if form.agent_name.data:
                agent = get_or_create_agent(form.agent_name.data)

            vehicle = get_or_create_vehicle({
                'vehicle_plate': form.vehicle_plate.data,
                'engine_number': form.engine_number.data,
                'brand': form.brand.data,
                'model': form.model.data,
                'chassis_number': form.chassis_number.data,
                'color': color,
                'model_year': form.model_year.data,
                'gear_type': gear_type,
                'fuel_type': fuel_type,
                'vehicle_km': form.vehicle_km.data
            })

            new_report = create_report(
                inspection_date=form.inspection_date.data,
                vehicle_plate=form.vehicle_plate.data,
                chassis_number=form.chassis_number.data,
                brand=form.brand.data,
                model=form.model.data,
                model_year=form.model_year.data,
                customer_id=customer.id,
                package_id=form.package_id.data,
                operation=form.operation.data,
                created_by=form.created_by.data,
                registration_document_seen=form.registration_document_seen.data
            )

            # Optionally link VehicleOwner to the report if it was created
            if vehicle_owner:
                vehicle_owner.report_id = new_report.id
                db.session.add_package(vehicle_owner)

            # Optionally link Agent to the report if it was created
            if agent:
                agent.report_id = new_report.id
                db.session.add_package(agent)

            # Commit all changes
            db.session.commit()

            flash('Rapor başarıyla oluşturuldu!', 'success')
            return redirect(url_for('reports.report_list'))

        except IntegrityError as e:
            db.session.rollback()
            flash(f'Tüm değerleri doğru girdiğinize emin olun!', 'error')
            print(f"IntegrityError: {e}")

        except Exception as e:
            db.session.rollback()
            flash(f'Beklenmedik bir hata oluştu!', 'error')
            print(f"Unexpected Error: {e}")
    else:
        print("Form validation failed")
        print(form.errors)

    # Retrieve data for the form and render the template
    return render_template('reports.html', form=form)


@reports.route('/report/update/<int:report_id>', methods=['GET', 'POST'])
def update_report(report_id):
    report = Report.query.get_or_404(report_id)
    form = ReportForm(obj=report)

    if form.validate_on_submit():
        form.populate_obj(report)

        try:
            db.session.commit()
            flash('Rapor başarıyla güncellendi!', 'success')
            return redirect(url_for('reports.report_list'))
        except IntegrityError as e:
            db.session.rollback()
            flash(f'Tüm değerleri doğru girdiğinize emin olun!', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Beklenmedik bir hata oluştu!', 'error')

    # Retrieve necessary data for the form
    customers = Customer.query.all()
    packages = Package.query.all()
    staff_members = Staff.query.all()
    return render_template('report/update_report.html', form=form, customers=customers, packages=packages,
                           staff=staff_members)


@reports.route('/report/delete/<int:report_id>', methods=['POST'])
def delete_report(report_id):
    report = Report.query.get_or_404(report_id)
    db.session.delete(report)
    db.session.commit()
    flash('Report successfully deleted!')
    return redirect(url_for('reports.report_list'))
