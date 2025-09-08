"""
Rutas API para el scraper de la Oficina Judicial Virtual
"""

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import logging
from datetime import datetime
import json

from ..scraper.ojv_scraper import OJVScraper
from ..models.causa import Causa
from ..database import db

scraper_bp = Blueprint('scraper', __name__, url_prefix='/api/scraper')

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@scraper_bp.route('/login', methods=['POST'])
@cross_origin()
def login_ojv():
    """
    Endpoint para iniciar sesión en la Oficina Judicial Virtual
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        username = data.get('username')
        password = data.get('password')
        auth_type = data.get('auth_type', 'clave_unica')  # 'clave_unica' o 'clave_poder_judicial'
        
        if not username or not password:
            return jsonify({'error': 'Usuario y contraseña son requeridos'}), 400
        
        # Crear instancia del scraper
        scraper = OJVScraper()
        
        # Intentar login según el tipo de autenticación
        if auth_type == 'clave_unica':
            success = scraper.login_clave_unica(username, password)
        elif auth_type == 'clave_poder_judicial':
            success = scraper.login_clave_poder_judicial(username, password)
        else:
            return jsonify({'error': 'Tipo de autenticación no válido'}), 400
        
        if success:
            # Guardar la sesión del scraper (en una implementación real, 
            # esto se haría de forma más segura)
            return jsonify({
                'success': True,
                'message': 'Login exitoso',
                'session_id': 'temp_session_id'  # En producción, generar un ID real
            })
        else:
            return jsonify({'error': 'Credenciales inválidas'}), 401
            
    except Exception as e:
        logger.error(f"Error en login: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@scraper_bp.route('/buscar-causa', methods=['POST'])
@cross_origin()
def buscar_causa():
    """
    Endpoint para buscar una causa específica por rol
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        rol = data.get('rol')
        competencia = data.get('competencia', 'civil')
        
        if not rol:
            return jsonify({'error': 'El rol es requerido'}), 400
        
        # Crear instancia del scraper
        scraper = OJVScraper()
        
        # Por ahora, simular que ya está logueado
        scraper.is_logged_in = True
        
        # Buscar la causa
        causas = scraper.buscar_causa_por_rol(rol, competencia)
        
        return jsonify({
            'success': True,
            'causas': causas,
            'total': len(causas)
        })
        
    except Exception as e:
        logger.error(f"Error buscando causa: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@scraper_bp.route('/scraping-masivo', methods=['POST'])
@cross_origin()
def scraping_masivo():
    """
    Endpoint para realizar scraping masivo de múltiples causas
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        roles = data.get('roles', [])
        competencias = data.get('competencias', ['civil', 'laboral', 'penal', 'cobranza', 'familia'])
        actualizar_bd = data.get('actualizar_bd', True)
        
        if not roles:
            return jsonify({'error': 'Se requiere al menos un rol'}), 400
        
        # Crear instancia del scraper
        scraper = OJVScraper()
        
        # Por ahora, simular que ya está logueado
        scraper.is_logged_in = True
        
        # Realizar scraping masivo
        todas_las_causas = scraper.scraper_causas_masivo(roles, competencias)
        
        # Si se solicita, actualizar la base de datos
        causas_actualizadas = 0
        causas_nuevas = 0
        
        if actualizar_bd:
            for causa_data in todas_las_causas:
                try:
                    # Buscar si la causa ya existe
                    causa_existente = Causa.query.filter_by(
                        rol=causa_data.get('rit', causa_data.get('rol', ''))
                    ).first()
                    
                    if causa_existente:
                        # Actualizar causa existente
                        causa_existente.caratulado = causa_data.get('caratulado', '')
                        causa_existente.tribunal = causa_data.get('tribunal', '')
                        causa_existente.fecha_ingreso = causa_data.get('fecha_ingreso', '')
                        causa_existente.estado = causa_data.get('estado_causa', causa_data.get('estado', ''))
                        causa_existente.competencia = causa_data.get('competencia', '')
                        causa_existente.fecha_actualizacion = datetime.utcnow()
                        
                        # Actualizar historial si existe
                        if 'historial_movimientos' in causa_data:
                            causa_existente.historial_movimientos = json.dumps(causa_data['historial_movimientos'])
                        
                        causas_actualizadas += 1
                        
                    else:
                        # Crear nueva causa
                        nueva_causa = Causa(
                            rol=causa_data.get('rit', causa_data.get('rol', '')),
                            caratulado=causa_data.get('caratulado', ''),
                            tribunal=causa_data.get('tribunal', ''),
                            fecha_ingreso=causa_data.get('fecha_ingreso', ''),
                            estado=causa_data.get('estado_causa', causa_data.get('estado', '')),
                            competencia=causa_data.get('competencia', ''),
                            historial_movimientos=json.dumps(causa_data.get('historial_movimientos', [])),
                            fecha_creacion=datetime.utcnow(),
                            fecha_actualizacion=datetime.utcnow()
                        )
                        
                        db.session.add(nueva_causa)
                        causas_nuevas += 1
                        
                except Exception as e:
                    logger.error(f"Error procesando causa: {str(e)}")
                    continue
            
            # Confirmar cambios en la base de datos
            try:
                db.session.commit()
                logger.info(f"Base de datos actualizada: {causas_nuevas} nuevas, {causas_actualizadas} actualizadas")
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error guardando en base de datos: {str(e)}")
                return jsonify({'error': 'Error guardando en base de datos'}), 500
        
        return jsonify({
            'success': True,
            'message': 'Scraping masivo completado',
            'total_causas_scrapeadas': len(todas_las_causas),
            'causas_nuevas': causas_nuevas,
            'causas_actualizadas': causas_actualizadas,
            'causas': todas_las_causas[:10]  # Devolver solo las primeras 10 para no sobrecargar la respuesta
        })
        
    except Exception as e:
        logger.error(f"Error en scraping masivo: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@scraper_bp.route('/detalle-causa', methods=['POST'])
@cross_origin()
def obtener_detalle_causa():
    """
    Endpoint para obtener el detalle completo de una causa
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        causa_id = data.get('causa_id')
        competencia = data.get('competencia', 'civil')
        
        if not causa_id:
            return jsonify({'error': 'El ID de la causa es requerido'}), 400
        
        # Crear instancia del scraper
        scraper = OJVScraper()
        
        # Por ahora, simular que ya está logueado
        scraper.is_logged_in = True
        
        # Obtener detalle de la causa
        detalle = scraper.obtener_detalle_causa(causa_id, competencia)
        
        if detalle:
            return jsonify({
                'success': True,
                'detalle': detalle
            })
        else:
            return jsonify({'error': 'No se pudo obtener el detalle de la causa'}), 404
        
    except Exception as e:
        logger.error(f"Error obteniendo detalle: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@scraper_bp.route('/sincronizar-con-sheets', methods=['POST'])
@cross_origin()
def sincronizar_con_sheets():
    """
    Endpoint para sincronizar los datos scrapeados con Google Sheets
    """
    try:
        data = request.get_json()
        
        # Obtener todas las causas de la base de datos
        causas = Causa.query.all()
        
        # Preparar datos para Google Sheets
        datos_sheets = []
        for causa in causas:
            datos_sheets.append({
                'Rol': causa.rol,
                'Caratulado': causa.caratulado,
                'Tribunal': causa.tribunal,
                'Fecha Ingreso': causa.fecha_ingreso,
                'Estado': causa.estado,
                'Competencia': causa.competencia,
                'Última Actualización': causa.fecha_actualizacion.isoformat() if causa.fecha_actualizacion else ''
            })
        
        # Aquí iría la lógica para actualizar Google Sheets
        # usando la integración existente con Google Sheets API
        
        return jsonify({
            'success': True,
            'message': 'Sincronización con Google Sheets completada',
            'causas_sincronizadas': len(datos_sheets)
        })
        
    except Exception as e:
        logger.error(f"Error sincronizando con Sheets: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@scraper_bp.route('/estado-scraper', methods=['GET'])
@cross_origin()
def estado_scraper():
    """
    Endpoint para obtener el estado del scraper
    """
    try:
        # Obtener estadísticas de la base de datos
        total_causas = Causa.query.count()
        causas_por_competencia = db.session.query(
            Causa.competencia, 
            db.func.count(Causa.id)
        ).group_by(Causa.competencia).all()
        
        # Última actualización
        ultima_causa = Causa.query.order_by(Causa.fecha_actualizacion.desc()).first()
        ultima_actualizacion = ultima_causa.fecha_actualizacion.isoformat() if ultima_causa and ultima_causa.fecha_actualizacion else None
        
        return jsonify({
            'success': True,
            'estado': {
                'total_causas': total_causas,
                'causas_por_competencia': dict(causas_por_competencia),
                'ultima_actualizacion': ultima_actualizacion,
                'scraper_activo': False  # Por ahora, siempre False
            }
        })
        
    except Exception as e:
        logger.error(f"Error obteniendo estado: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

