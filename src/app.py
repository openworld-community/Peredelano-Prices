from flask import Flask, render_template

from routes.collections_routes import collections_bp
from routes.map_routes import map_bp
from routes.products_routes import products_bp
from routes.scraping_routes import scraping_bp
from routes.users_routes import users_bp
from routes.utils_routes import utils_bp


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("start_page.html")


# Регистрируем Blueprint
app.register_blueprint(users_bp)
app.register_blueprint(products_bp)
app.register_blueprint(map_bp)
app.register_blueprint(collections_bp)
app.register_blueprint(utils_bp)
app.register_blueprint(scraping_bp)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
