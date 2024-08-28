from flask_wtf import CSRFProtect
from app import create_app
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5131", debug=True)

