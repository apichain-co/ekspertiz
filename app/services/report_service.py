from ..models import Report, Customer, VehicleOwner, Vehicle, Agent
from ..database import db
from datetime import datetime


def create_report(form_data, customer_id):
    new_report = Report(
        vehicle_plate=form_data['vehicle_plate'],
        chassis_number=form_data['chassis_number'],
        brand=form_data['brand'],
        model=form_data['model'],
        model_year=int(form_data['model_year']),
        inspection_date=datetime.strptime(form_data['inspection_date'], '%Y-%m-%d').date(),
        customer_id=customer_id,
        package_id=int(form_data['package_id']),
        created_by=int(form_data['created_by']),
        registration_document_seen=form_data.get('registration_document_seen') == 'on',
        operation=form_data['operation']
    )
    db.session.add(new_report)
    db.session.commit()
    return new_report



def get_or_create_customer(form_data):
    customer = Customer.query.filter_by(
        full_name=form_data['customer_name'],
        phone_number=form_data['customer_phone'],
        tc_tax_number=form_data['customer_tax_no'],
        email=form_data['customer_email'],
        address=form_data['customer_address']
    ).first()

    if not customer:
        customer = Customer(
            full_name=form_data['customer_name'],
            phone_number=form_data['customer_phone'],
            tc_tax_number=form_data['customer_tax_no'],
            email=form_data['customer_email'],
            address=form_data['customer_address']
        )
        db.session.add(customer)
        db.session.commit()
    return customer


def get_or_create_vehicle_owner(form_data):
    vehicle_owner = VehicleOwner.query.filter_by(
        full_name=form_data['owner_name'],
        tc_tax_number=form_data['owner_tax_no'],
        phone_number=form_data['owner_phone'],
        address=form_data['owner_address']
    ).first()

    if not vehicle_owner:
        vehicle_owner = VehicleOwner(
            full_name=form_data['owner_name'],
            tc_tax_number=form_data['owner_tax_no'],
            phone_number=form_data['owner_phone'],
            address=form_data['owner_address']
        )
        db.session.add(vehicle_owner)
        db.session.commit()
    return vehicle_owner


def get_or_create_agent(agent_name):
    agent = Agent.query.filter_by(full_name=agent_name).first()

    if not agent:
        agent = Agent(full_name=agent_name)
        db.session.add(agent)
        db.session.commit()
    return agent


def get_or_create_vehicle(form_data, report_id):
    vehicle = Vehicle.query.filter_by(
        plate=form_data['vehicle_plate'],
        chassis_number=form_data['chassis_number']
    ).first()

    if not vehicle:
        vehicle = Vehicle(
            plate=form_data['vehicle_plate'],
            engine_number=form_data['engine_number'],
            brand=form_data['brand'],
            model=form_data['model'],
            chassis_number=form_data['chassis_number'],
            color=form_data['color'],
            model_year=int(form_data['model_year']),
            transmission_type=form_data['gear_type'],
            fuel_type=form_data['fuel_type'],
            mileage=int(form_data['vehicle_km']),
            report_id=report_id
        )
        db.session.add(vehicle)
        db.session.commit()
    return vehicle



