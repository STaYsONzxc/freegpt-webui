import secrets
import json
from flask import Flask
from flask_ngrok import run_with_ngrok
from server.bp import bp
from server.website import Website
from server.backend import Backend_Api
from server.babel import create_babel

if __name__ == '__main__':
    # Load configuration from config.json
    config = json.load(open('config.json', 'r'))
    site_config = config['site_config']
    url_prefix = config.pop('url_prefix')

    # Create the app
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(16)

    # Set up Babel
    create_babel(app)

    # Set up the website routes
    site = Website(bp, url_prefix)
    for route in site.routes:
        bp.add_url_rule(
            route,
            view_func=site.routes[route]['function'],
            methods=site.routes[route]['methods'],
        )

    # Set up the backend API routes
    backend_api = Backend_Api(bp, config)
    for route in backend_api.routes:
        bp.add_url_rule(
            route,
            view_func=backend_api.routes[route]['function'],
            methods=backend_api.routes[route]['methods'],
        )

    # Register the blueprint
    app.register_blueprint(bp, url_prefix=url_prefix)

    # Run Flask with Ngrok
    run_with_ngrok(app)

    # Удалите 'host' из site_config, так как Flask уже настроен для использования Ngrok
    site_config.pop('host', None)

    # Замените `app.run(**site_config)` на простой запуск Flask
    app.run()
