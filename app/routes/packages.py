from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.database import db
from app.models.package import Package
from app.models.expertise import ExpertiseType  # Import your ExpertiseType model
from app.forms import PackageForm

packages = Blueprint('packages', __name__, url_prefix='/packages')

@packages.route('/add', methods=['GET', 'POST'])
def add_package():
    expertises = ExpertiseType.query.all()
    expertise_choices = [(str(expertise.id), expertise.name) for expertise in expertises]

    form = PackageForm(request.form)
    form.contents.choices = expertise_choices  # Set choices for SelectMultipleField dynamically

    if request.method == 'POST' and form.validate_on_submit():
        # Create a new package instance
        new_package = Package(
            name=form.name.data,
            price=form.price.data,
            contents=', '.join(form.contents.data),  # Join selected contents into a single string
            active=form.active.data == 'active'  # Convert to Boolean
        )
        # Add the new package to the database
        db.session.add(new_package)
        db.session.commit()

        flash('Package created successfully!', 'success')
        return redirect(url_for('packages.add_package'))
    else:
        print(form.errors)
        flash('Form validation failed.', 'error')

    return render_template('packages.html', form=form, expertises=expertises)
