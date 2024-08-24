from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..database import db
from ..models import Report, Customer, Package

reports = Blueprint('reports', __name__)

# Reports List
@reports.route('/reports')
def report_list():
    reports = Report.query.all()
    return render_template('reports.html', reports=reports)

# Create New Report
@reports.route('/report/add', methods=['GET', 'POST'])
def add_report():
    if request.method == 'POST':
        inspection_date = request.form['inspection_date']
        vehicle_plate = request.form['vehicle_plate']
        chassis_number = request.form['chassis_number']  # Updated to match model attribute
        brand = request.form['brand']
        model = request.form['model']
        model_year = request.form['model_year']
        customer_id = request.form['customer_id']
        package_id = request.form['package_id']
        operation = request.form['operation']

        new_report = Report(
            inspection_date=inspection_date,
            vehicle_plate=vehicle_plate,
            chassis_number=chassis_number,  # Updated to match model attribute
            brand=brand,
            model=model,
            model_year=model_year,
            customer_id=customer_id,
            package_id=package_id,
            operation=operation
        )
        db.session.add(new_report)
        db.session.commit()
        flash('New report successfully created!')
        return redirect(url_for('reports.report_list'))

    customers = Customer.query.all()
    packages = Package.query.all()
    return render_template('add_report.html', customers=customers, packages=packages)
