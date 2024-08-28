from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..database import db
from ..models import Appointment, Customer
from datetime import datetime
from ..forms import AppointmentForm

appointments = Blueprint('appointments', __name__)


@appointments.route('/appointments')
def appointment_list():
    page = request.args.get('page', 1, type=int)  # Get the current page, default is 1
    per_page = request.args.get('per_page', 10, type=int)  # per_page, default is 10
    paginated_appointments = Appointment.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('appointment/appointment_list.html', appointments=paginated_appointments.items,
                           pagination=paginated_appointments)


@appointments.route('/appointment/add', methods=['GET', 'POST'])
def add_appointment():
    form = AppointmentForm()
    if form.validate_on_submit():
        customer_name = form.customer_name.data
        phone_number = form.phone_number.data
        date_obj = form.date.data
        time_obj = form.time.data
        brand = form.brand.data
        model = form.model.data

        customer = Customer.query.filter_by(full_name=customer_name, phone_number=phone_number).first()
        # finds customer with customer name & phone num, if not found creates new customer
        if not customer:
            customer = Customer(full_name=customer_name, phone_number=phone_number)
            db.session.add_package(customer)
            db.session.commit()

        new_appointment = Appointment(
            customer_id=customer.id,
            date=date_obj,
            time=time_obj,
            brand=brand,
            model=model
        )
        db.session.add_package(new_appointment)
        db.session.commit()
        flash('New appointment successfully created!', 'success')
        return redirect(url_for('appointments.appointment_list'))
    else:
        flash('Randevu oluşturma başarısız. Bilgileri doğru girdiğinize emin olun.', 'error')
        print("Form failed validation:", form.errors)

    customers = Customer.query.all()
    return render_template('appointment/add_appointment.html', form=form, customers=customers)


@appointments.route('/appointment/update/<int:appointment_id>', methods=['GET', 'POST'])
def update_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    form = AppointmentForm(obj=appointment)  # Populate the form with existing data

    if form.validate_on_submit():  # This checks if the form is submitted and passes validation
        appointment.customer.full_name = form.customer_name.data
        appointment.customer.phone_number = form.phone_number.data
        appointment.date = form.date.data
        appointment.time = form.time.data
        appointment.brand = form.brand.data
        appointment.model = form.model.data
        appointment.reminder_sent = form.reminder_sent.data

        db.session.commit()
        flash('Randevu başarıyla güncellendi!')
        return redirect(url_for('appointments.appointment_list'))

    return render_template('appointment/update_appointment.html', form=form, appointment=appointment)
