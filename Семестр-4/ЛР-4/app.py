from flask import Flask
from config import Configuration
from controllers.routes import bp


app = Flask(__name__)

app.register_blueprint(bp)
app.config.from_object(Configuration)

if __name__ == '__main__':
    app.run()
