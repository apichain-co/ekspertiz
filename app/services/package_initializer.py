import json
from app.database import db
from app.models import Package, ExpertiseType, PackageExpertise, ExpertiseReport, Agent, ExpertiseFeature, Report


def create_standard_package():
    existing_package = Package.query.filter_by(name="Standard Package").first()

    if existing_package:
        print("Package with the name 'Standard Package' already exists. Skipping creation.")
        return

    standard_package = Package(
        name="Standard Package",
        price=299.99,  # Example price, adjust as needed
        contents="Kaporta & Boya Ekspertiz, Motor Ekspertiz",
        active=True
    )
    db.session.add_package(standard_package)
    db.session.commit()

    # Step 2: Find the relevant expertise types
    expertise_names = ["Kaporta Ekspertiz", "Boya Ekspertiz", "Motor Ekspertiz"]
    expertises = ExpertiseType.query.filter(ExpertiseType.name.in_(expertise_names)).all()

    if not expertises:
        print("Error: Some or all expertise types were not found.")
        return

    # Step 3: Associate expertise types with the package
    for expertise in expertises:
        package_expertise = PackageExpertise(package=standard_package, expertise_type=expertise)
        db.session.add_package(package_expertise)

    # Step 4: Commit the transaction
    db.session.commit()

    print(f"Standard Package with {', '.join(expertise_names)} created successfully.")
    # print_package_reports("Standard Package")



def print_package_reports(package_name):
    # Step 1: Retrieve the package by name
    package = Package.query.filter_by(name=package_name).first()
    if not package:
        print(f"Package '{package_name}' not found.")
        return

    # Step 2: Retrieve the associated expertise types through PackageExpertise
    package_expertises = PackageExpertise.query.filter_by(package_id=package.id).all()
    if not package_expertises:
        print(f"No expertises found for the package '{package_name}'.")
        return

    print(f"Reports for package '{package_name}':")

    # Step 3: For each associated expertise type, retrieve and print the reports and their features
    for package_expertise in package_expertises:
        expertise_reports = ExpertiseReport.query.filter_by(expertise_type_id=package_expertise.expertise_type_id).all()
        if expertise_reports:
            for report in expertise_reports:
                print(f"\n- Expertise: {report.expertise_type.name}, Report ID: {report.id}, Comment: {report.comment if report.comment else 'No Comment'}")
                # Step 4: Print all features and their statuses for this report
                if report.features:
                    for feature in report.features:
                        print(f"   - Feature: {feature.name}, Status: {feature.status}")
                else:
                    print("   No features found for this report.")
        else:
            print(f" - No reports found for expertise '{package_expertise.expertise_type.name}'")


def load_expertise_map(file_path='data/expertise_map.json'):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            expertise_map = json.load(file)
        return expertise_map
    except FileNotFoundError:
        print(f"JSON file not found: {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
        return {}

def get_default_features_for_expertise_type(expertise_name, expertise_map=None):
    if expertise_map is None:
        expertise_map = load_expertise_map()

    # Retrieve the features for the given expertise name
    return expertise_map.get(expertise_name, [])

