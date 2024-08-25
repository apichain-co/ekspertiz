from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SelectField, DateField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length

class ReportForm(FlaskForm):
    # Customer Information
    customer_name = StringField('Customer Name', validators=[DataRequired(), Length(min=2, max=100)])
    customer_phone = StringField('Customer Phone', validators=[DataRequired(), Length(min=10, max=15)])
    customer_tax_no = StringField('Customer Tax No', validators=[Optional(), Length(max=11)])
    customer_email = StringField('Customer Email', validators=[Optional(), Length(max=100)])
    customer_address = TextAreaField('Customer Address', validators=[Optional(), Length(max=255)])

    # Owner Information
    owner_name = StringField('Owner Name', validators=[DataRequired(), Length(min=2, max=100)])
    owner_tax_no = StringField('Owner Tax No', validators=[Optional(), Length(max=11)])
    owner_phone = StringField('Owner Phone', validators=[DataRequired(), Length(min=10, max=15)])
    owner_address = TextAreaField('Owner Address', validators=[DataRequired(), Length(max=255)])

    # Vehicle Information
    vehicle_plate = StringField('Vehicle Plate', validators=[DataRequired(), Length(min=1, max=10)])
    engine_number = StringField('Engine Number', validators=[DataRequired(), Length(min=1, max=17)])
    brand = StringField('Brand', validators=[DataRequired(), Length(min=1, max=50)])
    model = StringField('Model', validators=[DataRequired(), Length(min=1, max=50)])
    chassis_number = StringField('Chassis Number', validators=[DataRequired(), Length(min=1, max=17)])
    color = StringField('Color', validators=[DataRequired(), Length(min=1, max=50)])
    model_year = IntegerField('Model Year', validators=[DataRequired()])
    gear_type = StringField('Gear Type', validators=[DataRequired()])
    fuel_type = StringField('Fuel Type', validators=[DataRequired()])
    vehicle_km = IntegerField('Vehicle KM', validators=[DataRequired()])

    # Inspection Information
    inspection_date = DateField('Inspection Date', validators=[DataRequired()], format='%Y-%m-%d')
    package_id = SelectField('Package ID', coerce=int, validators=[DataRequired()])
    created_by = IntegerField('Created By', validators=[DataRequired()])
    registration_document_seen = BooleanField('Registration Document Seen')
    operation = StringField('Operation', validators=[Optional(), Length(max=255)])

    # Agent Information
    agent_name = StringField('Agent Name', validators=[DataRequired(), Length(min=2, max=100)])

    # Additional fields for pricing
    package_price = StringField('Package Price', validators=[Optional()])
    package_price_vat = StringField('Package Price (VAT Included)', validators=[Optional()])

    submit = SubmitField('Create Report')
