#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler
import os
from app.config.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    CORS(app)
    
    # Configure logging
    if not os.path.exists('app/logs'):
        os.makedirs('app/logs')
    
    file_handler = RotatingFileHandler('app/logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Application startup')
    
    # Register blueprints
    from app.api.services import bp as services_bp
    app.register_blueprint(services_bp, url_prefix='/api/services')
    
    from app.api.frontend import bp as frontend_bp
    app.register_blueprint(frontend_bp, url_prefix='/api/frontend')
    
    return app 