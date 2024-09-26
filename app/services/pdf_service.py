import os

from flask import render_template, url_for
from unidecode import unidecode
from weasyprint import HTML

from ..models import Report, Company, Vehicle, Customer, Staff, PackageExpertise, ExpertiseFeature, ExpertiseReport


def create_pdf(report_id):
    report = Report.query.get(report_id)
    company = Company.query.first()
    vehicle = Vehicle.query.get(report.vehicle_id)
    customer = Customer.query.get(report.customer_id)
    package = report.package
    staff = Staff.query.get(report.created_by)

    package_expertise_reports = []
    for pe in package.package_expertises:
        expertise_reports = ExpertiseReport.query.filter_by(expertise_type_id=pe.expertise_type_id).all()
        report = expertise_reports[0]
        package_expertise_reports.append({
            'expertise_type_name': report.expertise_type.name,
            'comment': report.comment,
            'features': report.features
        })
    motor_image_url = url_for('static', filename='assets/pdf_imgs/motor_expertise.png', _external=True)
    fren_image_url = url_for('static', filename='assets/pdf_imgs/lastik.png', _external=True)

    images = [
        {'filename': 'logo.jpeg', 'url': url_for('static', filename='assets/pdf_imgs/logo.jpeg', _external=True),
         'type': 'logo'},
        {'filename': 'motor_expertise.png',
         'url': url_for('static', filename='assets/pdf_imgs/motor_expertise.png', _external=True), 'type': 'motor'},
        {'filename': 'lastik.png', 'url': url_for('static', filename='assets/pdf_imgs/lastik.png', _external=True),
         'type': 'fren'},
        {'filename': 'abs.png', 'url': url_for('static', filename='assets/pdf_imgs/abs.png', _external=True),
         'type': 'beyin'},
        {'filename': 'air.png', 'url': url_for('static', filename='assets/pdf_imgs/air.png', _external=True),
         'type': 'beyin'},
        {'filename': 'airbag.png', 'url': url_for('static', filename='assets/pdf_imgs/airbag.png', _external=True),
         'type': 'beyin'},
        {'filename': 'brain.png', 'url': url_for('static', filename='assets/pdf_imgs/brain.png', _external=True),
         'type': 'beyin'},
        {'filename': 'engine.png', 'url': url_for('static', filename='assets/pdf_imgs/engine.png', _external=True),
         'type': 'beyin'},
        {'filename': 'gearbox.png', 'url': url_for('static', filename='assets/pdf_imgs/gearbox.png', _external=True),
         'type': 'beyin'},
        {'filename': 'steering.png', 'url': url_for('static', filename='assets/pdf_imgs/steering.png', _external=True),
         'type': 'beyin'},
        {'filename': 'tire.png', 'url': url_for('static', filename='assets/pdf_imgs/tire.png', _external=True),
         'type': 'beyin'}
    ]

    # Define the output directory and filename
    base_dir = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(base_dir, 'pdfs')
    if not os.path.exists(directory):
        os.makedirs(directory)

    sanitized_customer_name = unidecode(customer.full_name.replace(" ", "_").replace("/", "_"))
    base_filename = os.path.join(directory, f"RAPOR_{sanitized_customer_name}.pdf")
    filename = os.path.join(directory, base_filename)
    counter = 1
    while os.path.exists(filename):
        filename = os.path.join(directory, f"RAPOR_{sanitized_customer_name}_{counter}.pdf")
        counter += 1

    rendered_html = render_template('report_pdf.html',
                                    report=report,
                                    company=company,
                                    vehicle=vehicle,
                                    customer=customer,
                                    staff=staff,
                                    package=package,
                                    package_expertise_reports=package_expertise_reports,
                                    motor_image_url=motor_image_url,
                                    fren_image_url=fren_image_url,
                                    images=images
                                    )
    HTML(string=rendered_html).write_pdf(filename)
    return filename
