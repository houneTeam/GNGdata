from flask import Flask
from routes import routes

app = Flask(__name__, template_folder='templates')
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
