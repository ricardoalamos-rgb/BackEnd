"""
Aplicación principal del backend CRM con integración de scraper OJV
"""

from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import os
import logging

# Importar configuración de base de datos
from .database import db, init_db

# Importar rutas
from .routes.causa import causa_bp
from .routes.user import user_bp
from .routes.google_sheets_integration import google_sheets_bp
from .routes.app_script_integration import app_script_bp
from .routes.scraper_routes import scraper_bp

# Importar WebSocket manager
from .websocket_manager import socketio, init_websocket_events

def create_app():
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///crm.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configurar CORS
    CORS(app, origins="*")
    
    # Inicializar base de datos
    db.init_app(app)
    
    # Inicializar WebSocket
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Registrar blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(causa_bp)
    app.register_blueprint(google_sheets_bp)
    app.register_blueprint(app_script_bp)
    app.register_blueprint(scraper_bp)
    
    # Inicializar eventos WebSocket
    init_websocket_events()
    
    # Crear tablas de base de datos
    with app.app_context():
        init_db()
    
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    @app.route('/')
    def index():
        return jsonify({
            'message': 'CRM Backend API con Scraper OJV',
            'version': '1.0.0',
            'endpoints': {
                'users': '/api/users',
                'causas': '/api/causas',
                'google_sheets': '/api/google-sheets',
                'app_script': '/api/app-script',
                'scraper': '/api/scraper'
            }
        })
    
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy'})
    
    return app

# Crear la aplicación
app = create_app()

if __name__ == '__main__':
    # Ejecutar en modo desarrollo
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

