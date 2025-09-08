# Guía de Instalación y Despliegue del CRM Legal con Scraper OJV

Esta guía te proporcionará los pasos necesarios para desplegar tu CRM Legal (frontend y backend con scraper integrado) en un entorno de producción. Es crucial seguir estos pasos cuidadosamente para asegurar el correcto funcionamiento de la aplicación.

## 1. Preparación del Entorno

Antes de comenzar, asegúrate de tener acceso a:

*   **Un editor de texto** (VS Code, Sublime Text, etc.)
*   **Acceso a una terminal/línea de comandos**
*   **Conexión a Internet**
*   **Cuenta de GitHub** (o similar) para alojar tu código
*   **Credenciales de Google Cloud Platform** (para la integración con Google Sheets)
*   **Credenciales de la Oficina Judicial Virtual** (Clave Única o Clave Poder Judicial)

## 2. Descomprimir el Proyecto

Primero, descomprime el archivo `crm_project_with_scraper.zip` que te proporcioné. Contendrá dos carpetas principales:

*   `crm_backend`: Contiene el código del servidor Flask (backend) con el scraper.
*   `crm_mobile_app`: Contiene el código de la Progressive Web App (PWA) del frontend.

## 3. Despliegue del Backend (Servidor Flask con Scraper)

El backend es el corazón de tu CRM, donde se gestiona la lógica de negocio, la base de datos y el scraper de la OJV. Te recomiendo usar **Railway** o **Render** para un despliegue sencillo y con planes gratuitos.

### Opción A: Despliegue con Railway (Recomendado)

1.  **Crea una cuenta en Railway**: Ve a [https://railway.app/](https://railway.app/) y regístrate (puedes usar tu cuenta de GitHub).
2.  **Crea un nuevo proyecto**: Haz clic en `New Project`.
3.  **Despliega desde un repositorio de GitHub**: Selecciona `Deploy from GitHub Repo`. Necesitarás subir la carpeta `crm_backend` a un nuevo repositorio en tu cuenta de GitHub.
4.  **Configura el despliegue**: Railway detectará automáticamente que es una aplicación Python. Asegúrate de que el comando de build sea `pip install -r requirements.txt` y el comando de inicio sea `python src/main.py`.
5.  **Configura las Variables de Entorno**: Esto es CRÍTICO. En la sección `Variables` de tu proyecto en Railway, añade las siguientes:
    *   `FLASK_APP`: `src/main.py`
    *   `FLASK_ENV`: `production`
    *   `SECRET_KEY`: Genera una clave secreta fuerte (ej. usando `os.urandom(24).hex()` en Python). **No uses la clave de desarrollo**.
    *   `DATABASE_URL`: Railway te proporcionará una base de datos PostgreSQL por defecto. Usa la URL que te dé Railway (ej. `postgresql://user:pass@host:port/db`). Si prefieres SQLite, puedes omitir esta variable y Railway usará el archivo `crm.db`.
    *   `OJV_BASE_URL`: `https://oficinajudicialvirtual.pjud.cl`
    *   `OJV_TIMEOUT`: `30`
    *   `OJV_MAX_RETRIES`: `3`
    *   `OJV_DELAY_BETWEEN_REQUESTS`: `2`
    *   `LOG_LEVEL`: `INFO`
    *   `GOOGLE_SHEETS_CREDENTIALS_FILE`: (Opcional) Si vas a usar la integración con Google Sheets, la ruta a tu archivo de credenciales JSON dentro del contenedor. Es más fácil montarlo como un secreto o volumen.
    *   `GOOGLE_SHEETS_SPREADSHEET_ID`: (Opcional) El ID de tu Google Sheet.
6.  **Despliega**: Haz clic en `Deploy`. Railway construirá y desplegará tu aplicación.
7.  **Obtén la URL del Backend**: Una vez desplegado, Railway te dará una URL pública (ej. `https://tu-backend-nombre.up.railway.app`). Anótala, la necesitarás para el frontend.

### Opción B: Despliegue con Render

1.  **Crea una cuenta en Render**: Ve a [https://render.com/](https://render.com/) y regístrate.
2.  **Crea un nuevo servicio web**: Haz clic en `New` -> `Web Service`.
3.  **Conecta tu repositorio de GitHub**: Sube la carpeta `crm_backend` a un nuevo repositorio en tu cuenta de GitHub y conéctalo a Render.
4.  **Configura el servicio**: 
    *   `Name`: Un nombre para tu servicio.
    *   `Region`: La región más cercana a ti.
    *   `Branch`: `main` (o la rama donde tengas tu código).
    *   `Root Directory`: `/` (si `crm_backend` es la raíz del repo).
    *   `Runtime`: `Python 3`.
    *   `Build Command`: `pip install -r requirements.txt`.
    *   `Start Command`: `python src/main.py`.
5.  **Configura las Variables de Entorno**: En `Advanced` -> `Environment Variables`, añade las mismas variables que en Railway.
6.  **Despliega**: Haz clic en `Create Web Service`.
7.  **Obtén la URL del Backend**: Render te proporcionará una URL pública (ej. `https://tu-backend-nombre.onrender.com`). Anótala.

## 4. Despliegue del Frontend (PWA)

El frontend es la interfaz de usuario de tu CRM. Te recomiendo usar **Vercel** o **Netlify** por su facilidad para desplegar PWAs y sitios estáticos.

### Opción A: Despliegue con Vercel (Recomendado)

1.  **Crea una cuenta en Vercel**: Ve a [https://vercel.com/](https://vercel.com/) y regístrate (puedes usar tu cuenta de GitHub).
2.  **Crea un nuevo proyecto**: Haz clic en `New Project`.
3.  **Importa tu repositorio de GitHub**: Sube la carpeta `crm_mobile_app` a un nuevo repositorio en tu cuenta de GitHub y conéctalo a Vercel.
4.  **Configura el proyecto**: Vercel detectará que es una aplicación React. Asegúrate de que el `Build Command` sea `pnpm build` y el `Output Directory` sea `dist`.
5.  **Configura las Variables de Entorno**: En `Environment Variables`, añade:
    *   `VITE_API_URL`: La URL pública de tu backend que obtuviste en el paso 3 (ej. `https://tu-backend-nombre.up.railway.app`).
6.  **Despliega**: Haz clic en `Deploy`.
7.  **Obtén la URL del Frontend**: Vercel te dará una URL pública (ej. `https://tu-pwa-nombre.vercel.app`).

### Opción B: Despliegue con Netlify

1.  **Crea una cuenta en Netlify**: Ve a [https://www.netlify.com/](https://www.netlify.com/) y regístrate.
2.  **Añade un nuevo sitio**: Haz clic en `Add new site` -> `Import an existing project`.
3.  **Conecta tu repositorio de GitHub**: Sube la carpeta `crm_mobile_app` a un nuevo repositorio en tu cuenta de GitHub y conéctalo a Netlify.
4.  **Configura el despliegue**: 
    *   `Base directory`: `/` (si `crm_mobile_app` es la raíz del repo).
    *   `Build command`: `pnpm build`.
    *   `Publish directory`: `dist`.
5.  **Configura las Variables de Entorno**: En `Build & deploy` -> `Environment`, añade:
    *   `VITE_API_URL`: La URL pública de tu backend.
6.  **Despliega**: Haz clic en `Deploy site`.
7.  **Obtén la URL del Frontend**: Netlify te proporcionará una URL pública (ej. `https://tu-pwa-nombre.netlify.app`).

## 5. Configuración de Google Cloud Platform (GCP)

Para que tu backend pueda interactuar con Google Sheets, necesitas autorizar las URLs de tu backend y frontend en tu proyecto de GCP.

1.  **Accede a Google Cloud Console**: Ve a [https://console.cloud.google.com/](https://console.cloud.google.com/)
2.  **Navega a APIs & Services > Credentials**.
3.  **Edita tu OAuth 2.0 Client ID** (el que creaste previamente para la integración con Google Sheets).
4.  En la sección **`Authorized JavaScript origins`**, añade la URL de tu frontend (ej. `https://tu-pwa-nombre.vercel.app`).
5.  En la sección **`Authorized redirect URIs`**, añade la URL de tu backend (ej. `https://tu-backend-nombre.up.railway.app`).
6.  **Guarda los cambios**.

## 6. Prueba del Scraper con Credenciales Reales

Una vez que tanto el backend como el frontend estén desplegados y las URLs autorizadas en GCP:

1.  **Accede a la PWA** desde tu iPhone o iPad usando la URL del frontend (ej. `https://tu-pwa-nombre.vercel.app`).
2.  **Instala la PWA** en tu pantalla de inicio (en Safari, usa el botón de compartir y selecciona "Añadir a pantalla de inicio").
3.  **Navega a la sección "Scraper OJV"** dentro de la PWA.
4.  **Introduce tus credenciales reales** de la Clave Única o Clave Poder Judicial en el formulario de login.
5.  **Haz clic en "Iniciar Sesión"**.
6.  Si el login es exitoso, podrás **realizar búsquedas de causas por rol** y ejecutar el **scraping masivo**.
7.  **Verifica los logs** en la pestaña "Logs" del panel del scraper para ver el progreso y los resultados.

## 7. Sincronización con Google Sheets

Para sincronizar los datos scrapeados con tu Google Sheet:

1.  Asegúrate de que la integración con Google Sheets esté configurada correctamente en tu backend (variables de entorno y archivo de credenciales).
2.  Desde el panel del scraper en la PWA, en la pestaña "Masivo", haz clic en "Sincronizar Sheets".
3.  Los datos de las causas scrapeadas se enviarán a tu Google Sheet.

## Solución de Problemas

*   **Errores de Despliegue**: Revisa los logs de despliegue en Railway/Render y Vercel/Netlify.
*   **Errores de Conexión**: Asegúrate de que `VITE_API_URL` en el frontend apunte a la URL correcta de tu backend.
*   **Errores de Scraper**: Revisa los logs en la pestaña "Logs" del panel del scraper en la PWA. Asegúrate de que tus credenciales sean correctas y que la OJV no haya cambiado su estructura.

¡Felicidades! Con estos pasos, tendrás tu CRM Legal con el scraper de la OJV funcionando en producción.

