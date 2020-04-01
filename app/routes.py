from app import app


@app.route('/')
@app.route('/hello')
def index():
    return "Hi, fellow Flask developer!"
