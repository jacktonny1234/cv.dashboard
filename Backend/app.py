
import os
import configparser
from flask import Flask, render_template, Blueprint, request
from api.face import face_v1
from api.yolo import yolo_v1
from flask_cors import CORS

def create_app():

    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    STATIC_FOLDER = os.path.join(APP_DIR, 'build/static')
    TEMPLATE_FOLDER = os.path.join(APP_DIR, 'build')

    app = Flask(__name__, static_folder=STATIC_FOLDER,
                template_folder=TEMPLATE_FOLDER,
                )

    # Enable CORS for all routes
    CORS(app, resources={r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Origin"]
    }})
    
    app.register_blueprint(face_v1)
    app.register_blueprint(yolo_v1)

    @app.before_request
    def log_request_info():
        print("=" * 50)
        print(f"Incoming request: {request.method} {request.path}")
        print(f"Headers: {dict(request.headers)}")
        print("=" * 50)
    
    @app.after_request
    def add_header(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = '*'
        response.headers['Access-Control-Allow-Methods'] = '*'
        return response

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def index(path):
        return '',404

    return app



if __name__ == "__main__":
    app = create_app()
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0', port=8888)
