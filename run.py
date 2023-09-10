import argparse
import secrets
import json
from flask import Flask
from flask_ngrok import run_with_ngrok
from server.bp import bp
from server.website import Website
from server.backend import Backend_Api
from server.babel import create_babel
from pyngrok import ngrok  # Импортируйте ngrok

def parse_args():
    parser = argparse.ArgumentParser(description="Run the FreeGPT web application")
    parser.add_argument("--token", type=str, default="", help="Your ngrok token")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    # Load configuration from config.json
    config = json.load(open('config.json', 'r'))
    site_config = config['site_config']
    url_prefix = config.pop('url_prefix')

    # Создайте экземпляр приложения Flask
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(16)

    # Настройте Babel
    create_babel(app)

    # Настройте маршруты для веб-сайта
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

    # Зарегистрируйте blueprint
    app.register_blueprint(bp, url_prefix=url_prefix)

    # Запуск Flask с использованием Ngrok
    if args.token:
        # Используйте токен Ngrok, если он предоставлен в аргументах командной строки
        ngrok.set_auth_token(args.token)

    # Запустите Ngrok и получите общедоступный URL
    public_url = ngrok.connect(port=site_config['port'])

    # Выведите общедоступный URL в консоль
    print(" * Ngrok URL:", public_url)

    # Замените `app.run(**site_config)` на простой запуск Flask
    app.run()

