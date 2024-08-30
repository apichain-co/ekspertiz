from app.database import db
from app.models import ExpertiseReport, ExpertiseFeature, ExpertiseType


class ExpertiseInitializer:

    @classmethod
    def load_expertise_map(cls, file_path='data/expertise_map.json'):
        from pathlib import Path
        import json

        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"JSON file not found: {file_path}")

        with file_path.open('r', encoding='utf-8') as file:
            return json.load(file)

    @classmethod
    def add_expertise_report(cls, expertise_name, parts_and_statuses, comment=""):
        expertise_type = ExpertiseType.query.filter_by(name=expertise_name).first()
        if not expertise_type:
            expertise_type = ExpertiseType(name=expertise_name)
            db.session.add(expertise_type)  # Corrected line
            db.session.commit()
        else:
            existing_report = ExpertiseReport.query.filter_by(expertise_type=expertise_type).first()
            if existing_report:
                return False  # Indicates that the report already exists

        expertise_report = ExpertiseReport(expertise_type=expertise_type, comment=comment)
        db.session.add(expertise_report)  # Corrected line
        db.session.commit()

        for part in parts_and_statuses:
            feature = ExpertiseFeature(name=part['part_name'], status=part['default_status'], expertise_report=expertise_report)
            db.session.add(feature)  # Corrected line

        db.session.commit()

        return True  # Indicates that the report was successfully created

    @classmethod
    def initialize_expertise_reports(cls):
        expertise_map = cls.load_expertise_map()
        created_reports = []
        existing_reports = []

        for expertise_name, parts_and_statuses in expertise_map.items():
            if cls.add_expertise_report(expertise_name, parts_and_statuses):
                created_reports.append(expertise_name)
            else:
                existing_reports.append(expertise_name)

        # Print a summary message
        if created_reports:
            print(f"Successfully created reports: {', '.join(created_reports)}")
        if existing_reports:
            print(f"Reports already exist: {', '.join(existing_reports)}")
