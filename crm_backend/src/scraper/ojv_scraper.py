"""
Scraper para la Oficina Judicial Virtual de Chile
Extrae información de causas legales para integrar con el CRM
"""

import requests
from bs4 import BeautifulSoup
import time
import json
import logging
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin
import re

class OJVScraper:
    """Scraper para la Oficina Judicial Virtual de Chile"""
    
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://oficinajudicialvirtual.pjud.cl"
        self.login_url = f"{self.base_url}/home/index.php"
        self.is_logged_in = False
        
        # Headers para simular un navegador real
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def login_clave_unica(self, username: str, password: str) -> bool:
        """
        Realiza login usando Clave Única
        
        Args:
            username: Usuario de Clave Única
            password: Contraseña de Clave Única
            
        Returns:
            bool: True si el login fue exitoso, False en caso contrario
        """
        try:
            # Obtener la página principal
            response = self.session.get(self.login_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar el botón "Todos los Servicios" y luego "Clave Única"
            # Esto requiere análisis más detallado del HTML de login
            # Por ahora, simulamos el proceso
            
            self.logger.info("Iniciando proceso de login con Clave Única...")
            
            # Simular delay humano
            time.sleep(2)
            
            # Aquí iría la lógica específica de login con Clave Única
            # Esto requiere análisis del flujo de autenticación real
            
            # Por ahora, marcamos como logueado para continuar con el desarrollo
            self.is_logged_in = True
            self.logger.info("Login simulado exitoso")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error durante el login: {str(e)}")
            return False
    
    def login_clave_poder_judicial(self, username: str, password: str) -> bool:
        """
        Realiza login usando Clave Poder Judicial
        
        Args:
            username: Usuario de Clave Poder Judicial
            password: Contraseña de Clave Poder Judicial
            
        Returns:
            bool: True si el login fue exitoso, False en caso contrario
        """
        try:
            self.logger.info("Iniciando proceso de login con Clave Poder Judicial...")
            
            # Obtener la página principal
            response = self.session.get(self.login_url)
            response.raise_for_status()
            
            # Simular delay humano
            time.sleep(2)
            
            # Aquí iría la lógica específica de login con Clave Poder Judicial
            # Esto requiere análisis del flujo de autenticación real
            
            # Por ahora, marcamos como logueado para continuar con el desarrollo
            self.is_logged_in = True
            self.logger.info("Login simulado exitoso")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error durante el login: {str(e)}")
            return False
    
    def buscar_causa_por_rol(self, rol: str, competencia: str = "civil") -> List[Dict]:
        """
        Busca una causa por número de rol en la sección "Mis Causas"
        
        Args:
            rol: Número de rol de la causa (ej: "12345-2023")
            competencia: Tipo de competencia (civil, laboral, penal, etc.)
            
        Returns:
            List[Dict]: Lista de causas encontradas con sus datos
        """
        if not self.is_logged_in:
            self.logger.error("No se ha iniciado sesión")
            return []
        
        try:
            self.logger.info(f"Buscando causa con rol: {rol} en competencia: {competencia}")
            
            # URLs específicas por competencia basadas en el análisis del HTML
            competencia_urls = {
                "suprema": "misCausas/suprema/consultaMisCausasSuprema.php",
                "apelaciones": "misCausas/apelaciones/consultaMisCausasApelaciones.php",
                "civil": "misCausas/civil/consultaMisCausasCivil.php",
                "laboral": "misCausas/laboral/consultaMisCausasLaboral.php",
                "penal": "misCausas/penal/consultaMisCausasPenal.php",
                "cobranza": "misCausas/cobranza/consultaMisCausasCobranza.php",
                "familia": "misCausas/familia/consultaMisCausasFamilia.php",
                "disciplinario": "misCausas/disciplinario/consultaMisCausasDisciplinario.php"
            }
            
            if competencia not in competencia_urls:
                self.logger.error(f"Competencia no válida: {competencia}")
                return []
            
            # Preparar datos del formulario basados en el análisis del HTML
            form_data = self._preparar_datos_busqueda(rol, competencia)
            
            # Realizar la búsqueda
            search_url = urljoin(self.base_url, competencia_urls[competencia])
            
            # Simular delay humano
            time.sleep(1)
            
            response = self.session.post(search_url, data=form_data)
            response.raise_for_status()
            
            # Parsear los resultados
            causas = self._parsear_resultados_busqueda(response.content, competencia)
            
            # Si hay paginación, obtener todas las páginas
            if causas:
                causas_adicionales = self._obtener_paginas_adicionales(search_url, form_data, competencia)
                causas.extend(causas_adicionales)
            
            self.logger.info(f"Se encontraron {len(causas)} causas")
            return causas
            
        except Exception as e:
            self.logger.error(f"Error durante la búsqueda: {str(e)}")
            return []
    
    def _preparar_datos_busqueda(self, rol: str, competencia: str) -> Dict:
        """
        Prepara los datos del formulario para la búsqueda basado en el análisis del HTML
        
        Args:
            rol: Número de rol
            competencia: Tipo de competencia
            
        Returns:
            Dict: Datos del formulario preparados
        """
        # Extraer número y año del rol (ej: "12345-2023" -> rol="12345", año="2023")
        rol_parts = rol.split('-')
        numero_rol = rol_parts[0] if len(rol_parts) > 0 else rol
        año_rol = rol_parts[1] if len(rol_parts) > 1 else ""
        
        # Datos base comunes a todas las competencias
        base_data = {
            'tipCausaMisCau': 'M',  # Tipo de causa (M = Mis causas)
        }
        
        # Datos específicos por competencia basados en el análisis del HTML
        if competencia == "civil":
            form_data = {
                **base_data,
                'rutMisCauCiv': '',
                'dvMisCauCiv': '',
                'tipoMisCauCiv': '0',
                'rolMisCauCiv': numero_rol,
                'anhoMisCauCiv': año_rol,
                'tipCausaMisCauCiv': 'M',
                'estadoCausaMisCauCiv': '1',
                'fecDesdeMisCauCiv': '',
                'fecHastaMisCauCiv': '',
                'nombreMisCauCiv': '',
                'apePatMisCauCiv': '',
                'apeMatMisCauCiv': ''
            }
        elif competencia == "laboral":
            form_data = {
                **base_data,
                'rutMisCauLab': '',
                'dvMisCauLab': '',
                'tipoMisCaulab': '0',
                'rolMisCauLab': numero_rol,
                'anhoMisCauLab': año_rol,
                'tipCausaMisCauLab': 'M',
                'estadoCausaMisCauLab': '1',
                'fecDesdeMisCauLab': '',
                'fecHastaMisCauLab': '',
                'nombreMisCauLab': '',
                'apePatMisCauLab': '',
                'apeMatMisCauLab': ''
            }
        elif competencia == "penal":
            form_data = {
                **base_data,
                'rutMisCauPen': '',
                'dvMisCauPen': '',
                'tipoMisCauPen': '0',
                'rolMisCauPen': numero_rol,
                'anhoMisCauPen': año_rol,
                'tipCausaMisCauPen': 'M',
                'estadoCausaMisCauPen': '2',
                'fecDesdeMisCauPen': '',
                'fecHastaMisCauPen': '',
                'nombreMisCauPen': '',
                'apePatMisCauPen': '',
                'apeMatMisCauPen': ''
            }
        else:
            # Formato genérico para otras competencias
            form_data = {
                **base_data,
                f'rol{competencia.capitalize()}': numero_rol,
                f'anho{competencia.capitalize()}': año_rol,
            }
        
        return form_data
    
    def _parsear_resultados_busqueda(self, html_content: bytes, competencia: str) -> List[Dict]:
        """
        Parsea los resultados HTML de la búsqueda
        
        Args:
            html_content: Contenido HTML de la respuesta
            competencia: Tipo de competencia
            
        Returns:
            List[Dict]: Lista de causas parseadas
        """
        causas = []
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Buscar la tabla de resultados
            # El ID de la tabla varía según la competencia
            tabla_ids = {
                "civil": "verDetalleMisCauCiv",
                "laboral": "verDetalleMisCauLab",
                "penal": "verDetalleMisCauPen",
                "cobranza": "verDetalleMisCauCob",
                "familia": "verDetalleMisCauFam",
                "suprema": "verDetalleMisCauSup",
                "apelaciones": "verDetalleMisCauApe",
                "disciplinario": "verDetalleMisCauDisc"
            }
            
            tabla_id = tabla_ids.get(competencia, "verDetalleMisCauCiv")
            tabla = soup.find('div', {'id': tabla_id})
            
            if not tabla:
                self.logger.warning(f"No se encontró la tabla de resultados para {competencia}")
                return causas
            
            # Buscar filas de la tabla
            filas = tabla.find_all('tr')
            
            for fila in filas[1:]:  # Saltar el header
                celdas = fila.find_all('td')
                if len(celdas) >= 4:  # Mínimo de columnas esperadas
                    causa = self._extraer_datos_causa(celdas, competencia)
                    if causa:
                        causas.append(causa)
            
        except Exception as e:
            self.logger.error(f"Error parseando resultados: {str(e)}")
        
        return causas
    
    def _extraer_datos_causa(self, celdas: List, competencia: str) -> Optional[Dict]:
        """
        Extrae los datos de una causa desde las celdas de la tabla
        
        Args:
            celdas: Lista de celdas de la fila
            competencia: Tipo de competencia
            
        Returns:
            Optional[Dict]: Datos de la causa o None si hay error
        """
        try:
            # La estructura de columnas varía según la competencia
            # Basado en el análisis del HTML:
            
            if competencia == "civil":
                # Civil: Rit, Tribunal, Caratulado, Fecha Ingreso, Estado Cuaderno, Cuaderno, Institución
                return {
                    'rit': celdas[1].get_text(strip=True) if len(celdas) > 1 else '',
                    'tribunal': celdas[2].get_text(strip=True) if len(celdas) > 2 else '',
                    'caratulado': celdas[3].get_text(strip=True) if len(celdas) > 3 else '',
                    'fecha_ingreso': celdas[4].get_text(strip=True) if len(celdas) > 4 else '',
                    'estado_cuaderno': celdas[5].get_text(strip=True) if len(celdas) > 5 else '',
                    'cuaderno': celdas[6].get_text(strip=True) if len(celdas) > 6 else '',
                    'institucion': celdas[7].get_text(strip=True) if len(celdas) > 7 else '',
                    'competencia': competencia
                }
            elif competencia == "laboral":
                # Laboral: Rit, Tribunal, Caratulado, Fecha Ingreso, Estado Causa, Institución
                return {
                    'rit': celdas[1].get_text(strip=True) if len(celdas) > 1 else '',
                    'tribunal': celdas[2].get_text(strip=True) if len(celdas) > 2 else '',
                    'caratulado': celdas[3].get_text(strip=True) if len(celdas) > 3 else '',
                    'fecha_ingreso': celdas[4].get_text(strip=True) if len(celdas) > 4 else '',
                    'estado_causa': celdas[5].get_text(strip=True) if len(celdas) > 5 else '',
                    'institucion': celdas[6].get_text(strip=True) if len(celdas) > 6 else '',
                    'competencia': competencia
                }
            elif competencia == "penal":
                # Penal: Rit, Ruc, Tribunal, Caratulado, Fecha Ingreso, Estado Causa, Institución
                return {
                    'rit': celdas[1].get_text(strip=True) if len(celdas) > 1 else '',
                    'ruc': celdas[2].get_text(strip=True) if len(celdas) > 2 else '',
                    'tribunal': celdas[3].get_text(strip=True) if len(celdas) > 3 else '',
                    'caratulado': celdas[4].get_text(strip=True) if len(celdas) > 4 else '',
                    'fecha_ingreso': celdas[5].get_text(strip=True) if len(celdas) > 5 else '',
                    'estado_causa': celdas[6].get_text(strip=True) if len(celdas) > 6 else '',
                    'institucion': celdas[7].get_text(strip=True) if len(celdas) > 7 else '',
                    'competencia': competencia
                }
            else:
                # Formato genérico
                return {
                    'rol': celdas[1].get_text(strip=True) if len(celdas) > 1 else '',
                    'caratulado': celdas[2].get_text(strip=True) if len(celdas) > 2 else '',
                    'fecha_ingreso': celdas[3].get_text(strip=True) if len(celdas) > 3 else '',
                    'estado': celdas[4].get_text(strip=True) if len(celdas) > 4 else '',
                    'competencia': competencia
                }
                
        except Exception as e:
            self.logger.error(f"Error extrayendo datos de causa: {str(e)}")
            return None
    
    def _obtener_paginas_adicionales(self, search_url: str, form_data: Dict, competencia: str) -> List[Dict]:
        """
        Obtiene causas de páginas adicionales si hay paginación
        
        Args:
            search_url: URL de búsqueda
            form_data: Datos del formulario
            competencia: Tipo de competencia
            
        Returns:
            List[Dict]: Lista de causas adicionales
        """
        causas_adicionales = []
        pagina = 2  # Empezar desde la página 2
        
        try:
            while True:
                self.logger.info(f"Obteniendo página {pagina}")
                
                # Agregar número de página a los datos
                form_data_pagina = form_data.copy()
                form_data_pagina['pagina'] = str(pagina)
                
                # Simular delay humano
                time.sleep(1)
                
                response = self.session.post(search_url, data=form_data_pagina)
                response.raise_for_status()
                
                # Parsear resultados de esta página
                causas_pagina = self._parsear_resultados_busqueda(response.content, competencia)
                
                if not causas_pagina:
                    # No hay más resultados, terminar
                    break
                
                # Verificar si las causas son las mismas que la página anterior
                # para evitar bucles infinitos
                if causas_adicionales and causas_pagina == causas_adicionales[-len(causas_pagina):]:
                    self.logger.info("Detectado contenido duplicado, terminando paginación")
                    break
                
                causas_adicionales.extend(causas_pagina)
                pagina += 1
                
                # Límite de seguridad para evitar bucles infinitos
                if pagina > 10:  # Reducido de 100 a 10 para pruebas
                    self.logger.warning("Límite de páginas alcanzado")
                    break
                    
        except Exception as e:
            self.logger.error(f"Error obteniendo páginas adicionales: {str(e)}")
        
        return causas_adicionales
    
    def obtener_detalle_causa(self, causa_id: str, competencia: str) -> Optional[Dict]:
        """
        Obtiene los detalles completos de una causa específica
        
        Args:
            causa_id: ID de la causa
            competencia: Tipo de competencia
            
        Returns:
            Optional[Dict]: Detalles de la causa o None si hay error
        """
        if not self.is_logged_in:
            self.logger.error("No se ha iniciado sesión")
            return None
        
        try:
            self.logger.info(f"Obteniendo detalles de causa: {causa_id}")
            
            # URLs de detalle por competencia basadas en el análisis del HTML
            detalle_urls = {
                "civil": "../misCausas/civil/modal/misCausasCivil.php",
                "laboral": "../misCausas/laboral/modal/misCausasLaboral.php",
                "penal": "../misCausas/penal/modal/misCausasPenal.php",
                "cobranza": "../misCausas/cobranza/modal/misCausasCobranza.php",
                "familia": "../misCausas/familia/modal/misCausasFamilia.php",
                "suprema": "../misCausas/suprema/modal/misCausasSuprema.php",
                "apelaciones": "../misCausas/apelaciones/modal/misCausasApelaciones.php",
                "disciplinario": "../misCausas/disciplinario/modal/misCausasDisciplinario.php"
            }
            
            if competencia not in detalle_urls:
                self.logger.error(f"Competencia no válida para detalle: {competencia}")
                return None
            
            # Preparar datos para obtener el detalle
            detalle_data = {
                'dtaCausa': causa_id,
                'token': 'b36b9879b04415acb1868ce4df9fc422'  # Token encontrado en el HTML
            }
            
            detalle_url = urljoin(self.base_url, detalle_urls[competencia])
            
            # Simular delay humano
            time.sleep(1)
            
            response = self.session.post(detalle_url, data=detalle_data)
            response.raise_for_status()
            
            # Parsear el detalle
            detalle = self._parsear_detalle_causa(response.content, competencia)
            
            return detalle
            
        except Exception as e:
            self.logger.error(f"Error obteniendo detalle de causa: {str(e)}")
            return None
    
    def _parsear_detalle_causa(self, html_content: bytes, competencia: str) -> Dict:
        """
        Parsea el HTML del detalle de una causa
        
        Args:
            html_content: Contenido HTML del detalle
            competencia: Tipo de competencia
            
        Returns:
            Dict: Detalles parseados de la causa
        """
        detalle = {}
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extraer información general
            detalle['historial_movimientos'] = []
            detalle['partes'] = []
            detalle['documentos'] = []
            
            # Buscar tabla de movimientos/gestiones
            tablas = soup.find_all('table')
            for tabla in tablas:
                filas = tabla.find_all('tr')
                for fila in filas[1:]:  # Saltar header
                    celdas = fila.find_all('td')
                    if len(celdas) >= 3:
                        movimiento = {
                            'fecha': celdas[0].get_text(strip=True),
                            'descripcion': celdas[1].get_text(strip=True),
                            'tipo': celdas[2].get_text(strip=True) if len(celdas) > 2 else ''
                        }
                        detalle['historial_movimientos'].append(movimiento)
            
            # Buscar información de partes
            # Esto requiere análisis más específico del HTML de cada competencia
            
        except Exception as e:
            self.logger.error(f"Error parseando detalle: {str(e)}")
        
        return detalle
    
    def scraper_causas_masivo(self, lista_roles: List[str], competencias: List[str] = None) -> List[Dict]:
        """
        Realiza scraping masivo de múltiples causas
        
        Args:
            lista_roles: Lista de números de rol a buscar
            competencias: Lista de competencias a buscar (si None, busca en todas)
            
        Returns:
            List[Dict]: Lista de todas las causas encontradas
        """
        if competencias is None:
            competencias = ["civil", "laboral", "penal", "cobranza", "familia"]
        
        todas_las_causas = []
        
        for rol in lista_roles:
            self.logger.info(f"Procesando rol: {rol}")
            
            for competencia in competencias:
                causas = self.buscar_causa_por_rol(rol, competencia)
                
                # Obtener detalles de cada causa encontrada
                for causa in causas:
                    if 'rit' in causa:
                        detalle = self.obtener_detalle_causa(causa['rit'], competencia)
                        if detalle:
                            causa.update(detalle)
                
                todas_las_causas.extend(causas)
                
                # Delay entre competencias
                time.sleep(2)
            
            # Delay entre roles
            time.sleep(3)
        
        self.logger.info(f"Scraping completado. Total de causas: {len(todas_las_causas)}")
        return todas_las_causas
    
    def logout(self):
        """Cierra la sesión"""
        try:
            logout_url = f"{self.base_url}/salirN.php"
            self.session.get(logout_url)
            self.is_logged_in = False
            self.logger.info("Sesión cerrada")
        except Exception as e:
            self.logger.error(f"Error cerrando sesión: {str(e)}")

