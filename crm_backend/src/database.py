"""
Configuración de base de datos para el CRM
"""

from flask_sqlalchemy import SQLAlchemy
import os

# Instancia de SQLAlchemy
db = SQLAlchemy()

def init_db():
    """Inicializar la base de datos y crear todas las tablas"""
    try:
        # Importar todos los modelos para que SQLAlchemy los reconozca
        from .models.user import User
        from .models.causa import Causa
        
        # Crear todas las tablas
        db.create_all()
        print("✅ Base de datos inicializada correctamente")
        
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {str(e)}")
        raise e

def get_db_url():
    """Obtener la URL de la base de datos desde variables de entorno"""
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # Railway y otras plataformas a veces usan postgres:// pero SQLAlchemy necesita postgresql://
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        return database_url
    else:
        # Usar SQLite por defecto para desarrollo
        return 'sqlite:///crm.db'

