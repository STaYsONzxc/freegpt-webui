import secrets
from server.bp import bp
from server.website import Website
from server.backend import Backend_Api
from server.babel import create_babel
from json import load
from flask import Flask
import gradio as gr

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

# Define a Gradio interface
def flask_to_gradio(*args, **kwargs):
    # Use this function to send input to your Flask backend
    # You can define the logic to pass data and get responses from your Flask app here
    # For example, you can use Flask's request module to send data to your Flask routes
    pass

def gradio_to_flask(*args, **kwargs):
    # Use this function to convert Gradio's output to Flask response
    pass

interface = gr.Interface(
    fn=flask_to_gradio,
    inputs=gr.Textbox(),  # Define a simple text input
    outputs=None,
    fn_output=gradio_to_flask,
)

if __name__ == '__main__':
    # Run the Gradio interface
    interface.launch(share=True)

