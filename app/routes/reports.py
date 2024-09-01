from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from ..database import db
from ..enums import FuelType, TransmissionType, Color
from ..models import Report, Customer, Package, Staff, Vehicle
from datetime import datetime
from ..services.enum_service import COLOR_MAPPING, TRANSMISSION_TYPE_MAPPING, FUEL_TYPE_MAPPING, map_to_enum
from ..services.report_service import (get_or_create_customer, create_report, get_or_create_vehicle_owner,
                                       get_or_create_agent, get_or_create_vehicle, get_or_create_staff_by_name)
from sqlalchemy.exc import IntegrityError
from ..forms.report_form import ReportForm

reports = Blueprint('reports', __name__)


@reports.route('/reports')
def report_list():
    page = request.args.get('page', 1, type=int)  # Get the current page, default is 1
    per_page = request.args.get('per_page', 10, type=int)  # Items per page, default is 10
    paginated_reports = Report.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('report_sections/report_list.html', reports=paginated_reports.items, pagination=paginated_reports)




@reports.route('/report/add', methods=['GET', 'POST'])
def add_report():
    form = ReportForm()

    # Define choices for the form fields
    fuel_types = [(fuel.name, fuel.value) for fuel in FuelType]
    transmission_types = [(transmission.name, transmission.value) for transmission in TransmissionType]
    colors = [(color.name, color.value) for color in Color]

    # Populate dynamic choices for SelectFields
    form.package_id.choices = [(pkg.id, pkg.name) for pkg in Package.query.all()]
    form.color.choices = colors
    form.gear_type.choices = transmission_types
    form.fuel_type.choices = fuel_types

    form.created_by.choices = [(staff.id, staff.full_name) for staff in Staff.query.all()]

    packages = Package.query.all()
    current_year = datetime.now().year

    form.created_at.data = datetime.now()
    form.inspection_date.data = datetime.now()

    vehicle_info = None  # Initialize vehicle_info

    if form.validate_on_submit():
        try:
            # Create the Vehicle
            vehicle = get_or_create_vehicle({
                'vehicle_plate': form.vehicle_plate.data,
                'engine_number': form.engine_number.data,
                'brand': form.brand.data,
                'model': form.model.data,
                'chassis_number': form.chassis_number.data,
                'color': form.color.data,
                'model_year': form.model_year.data,
                'gear_type': form.gear_type.data,
                'fuel_type': form.fuel_type.data,
                'vehicle_km': form.vehicle_km.data,
            })

            # Update vehicle_info for use in rendering the form
            vehicle_info = {
                'plate': vehicle.plate,
                'brand': vehicle.brand,
                'model': vehicle.model,
                'chassis_number': vehicle.chassis_number,
                'color': vehicle.color.value,
                'model_year': vehicle.model_year,
                'transmission_type': vehicle.transmission_type.value,
                'fuel_type': vehicle.fuel_type.value,
                'mileage': vehicle.mileage
            }

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

            # Get or create the staff with name
            staff = get_or_create_staff_by_name(form.created_by)

            # Create a new Report with the generated vehicle details
            new_report = create_report(
                inspection_date=form.inspection_date.data,
                vehicle_id=vehicle.id,
                customer_id=customer.id,
                package_id=form.package_id.data,
                operation=form.operation.data,
                created_by=staff.id,
                registration_document_seen=form.registration_document_seen.data
            )
            # Optionally link VehicleOwner to the report if it was created
            if vehicle_owner:
                vehicle_owner.report_id = new_report.id
                db.session.add(vehicle_owner)

            # Optionally link Agent to the report if it was created
            if agent:
                agent.report_id = new_report.id
                db.session.add(agent)

            # Commit all changes
            db.session.commit()

            flash('Rapor başarıyla oluşturuldu!', 'success')
            return redirect(url_for('reports.report_list'))

        except IntegrityError as e:
            db.session.rollback()
            flash('Tüm değerleri doğru girdiğinize emin olun!', 'error')
            print(f"IntegrityError: {e}")

        except Exception as e:
            db.session.rollback()
            flash('Beklenmedik bir hata oluştu!', 'error')
            print(f"Unexpected Error: {e}")

    else:
        print("Form validation failed")
        print(form.errors)

    # Render the form with errors and vehicle info if available
    return render_template(
        'reports.html',
        form=form,
        fuel_types=fuel_types,
        transmission_types=transmission_types,
        colors=colors,
        vehicle_info=vehicle_info,
        packages=packages,
        current_year=current_year
    )


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
