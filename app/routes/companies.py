from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..database import db
from ..models import Company

companies = Blueprint('companies', __name__)

@companies.route('/company')
def company_detail():
    company = Company.query.first()
    return render_template('settings/update_company.html', company=company)

@companies.route('/company/add', methods=['GET', 'POST'])
def add_company():
    if request.method == 'POST':
        name = request.form['name']
        phone_1 = request.form.get('phone_1')
        phone_2 = request.form.get('phone_2')
        fax = request.form.get('fax')
        email = request.form.get('email')
        website = request.form.get('website')
        address = request.form.get('address')
        my_business_address_link = request.form.get('my_business_address_link')

        new_company = Company(
            name=name,
            phone_1=phone_1,
            phone_2=phone_2,
            fax=fax,
            email=email,
            website=website,
            address=address,
            my_business_address_link=my_business_address_link
        )
        db.session.add(new_company)
        db.session.commit()
        flash('New company successfully created!')
        return redirect(url_for('companies.company_detail'))

    return render_template('settings/add_company.html')

@companies.route('/company/update', methods=['GET', 'POST'])
def update_company():
    company = Company.query.first()

    if not company:
        # Provide default values if no company exists
        company = Company(
            name="Firma Adı",
            phone_1="000-000-0000",
            phone_2="000-000-0000",
            fax="000-000-0000",
            email="default@company.com",
            website="https://www.defaultcompany.com",
            address="123 Default Street, Default City, DC 12345",
            my_business_address_link="https://maps.google.com/?q=default+address"
        )
        db.session.add(company)
        db.session.commit()
        flash('Default company created. Please update the details.')

    if request.method == 'POST':
        company.name = request.form['name']
        company.phone_1 = request.form.get('phone_1')
        company.phone_2 = request.form.get('phone_2')
        company.fax = request.form.get('fax')
        company.email = request.form.get('email')
        company.website = request.form.get('website')
        company.address = request.form.get('address')
        company.my_business_address_link = request.form.get('my_business_address_link')

        db.session.commit()
        flash('Company successfully updated!')
        return redirect(url_for('companies.company_detail'))

    return render_template('settings/update_company.html', company=company)


@companies.route('/company/delete', methods=['POST'])
def delete_company():
    company = Company.query.first()
    db.session.delete(company)
    db.session.commit()
    flash('Company successfully deleted!')
    return redirect(url_for('companies.company_detail'))
