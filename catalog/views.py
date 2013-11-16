from catalog import app, models

@app.route('/')
def index():
    return "Hello!"
