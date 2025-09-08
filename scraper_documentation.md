# Documentación del Scraper para Oficina Judicial Virtual (OJV)

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Instalación y Configuración](#instalación-y-configuración)
4. [Guía de Uso](#guía-de-uso)
5. [API Reference](#api-reference)
6. [Estructura del Código](#estructura-del-código)
7. [Configuración de Producción](#configuración-de-producción)
8. [Troubleshooting](#troubleshooting)
9. [Mantenimiento](#mantenimiento)

## Introducción

El Scraper para la Oficina Judicial Virtual (OJV) es un componente integral del CRM Legal que permite la extracción automatizada de información de causas judiciales desde el sitio web oficial de la Oficina Judicial Virtual de Chile.

### Características Principales

- **Autenticación Múltiple**: Soporte para Clave Única y Clave Poder Judicial
- **Búsqueda Multi-Competencia**: Extracción de datos de Civil, Laboral, Penal, Cobranza, Familia, Suprema, Apelaciones y Disciplinario
- **Scraping Inteligente**: Manejo automático de paginación y detección de contenido duplicado
- **Integración CRM**: Sincronización bidireccional con Google Sheets y base de datos local
- **Interfaz Web**: Panel de control integrado en la PWA para gestión del scraper
- **Logging Avanzado**: Sistema de logs detallado para monitoreo y debugging

### Beneficios

- **Automatización**: Reduce el trabajo manual de consulta de causas
- **Actualización en Tiempo Real**: Mantiene el CRM actualizado con la información más reciente
- **Escalabilidad**: Capaz de procesar múltiples causas de forma masiva
- **Confiabilidad**: Manejo robusto de errores y reintentos automáticos



## Arquitectura del Sistema

### Componentes Principales

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PWA Frontend  │    │  Backend Flask  │    │  OJV Website    │
│                 │    │                 │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │ScraperPanel │ │◄──►│ │Scraper APIs │ │◄──►│ │   HTML/JS   │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
│                 │    │                 │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │                 │
│ │   CRM UI    │ │◄──►│ │  Database   │ │    │                 │
│ └─────────────┘ │    │ └─────────────┘ │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│  Google Sheets  │    │   WebSocket     │
│                 │    │  (Real-time)    │
└─────────────────┘    └─────────────────┘
```

### Flujo de Datos

1. **Autenticación**: El usuario se autentica en OJV a través del scraper
2. **Búsqueda**: Se envían consultas por rol a diferentes competencias
3. **Extracción**: Se parsean los resultados HTML y se extraen los datos estructurados
4. **Almacenamiento**: Los datos se guardan en la base de datos local
5. **Sincronización**: Los datos se sincronizan con Google Sheets
6. **Notificación**: Se notifica al frontend via WebSocket sobre las actualizaciones

### Tecnologías Utilizadas

- **Backend**: Python 3.11, Flask, SQLAlchemy
- **Scraping**: Requests, BeautifulSoup4, lxml
- **Base de Datos**: SQLite (desarrollo), PostgreSQL (producción recomendada)
- **Frontend**: React, Socket.IO
- **Comunicación**: REST APIs, WebSockets
- **Integración**: Google Sheets API, Google Apps Script


## Instalación y Configuración

### Requisitos del Sistema

- Python 3.11 o superior
- Node.js 18 o superior
- Acceso a internet para conectar con OJV
- Credenciales válidas de Clave Única o Clave Poder Judicial

### Instalación del Backend

```bash
# Clonar el repositorio
git clone <repository-url>
cd crm_backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
export FLASK_APP=src/main.py
export FLASK_ENV=development
export SECRET_KEY=your-secret-key-here
export DATABASE_URL=sqlite:///crm.db

# Inicializar base de datos
flask db init
flask db migrate
flask db upgrade

# Ejecutar servidor
python src/main.py
```

### Instalación del Frontend

```bash
# Navegar al directorio del frontend
cd crm_mobile_app

# Instalar dependencias
pnpm install

# Configurar variables de entorno
echo "VITE_API_URL=http://localhost:5000" > .env

# Ejecutar en modo desarrollo
pnpm dev

# Compilar para producción
pnpm build
```

### Configuración de Variables de Entorno

Crear un archivo `.env` en el directorio del backend:

```env
# Configuración de Flask
FLASK_APP=src/main.py
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-change-in-production

# Base de datos
DATABASE_URL=sqlite:///crm.db

# Google Sheets API (opcional)
GOOGLE_SHEETS_CREDENTIALS_FILE=path/to/credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=your-spreadsheet-id

# Configuración del Scraper
OJV_BASE_URL=https://oficinajudicialvirtual.pjud.cl
OJV_TIMEOUT=30
OJV_MAX_RETRIES=3
OJV_DELAY_BETWEEN_REQUESTS=2

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/scraper.log
```

### Configuración de Credenciales

Para usar el scraper, necesitarás configurar las credenciales de acceso a OJV:

1. **Clave Única**: Obtener credenciales en [claveunica.gob.cl](https://claveunica.gob.cl)
2. **Clave Poder Judicial**: Solicitar acceso a través del Poder Judicial

**Importante**: Las credenciales se manejan de forma segura y nunca se almacenan en texto plano.


## Guía de Uso

### Uso a través de la Interfaz Web (PWA)

#### 1. Acceso al Panel de Scraper

1. Abrir la PWA del CRM Legal
2. Navegar a la sección "Scraper OJV"
3. El panel mostrará el estado actual del scraper

#### 2. Iniciar Sesión en OJV

```javascript
// Desde el panel web:
1. Seleccionar tipo de autenticación (Clave Única o Clave Poder Judicial)
2. Ingresar usuario y contraseña
3. Hacer clic en "Iniciar Sesión"
4. Verificar que el estado cambie a "Conectado"
```

#### 3. Búsqueda Individual

```javascript
// Para buscar una causa específica:
1. Ir a la pestaña "Búsqueda"
2. Ingresar el número de rol (ej: 12345-2023)
3. Seleccionar la competencia
4. Hacer clic en "Buscar Causa"
5. Revisar los resultados en la sección inferior
```

#### 4. Scraping Masivo

```javascript
// Para procesar múltiples causas:
1. Ir a la pestaña "Masivo"
2. Ingresar los roles (uno por línea):
   12345-2023
   67890-2024
   11111-2023
3. Seleccionar las competencias a buscar
4. Marcar "Actualizar base de datos" si se desea
5. Hacer clic en "Iniciar Scraping"
6. Monitorear el progreso en la pestaña "Logs"
```

### Uso Programático (API)

#### Autenticación

```python
import requests

# Login con Clave Única
response = requests.post('http://localhost:5000/api/scraper/login', json={
    'username': 'tu_usuario',
    'password': 'tu_contraseña',
    'auth_type': 'clave_unica'
})

if response.json()['success']:
    session_id = response.json()['session_id']
    print("Login exitoso")
```

#### Búsqueda de Causa Individual

```python
# Buscar una causa específica
response = requests.post('http://localhost:5000/api/scraper/buscar-causa', json={
    'rol': '12345-2023',
    'competencia': 'civil'
})

causas = response.json()['causas']
for causa in causas:
    print(f"RIT: {causa['rit']}, Caratulado: {causa['caratulado']}")
```

#### Scraping Masivo

```python
# Procesar múltiples causas
roles = ['12345-2023', '67890-2024', '11111-2023']
competencias = ['civil', 'laboral', 'penal']

response = requests.post('http://localhost:5000/api/scraper/scraping-masivo', json={
    'roles': roles,
    'competencias': competencias,
    'actualizar_bd': True
})

result = response.json()
print(f"Procesadas: {result['total_causas_scrapeadas']} causas")
print(f"Nuevas: {result['causas_nuevas']}, Actualizadas: {result['causas_actualizadas']}")
```

### Uso desde Python (Directo)

```python
from scraper.ojv_scraper import OJVScraper

# Crear instancia del scraper
scraper = OJVScraper()

# Iniciar sesión
if scraper.login_clave_unica('usuario', 'contraseña'):
    print("Login exitoso")
    
    # Buscar una causa
    causas = scraper.buscar_causa_por_rol('12345-2023', 'civil')
    
    # Obtener detalles
    for causa in causas:
        detalle = scraper.obtener_detalle_causa(causa['rit'], 'civil')
        print(f"Causa: {causa['caratulado']}")
        print(f"Movimientos: {len(detalle.get('historial_movimientos', []))}")
    
    # Cerrar sesión
    scraper.logout()
```

### Programación de Tareas Automáticas

Para automatizar el scraping, puedes usar cron (Linux/Mac) o Task Scheduler (Windows):

```bash
# Ejemplo de crontab para ejecutar diariamente a las 8:00 AM
0 8 * * * cd /path/to/crm_backend && python scripts/daily_scraping.py
```

Crear el script `scripts/daily_scraping.py`:

```python
#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.scraper.ojv_scraper import OJVScraper
from src.models.causa import Causa

def daily_scraping():
    scraper = OJVScraper()
    
    # Obtener roles de causas activas desde la base de datos
    causas_activas = Causa.query.filter_by(estado='Activa').all()
    roles = [causa.rol for causa in causas_activas]
    
    # Realizar scraping
    if scraper.login_clave_unica(os.getenv('OJV_USERNAME'), os.getenv('OJV_PASSWORD')):
        resultados = scraper.scraper_causas_masivo(roles)
        print(f"Scraping completado: {len(resultados)} causas procesadas")
        scraper.logout()

if __name__ == "__main__":
    daily_scraping()
```


## API Reference

### Endpoints del Scraper

#### POST /api/scraper/login
Inicia sesión en la Oficina Judicial Virtual.

**Request Body:**
```json
{
    "username": "string",
    "password": "string",
    "auth_type": "clave_unica" | "clave_poder_judicial"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Login exitoso",
    "session_id": "string"
}
```

#### POST /api/scraper/buscar-causa
Busca una causa específica por número de rol.

**Request Body:**
```json
{
    "rol": "12345-2023",
    "competencia": "civil"
}
```

**Response:**
```json
{
    "success": true,
    "causas": [
        {
            "rit": "C-12345-2023",
            "tribunal": "1° Juzgado Civil de Santiago",
            "caratulado": "JUAN PEREZ CON MARIA GONZALEZ",
            "fecha_ingreso": "15/03/2023",
            "estado_cuaderno": "En Tramitación",
            "competencia": "civil"
        }
    ],
    "total": 1
}
```

#### POST /api/scraper/scraping-masivo
Realiza scraping masivo de múltiples causas.

**Request Body:**
```json
{
    "roles": ["12345-2023", "67890-2024"],
    "competencias": ["civil", "laboral"],
    "actualizar_bd": true
}
```

**Response:**
```json
{
    "success": true,
    "message": "Scraping masivo completado",
    "total_causas_scrapeadas": 5,
    "causas_nuevas": 2,
    "causas_actualizadas": 3,
    "causas": [...]
}
```

#### POST /api/scraper/detalle-causa
Obtiene el detalle completo de una causa.

**Request Body:**
```json
{
    "causa_id": "C-12345-2023",
    "competencia": "civil"
}
```

**Response:**
```json
{
    "success": true,
    "detalle": {
        "historial_movimientos": [
            {
                "fecha": "15/03/2023",
                "descripcion": "Ingreso de demanda",
                "tipo": "Resolución"
            }
        ],
        "partes": [],
        "documentos": []
    }
}
```

#### POST /api/scraper/sincronizar-con-sheets
Sincroniza los datos scrapeados con Google Sheets.

**Response:**
```json
{
    "success": true,
    "message": "Sincronización con Google Sheets completada",
    "causas_sincronizadas": 150
}
```

#### GET /api/scraper/estado-scraper
Obtiene el estado actual del scraper.

**Response:**
```json
{
    "success": true,
    "estado": {
        "total_causas": 150,
        "causas_por_competencia": {
            "civil": 80,
            "laboral": 45,
            "penal": 25
        },
        "ultima_actualizacion": "2023-12-01T10:30:00Z",
        "scraper_activo": false
    }
}
```

### Clases Python

#### OJVScraper

**Constructor:**
```python
scraper = OJVScraper()
```

**Métodos principales:**

##### login_clave_unica(username: str, password: str) -> bool
Realiza login usando Clave Única.

##### login_clave_poder_judicial(username: str, password: str) -> bool
Realiza login usando Clave Poder Judicial.

##### buscar_causa_por_rol(rol: str, competencia: str = "civil") -> List[Dict]
Busca una causa por número de rol.

**Parámetros:**
- `rol`: Número de rol (ej: "12345-2023")
- `competencia`: Tipo de competencia ("civil", "laboral", "penal", etc.)

**Retorna:** Lista de diccionarios con datos de las causas encontradas.

##### obtener_detalle_causa(causa_id: str, competencia: str) -> Optional[Dict]
Obtiene los detalles completos de una causa.

##### scraper_causas_masivo(lista_roles: List[str], competencias: List[str] = None) -> List[Dict]
Realiza scraping masivo de múltiples causas.

##### logout()
Cierra la sesión en OJV.

### Estructura de Datos

#### Causa (Datos básicos)
```python
{
    'rit': str,           # RIT de la causa
    'tribunal': str,      # Nombre del tribunal
    'caratulado': str,    # Caratulado de la causa
    'fecha_ingreso': str, # Fecha de ingreso
    'estado_cuaderno': str, # Estado del cuaderno (civil)
    'estado_causa': str,  # Estado de la causa (laboral/penal)
    'competencia': str,   # Tipo de competencia
    'ruc': str,          # RUC (solo penal)
    'cuaderno': str,     # Tipo de cuaderno (civil)
    'institucion': str   # Institución
}
```

#### Detalle de Causa
```python
{
    'historial_movimientos': [
        {
            'fecha': str,
            'descripcion': str,
            'tipo': str
        }
    ],
    'partes': [
        {
            'nombre': str,
            'tipo': str,
            'rut': str
        }
    ],
    'documentos': [
        {
            'nombre': str,
            'fecha': str,
            'tipo': str
        }
    ]
}
```


## Estructura del Código

### Directorio del Backend
```
crm_backend/
├── src/
│   ├── scraper/
│   │   ├── __init__.py
│   │   └── ojv_scraper.py          # Clase principal del scraper
│   ├── routes/
│   │   └── scraper_routes.py       # Endpoints API del scraper
│   ├── models/
│   │   └── causa.py               # Modelo de datos de causa
│   └── main.py                    # Aplicación Flask principal
├── requirements.txt               # Dependencias Python
└── README.md
```

### Directorio del Frontend
```
crm_mobile_app/
├── src/
│   ├── components/
│   │   └── ScraperPanel.jsx       # Panel de control del scraper
│   ├── lib/
│   │   └── api.js                # Cliente API
│   └── App.jsx                   # Aplicación principal
├── package.json
└── dist/                         # Archivos compilados
```

### Archivos de Configuración
- `requirements.txt`: Dependencias Python del backend
- `package.json`: Dependencias Node.js del frontend
- `.env`: Variables de entorno (no incluir en git)
- `test_scraper.py`: Suite de pruebas unitarias

## Configuración de Producción

### Consideraciones de Seguridad

1. **Credenciales**: Nunca hardcodear credenciales en el código
2. **HTTPS**: Usar siempre HTTPS en producción
3. **Rate Limiting**: Implementar límites de velocidad para evitar sobrecarga
4. **Logging**: Configurar logs apropiados sin exponer información sensible

### Variables de Entorno de Producción

```env
FLASK_ENV=production
SECRET_KEY=your-super-secure-secret-key
DATABASE_URL=postgresql://user:password@localhost/crm_db
OJV_TIMEOUT=60
OJV_MAX_RETRIES=5
OJV_DELAY_BETWEEN_REQUESTS=3
LOG_LEVEL=WARNING
```

### Despliegue con Docker

```dockerfile
# Dockerfile para el backend
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
EXPOSE 5000

CMD ["python", "src/main.py"]
```

### Monitoreo y Alertas

Configurar monitoreo para:
- Fallos de autenticación en OJV
- Errores de scraping
- Cambios en la estructura de la página OJV
- Rendimiento y tiempo de respuesta

## Troubleshooting

### Problemas Comunes

#### Error de Autenticación
```
Error: Credenciales inválidas
```
**Solución:**
1. Verificar que las credenciales sean correctas
2. Comprobar que la cuenta no esté bloqueada
3. Intentar login manual en OJV para verificar

#### Error de Conexión
```
Error: No se pudo conectar con OJV
```
**Solución:**
1. Verificar conexión a internet
2. Comprobar que OJV esté disponible
3. Revisar configuración de proxy si aplica

#### Datos No Encontrados
```
Warning: No se encontraron causas
```
**Solución:**
1. Verificar que el rol sea correcto
2. Comprobar que la competencia sea la adecuada
3. Verificar que la causa exista en OJV

#### Error de Parseo
```
Error: No se pudo parsear la respuesta HTML
```
**Solución:**
1. Verificar si OJV cambió su estructura HTML
2. Revisar los logs detallados
3. Actualizar los selectores CSS si es necesario

### Logs y Debugging

#### Habilitar Logging Detallado
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Revisar Logs del Sistema
```bash
# Ver logs en tiempo real
tail -f logs/scraper.log

# Buscar errores específicos
grep "ERROR" logs/scraper.log
```

## Mantenimiento

### Tareas de Mantenimiento Regular

#### Diario
- Revisar logs de errores
- Verificar que el scraping automático funcione
- Monitorear rendimiento

#### Semanal
- Revisar estadísticas de uso
- Verificar integridad de datos
- Actualizar dependencias si es necesario

#### Mensual
- Realizar backup de la base de datos
- Revisar y optimizar consultas
- Actualizar documentación si hay cambios

### Actualizaciones del Sistema

#### Actualizar Dependencias
```bash
# Backend
pip install -r requirements.txt --upgrade

# Frontend
pnpm update
```

#### Migración de Base de Datos
```bash
flask db migrate -m "Descripción del cambio"
flask db upgrade
```

### Monitoreo de Cambios en OJV

La Oficina Judicial Virtual puede cambiar su estructura HTML. Para detectar cambios:

1. **Monitoreo Automático**: Implementar alertas cuando el parseo falle
2. **Pruebas Regulares**: Ejecutar pruebas automatizadas diariamente
3. **Versionado**: Mantener versiones del HTML de referencia

### Contacto y Soporte

Para soporte técnico o reportar problemas:
- Revisar los logs detallados
- Incluir información del entorno (versión Python, OS, etc.)
- Proporcionar pasos para reproducir el problema
- Incluir ejemplos de datos que causan el error

---

**Nota**: Esta documentación debe mantenerse actualizada conforme evolucione el sistema. Última actualización: Diciembre 2023.

