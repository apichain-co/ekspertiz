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
                                    motor_image_url=motor_image_url)
    HTML(string=rendered_html).write_pdf(filename)
    return filename

