from app.database import db
from app.models import ExpertiseReport, ExpertiseFeature, ExpertiseType

def add_expertise_report(expertise_name, parts_and_statuses, comment=""):

    # Step 1: Create or retrieve the ExpertiseType
    expertise_type = ExpertiseType.query.filter_by(name=expertise_name).first()
    if not expertise_type:
        expertise_type = ExpertiseType(name=expertise_name)
        db.session.add(expertise_type)
        db.session.commit()

    # Step 2: Create the ExpertiseReport for this type
    existing_report = ExpertiseReport.query.filter_by(expertise_type=expertise_type).first()
    if existing_report:
        print(f"ExpertiseReport for '{expertise_name}' already exists. No duplicate created.")
        return

    expertise_report = ExpertiseReport(expertise_type=expertise_type, comment=comment)
    db.session.add(expertise_report)
    db.session.commit()

    # Step 3: Add each part as an ExpertiseFeature to the report
    for part_name, status in parts_and_statuses:
        feature = ExpertiseFeature(name=part_name, status=status, expertise_report=expertise_report)
        db.session.add(feature)

    # Step 4: Commit all the changes to the database
    db.session.commit()

    print(f"{expertise_name} report added successfully!")

parts_and_statuses_fren = [
    ("Ön Sol Fren", None),
    ("Ön Sağ Fren", None),
    ("Arka Sol Fren", None),
    ("Arka Sağ Fren", None),
    ("El Freni Sol", None),
    ("El Freni Sağ", None),
]


parts_and_statuses_suspansiyon = [
    ("SOL ÖN", None),
    ("SAĞ ÖN", None),
    ("SOL ARKA", None),
    ("SAĞ ARKA", None),
]

def print_expertise_report_features():
    # Query all ExpertiseReports
    expertise_reports = ExpertiseReport.query.all()

    # Iterate through each report
    for report in expertise_reports:
        print(f"Expertise Report: {report.expertise_type.name}")
        print("Features and Statuses:")

        # Iterate through each feature in the report
        for feature in report.features:
            print(f"  - {feature.name}: {feature.status}")

        print("\n")  # Add a newline for better readability

def print_suspansiyon_testi_report():
    # Create the Flask app context
    # Query the ExpertiseType for "Süspansiyon Testi"
    expertise_type = ExpertiseType.query.filter_by(name="Süspansiyon Testi").first()

    if not expertise_type:
        print("No 'Süspansiyon Testi' report found.")
        return

    # Query the ExpertiseReport for this ExpertiseType
    expertise_report = ExpertiseReport.query.filter_by(expertise_type=expertise_type).first()

    if not expertise_report:
        print("No 'Süspansiyon Testi' expertise report found.")
        return

    print(f"Expertise Report: {expertise_report.expertise_type.name}")
    print("Features and Statuses:")

    # Iterate through each feature in the report
    for feature in expertise_report.features:
        print(f"  - {feature.name}: {feature.status}")

    print("\n")  # Add a newline for better readability