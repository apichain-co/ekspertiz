from app import create_app

app = create_app()


@app.template_filter('skip_none')
def skip_none(value):
    return value if value is not None else ''



if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5131", debug=True)
