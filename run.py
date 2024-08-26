from flask_wtf import CSRFProtect

from app import create_app
from app.services.create_expertises import add_expertise_report, parts_and_statuses_fren, \
    print_expertise_report_features, parts_and_statuses_suspansiyon, print_suspansiyon_testi_report
import logging

app = create_app()
# configure logging
app.logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)

# csrf
csrf = CSRFProtect(app)

@app.template_filter('skip_none')
def skip_none(value):
    return value if value is not None else ''

def main():
    with app.app_context():
        add_expertise_report("Fren Testi", parts_and_statuses_fren, comment="")
        add_expertise_report("Süspansiyon Testi", parts_and_statuses_suspansiyon, comment="")
        print_suspansiyon_testi_report()
# print_expertise_report_features()



if __name__ == '__main__':
    #main()
    app.run(host="0.0.0.0", port="5131", debug=True)

