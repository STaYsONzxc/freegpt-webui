import secrets
import os
from json import load
from flask import Flask
from pyngrok import ngrok

from server.bp import bp
from server.website import Website
from server.backend import Backend_Api
from server.babel import create_babel


if __name__ == '__main__':
    # Запустите Ngrok, чтобы получить публичный URL
    ngrok.set_auth_token(NgrokToken)
    public_url = ngrok.connect(port=site_config['port'])

    # Load configuration from config.json
    config = load(open('config.json', 'r'))
    site_config = config['site_config']
    url_prefix = config.pop('url_prefix')

    # Создайте приложение Flask
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(16)

    # Настройте Babel
    create_babel(app)

    # Настройте маршруты веб-сайта
    site = Website(bp, url_prefix)
    for route in site.routes:
        bp.add_url_rule(
            route,
            view_func=site.routes[route]['function'],
            methods=site.routes[route]['methods'],
        )

    # Настройте маршруты для бэкенда API
    backend_api = Backend_Api(bp, config)
    for route in backend_api.routes:
        bp.add_url_rule(
            route,
            view_func=backend_api.routes[route]['function'],
            methods=backend_api.routes[route]['methods'],
        )

    # Зарегистрируйте блюпринт
    app.register_blueprint(bp, url_prefix=url_prefix)

    # Запустите Flask-сервер
    print(f"Running on {public_url}")
    app.run(host=os.environ.get("COLAB_SERVER_IP", '0.0.0.0'), port=site_config['port'])
    print(f"Closing port {site_config['port']}")

