from flask import Blueprint, render_template
from ..models import Customer

customers = Blueprint('customers', __name__)

# Customer List
@customers.route('/customers')
def customer_list():
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)
