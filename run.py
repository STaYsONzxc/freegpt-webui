import secrets
from server.bp import bp
from server.website import Website
from server.backend import Backend_Api
from server.babel import create_babel
from json import load
from flask import Flask
from pyngrok import ngrok

# Используйте значение переменной Token
ngrok.set_auth_token(Token)

# Остальной код остается неизменным
if __name__ == '__main__':
    # Load configuration from config.json
    config = load(open('config.json', 'r'))
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

    # Start Ngrok and create a tunnel for the Flask app
    public_url = ngrok.connect(site_config['port'])
    print(f" * ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:{site_config['port']}\"")

    try:
        # Run the Flask server
        app.run(host="0.0.0.0", port=site_config['port'])
    except KeyboardInterrupt:
        # If the user presses Ctrl+C, gracefully stop the Ngrok tunnel and exit
        ngrok.disconnect(public_url)
        print(" * ngrok tunnel stopped")

