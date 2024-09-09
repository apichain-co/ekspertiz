import io
import os
from unidecode import unidecode
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from ..models import Report, Company, Vehicle, Customer, PackageExpertise, ExpertiseFeature
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


def draw_dynamic_text(c, x, y, text):
    c.drawString(x * cm, y * cm, text)


def draw_header(c, report, company):
    # Draw the logo
    logo_path = "../logo.jpeg"  # Path to the logo file
    c.drawImage(logo_path, 2 * cm, 26 * cm, width=3 * cm, height=3 * cm, mask='auto')

    # Draw the company name and report information
    c.setFont("DejaVuSans", 16)
    c.drawString(14 * cm, 28.5 * cm, company.name)

    c.setFont("DejaVuSans", 12)
    c.setFillColor(colors.red)
    c.drawString(14 * cm, 28 * cm, f"RAPOR NO : -{report.id:08}")

    c.setFillColor(colors.black)
    c.drawString(14 * cm, 27.5 * cm, f"TARİH : {report.created_at.strftime('%d %B %Y')}")
    c.drawString(14 * cm, 27 * cm, f"SAAT : {report.created_at.strftime('%H:%M')}")


def draw_general_infos(c, report, vehicle):
    c.setFont("DejaVuSans", 11)
    c.drawString(6.2 * cm, 23.7 * cm, f"{report.staff.full_name}")
    c.drawString(6.2 * cm, 22.95 * cm, f"{report.created_at.strftime('%d.%m.%Y')}")
    c.drawString(6.2 * cm, 22.2 * cm, f"{report.created_at.strftime('%H:%M')}")
    c.drawString(6.2 * cm, 20.7 * cm, f"{vehicle.mileage}")

    # if report.finished_at:
    # c.drawString(12 * cm, 1 * cm, f"Araç Teslim Saati: {report.finished_at.strftime('%H:%M')}")
    # else:

    if report.registration_document_seen:
        draw_tick(c, 12.65, 6)
    else:
        draw_tick(c, 14.55, 6)


def draw_footer(c, company):
    c.setFont("DejaVuSans", 8)
    c.drawString(1.8 * cm, 2 * cm, f"{company.name}")
    c.drawString(1.8 * cm, 1.6 * cm, f"ADRES: {company.address}")
    c.drawString(1.8 * cm, 1.2 * cm, f"TELEFON: {company.phone_1}")
    c.drawString(6.4 * cm, 1.2 * cm, f"E-POSTA: {company.email}")


def draw_vehicle_info(c, vehicle):
    c.setFont("DejaVuSans", 10)
    c.drawString(6.2 * cm, 16.8 * cm, f"{vehicle.brand}")
    c.drawString(6.2 * cm, 16 * cm, f"{vehicle.model}")
    c.drawString(6.2 * cm, 15.2 * cm, f"{vehicle.model_year}")
    c.drawString(6.2 * cm, 14.5 * cm, f"{vehicle.plate}")
    c.drawString(6.2 * cm, 13 * cm, f"{vehicle.chassis_number}")
    if vehicle.engine_number:
        c.drawString(6.2 * cm, 13.8 * cm, f"{vehicle.engine_number}")
    c.drawString(6.2 * cm, 12.2 * cm, f"{vehicle.fuel_type.value}")


def draw_customer_info(c, customer):
    c.setFont("DejaVuSans", 9)
    c.drawString(6.2 * cm, 10.3 * cm, f"{customer.full_name}")
    if customer.phone_number:
        c.drawString(6.2 * cm, 9.5 * cm, f"{customer.phone_number}")
    if customer.tc_tax_number:
        c.drawString(6.2 * cm, 8.8 * cm, f"{customer.tc_tax_number}")
    if customer.email:
        c.drawString(6.2 * cm, 8 * cm, f"{customer.email}")
    if customer.address:
        c.drawString(6.2 * cm, 7.2 * cm, f"{customer.address}")


def draw_expertise_info(c, package):
    for package_expertise in package.package_expertises:
        expertise_type_name = package_expertise.expertise_type.name
        if expertise_type_name == "Boya & Kaporta Ekspertiz":
            draw_tick(c, 11.45, 22.67)
        elif expertise_type_name == "Süspansiyon Ekspertiz":
            draw_tick(c, 11.45, 21.77)
        elif expertise_type_name == "Yol & Dyno Ekspertiz":
            draw_tick(c, 11.45, 20.88)
        elif expertise_type_name == "Mekanik Ekspertiz":
            draw_tick(c, 11.45, 20)
        elif expertise_type_name == "Beyin Ekspertiz":
            draw_tick(c, 11.45, 19.1)
        elif expertise_type_name == "Motor Ekspertiz":
            draw_tick(c, 16.57, 22.67)
        elif expertise_type_name == "Yanal Kayma Ekspertiz":
            draw_tick(c, 16.57, 21.77)
        elif expertise_type_name == "İç & Dış Ekspertiz":
            draw_tick(c, 16.57, 20.88)
        elif expertise_type_name == "Fren Ekspertiz":
            draw_tick(c, 16.57, 20)
        # draw_tick(c, )


def draw_tick(c, x, y, size=0.3):
    c.setLineWidth(2)
    c.line(x * cm, y * cm, (x + size / 3) * cm, (y - size / 2) * cm)
    c.line((x + size / 3) * cm, (y - size / 2) * cm, (x + size) * cm, (y + size / 2) * cm)


def draw_fren(c, package_expertise):
    pass


def draw_boya_kaporta(c, package_expertise):
    pass


def draw_suspansiyon(c, package_expertise):
    pass


def draw_yol_dyno(c, package_expertise):
    pass


def draw_mekanik(c, package_expertise):
    pass


def draw_beyin(c, package_expertise):
    pass


def draw_motor(c, package_expertise):
    pass


def draw_yanal_kayma(c, package_expertise):
    pass


def draw_ic_dis(c, package_expertise):
    pass


def draw_expertises(c, package ):
    for package_expertise in package.package_expertises:
        expertise_type_name = package_expertise.expertise_type.name
        if expertise_type_name == "Boya & Kaporta Ekspertiz":
            draw_boya_kaporta(c, package_expertise)
        elif expertise_type_name == "Süspansiyon Ekspertiz":
            draw_suspansiyon(c, package_expertise)
        elif expertise_type_name == "Yol & Dyno Ekspertiz":
            draw_yol_dyno(c, package_expertise)
        elif expertise_type_name == "Mekanik Ekspertiz":
            draw_mekanik(c, package_expertise)
        elif expertise_type_name == "Beyin Ekspertiz":
            draw_beyin(c, package_expertise)
        elif expertise_type_name == "Motor Ekspertiz":
            draw_motor(c, package_expertise)
        elif expertise_type_name == "Yanal Kayma Ekspertiz":
            draw_yanal_kayma(c, package_expertise)
        elif expertise_type_name == "İç & Dış Ekspertiz":
            draw_ic_dis(c, package_expertise)
        elif expertise_type_name == "Fren Ekspertiz":
            draw_fren(c, package_expertise)


def create_pdf(report_id):
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))

    # Fetch the necessary data
    report = Report.query.get(report_id)
    company = Company.query.first()
    vehicle = Vehicle.query.get(report.vehicle_id)
    customer = Customer.query.get(report.customer_id)
    package = report.package
    expertise_reports = [pe.expertise_type.expertise_reports for pe in package.package_expertises]

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

    # Load the existing PDF template
    template_path = "data/pdfs/first_pg.pdf"  
    existing_pdf = PdfReader(open(template_path, "rb"))
    output_pdf = PdfWriter()

    # Create a canvas to draw on
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=A4)

    # Adjust your draw functions here
    draw_header(c, report, company)
    draw_footer(c, company)
    draw_general_infos(c, report, vehicle)
    draw_vehicle_info(c, vehicle)
    draw_customer_info(c, customer)
    draw_expertise_info(c, package)

    # Finalize the canvas
    c.showPage()
    c.save()
    packet.seek(0)
    new_pdf = PdfReader(packet)
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])

    output_pdf.add_page(page)

    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=A4)

    draw_header(c, report, company)
    draw_footer(c, company)

    c.showPage()
    c.save()

    packet.seek(0)
    new_pdf = PdfReader(packet)
    new_page = new_pdf.pages[0]  # This is the second page
    output_pdf.add_page(new_page)  # Add the second page directly to the output PDF

    with open(filename, "wb") as outputStream:
        output_pdf.write(outputStream)

    return filename
