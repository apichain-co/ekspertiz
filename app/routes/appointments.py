from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..database import db
from ..models import Appointment, Customer
from datetime import datetime

appointments = Blueprint('appointments', __name__)

@appointments.route('/appointments')
def appointment_list():
    page = request.args.get('page', 1, type=int)  # Get the current page, default is 1
    per_page = request.args.get('per_page', 10, type=int)  # per_page, default is 10
    paginated_appointments = Appointment.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('appointment/appointment_list.html', appointments=paginated_appointments.items, pagination=paginated_appointments)



@appointments.route('/appointment/add', methods=['GET', 'POST'])
def add_appointment():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        phone_number = request.form['phone_number']
        date_str = request.form['date']
        time_str = request.form['time']
        brand = request.form['brand']
        model = request.form['model']

        # Convert date string to Python date object
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

        # Convert time string to Python time object
        time_obj = datetime.strptime(time_str, '%H:%M').time()

        customer = Customer.query.filter_by(full_name=customer_name, phone_number=phone_number).first()
        if not customer:
            customer = Customer(full_name=customer_name, phone_number=phone_number)
            db.session.add(customer)
            db.session.commit()

        new_appointment = Appointment(
            customer_id=customer.id,
            date=date_obj,
            time=time_obj,
            brand=brand,
            model=model
        )
        db.session.add(new_appointment)
        db.session.commit()
        flash('New appointment successfully created!')
        return redirect(url_for('appointments.appointment_list'))

    customers = Customer.query.all()
    return render_template('appointment/add_appointment.html', customers=customers)


@appointments.route('/appointment/update/<int:appointment_id>', methods=['GET', 'POST'])
def update_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)

    if request.method == 'POST':
        appointment.customer.full_name = request.form['customer_name']
        appointment.customer.phone_number = request.form['phone_number']
        appointment.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        appointment.time = datetime.strptime(request.form['time'], '%H:%M').time()
        appointment.brand = request.form['brand']
        appointment.model = request.form['model']

        db.session.commit()
        flash('Randevu başarıyla güncellendi!')
        return redirect(url_for('appointments.appointment_list'))

    return render_template('appointment/update_appointment.html', appointment=appointment)
