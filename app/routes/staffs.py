from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..database import db
from ..models import Staff

staff = Blueprint('staff', __name__)

# Staff List
@staff.route('/staff')
def staff_list():
    staff = Staff.query.all()
    return render_template('staff.html', staff=staff)

# Add New Staff
@staff.route('/staff/add', methods=['GET', 'POST'])
def add_staff():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        phone_number = request.form['phone_number']
        department = request.form['department']

        new_staff = Staff(
            name=name,
            password=password,
            phone_number=phone_number,
            department=department
        )
        db.session.add_package(new_staff)
        db.session.commit()
        flash('New staff member successfully added!')
        return redirect(url_for('staff.staff_list'))

    return render_template('add_staff.html')
