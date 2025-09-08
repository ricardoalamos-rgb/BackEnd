# Guía de Uso del Scraper OJV - CRM Legal

## Introducción

Esta guía te ayudará a usar el scraper de la Oficina Judicial Virtual integrado en tu CRM Legal. El scraper te permite automatizar la obtención de información actualizada de tus causas directamente desde el sitio web oficial de OJV.

## Acceso al Scraper

### Desde la Aplicación Web (PWA)

1. **Abrir la aplicación**: Accede a tu CRM Legal desde el navegador
2. **Navegar al scraper**: Haz clic en "Scraper OJV" en el menú de navegación
3. **Verificar estado**: El panel mostrará el estado actual del scraper

## Configuración Inicial

### Paso 1: Preparar Credenciales

Antes de usar el scraper, asegúrate de tener:
- **Clave Única**: Usuario y contraseña de claveunica.gob.cl
- **O Clave Poder Judicial**: Credenciales del Poder Judicial

### Paso 2: Iniciar Sesión en OJV

1. En el panel del scraper, ve a la pestaña "Login"
2. Selecciona tu tipo de autenticación:
   - **Clave Única**: Para usuarios con cuenta de Clave Única
   - **Clave Poder Judicial**: Para usuarios con credenciales del PJ
3. Ingresa tu usuario y contraseña
4. Haz clic en "Iniciar Sesión"
5. Verifica que el estado cambie a "Conectado" ✅

## Uso Básico

### Búsqueda Individual de Causas

Para buscar una causa específica:

1. **Ir a la pestaña "Búsqueda"**
2. **Ingresar el rol**: Escribe el número de rol (ejemplo: `12345-2023`)
3. **Seleccionar competencia**: Elige entre:
   - Civil
   - Laboral
   - Penal
   - Cobranza
   - Familia
   - Suprema
   - Apelaciones
   - Disciplinario
4. **Buscar**: Haz clic en "Buscar Causa"
5. **Revisar resultados**: Los datos aparecerán en la sección inferior

### Scraping Masivo

Para procesar múltiples causas a la vez:

1. **Ir a la pestaña "Masivo"**
2. **Ingresar roles**: Escribe los números de rol, uno por línea:
   ```
   12345-2023
   67890-2024
   11111-2023
   22222-2023
   ```
3. **Seleccionar competencias**: Marca las competencias donde buscar
4. **Configurar actualización**: Marca "Actualizar base de datos" para guardar los datos
5. **Iniciar**: Haz clic en "Iniciar Scraping"
6. **Monitorear**: Ve a la pestaña "Logs" para seguir el progreso

## Funciones Avanzadas

### Sincronización con Google Sheets

Para actualizar tu Google Sheet con los datos scrapeados:

1. Asegúrate de haber configurado la integración con Google Sheets
2. En la pestaña "Masivo", haz clic en "Sincronizar Sheets"
3. Los datos se actualizarán automáticamente en tu hoja de cálculo

### Programación Automática

Puedes configurar el scraping para que se ejecute automáticamente:

1. **Diario**: Actualización automática cada mañana
2. **Semanal**: Revisión completa de todas las causas
3. **Bajo demanda**: Ejecutar cuando sea necesario

## Interpretación de Resultados

### Datos que Obtiene el Scraper

Para cada causa, el scraper extrae:

- **RIT/Rol**: Número identificador de la causa
- **Tribunal**: Juzgado que conoce la causa
- **Caratulado**: Nombre de las partes involucradas
- **Fecha de Ingreso**: Cuándo se inició la causa
- **Estado**: Estado actual de la causa
- **Competencia**: Tipo de materia (civil, laboral, etc.)

### Estados de las Causas

- **Activa**: La causa está en tramitación
- **En Tramitación**: Proceso en curso
- **Terminada**: Causa finalizada
- **Suspendida**: Proceso temporalmente detenido

## Monitoreo y Logs

### Revisar el Progreso

En la pestaña "Logs" puedes ver:
- ✅ **Éxito**: Operaciones completadas correctamente
- ⚠️ **Advertencias**: Situaciones que requieren atención
- ❌ **Errores**: Problemas que impidieron completar la operación

### Interpretar los Mensajes

- `"Iniciando sesión en OJV..."` - El scraper está conectándose
- `"Se encontraron X causas"` - Número de resultados obtenidos
- `"Scraping completado: X causas procesadas"` - Proceso finalizado
- `"Error en login: ..."` - Problema con las credenciales

## Solución de Problemas Comunes

### No Puedo Iniciar Sesión

**Problema**: El login falla constantemente
**Soluciones**:
1. Verifica que tus credenciales sean correctas
2. Intenta hacer login manual en el sitio web de OJV
3. Revisa si tu cuenta está bloqueada
4. Contacta al administrador del sistema

### No Encuentra Mis Causas

**Problema**: El scraper no encuentra causas que sé que existen
**Soluciones**:
1. Verifica que el número de rol sea correcto (formato: 12345-2023)
2. Prueba en diferentes competencias
3. Confirma que la causa esté visible en OJV manualmente
4. Revisa si hay restricciones de acceso

### El Scraping es Muy Lento

**Problema**: El proceso toma mucho tiempo
**Explicación**: El scraper incluye delays intencionales para:
- Evitar sobrecargar el servidor de OJV
- Prevenir que nos detecten como bot
- Mantener la estabilidad del sistema

**Recomendaciones**:
- Procesa causas en lotes pequeños (máximo 50 a la vez)
- Ejecuta el scraping en horarios de menor tráfico
- Sé paciente, la calidad de los datos vale la espera

## Mejores Prácticas

### Uso Responsable

1. **No abuses del sistema**: Usa el scraper con moderación
2. **Respeta los horarios**: Evita usar el scraper en horarios peak
3. **Mantén tus credenciales seguras**: No las compartas con nadie
4. **Reporta problemas**: Informa cualquier comportamiento extraño

### Optimización

1. **Agrupa por competencia**: Busca causas similares juntas
2. **Actualiza regularmente**: Mantén tus datos frescos
3. **Revisa los logs**: Identifica patrones y problemas
4. **Limpia tus datos**: Elimina causas obsoletas del sistema

## Integración con tu Flujo de Trabajo

### Rutina Diaria Recomendada

1. **Mañana (8:00 AM)**:
   - Revisar causas urgentes manualmente
   - Ejecutar scraping de causas prioritarias

2. **Mediodía (12:00 PM)**:
   - Revisar logs de la mañana
   - Procesar causas adicionales si es necesario

3. **Tarde (5:00 PM)**:
   - Ejecutar scraping masivo de todas las causas activas
   - Sincronizar con Google Sheets
   - Revisar resumen del día

### Integración con Google Sheets

El scraper actualiza automáticamente tu Google Sheet con:
- Nuevas causas encontradas
- Cambios de estado
- Actualizaciones de fechas
- Nuevos movimientos procesales

## Soporte y Ayuda

### Recursos Disponibles

1. **Documentación técnica**: Para desarrolladores y administradores
2. **Logs del sistema**: Para diagnóstico de problemas
3. **Panel de estado**: Para monitoreo en tiempo real

### Contacto

Si necesitas ayuda:
1. Revisa primero los logs en la pestaña correspondiente
2. Anota el mensaje de error exacto
3. Incluye el número de rol que causó el problema
4. Contacta al soporte técnico con esta información

---

**¡Importante!** El scraper es una herramienta poderosa que te ahorrará horas de trabajo manual. Úsala responsablemente y siempre verifica la información crítica directamente en el sitio web de OJV cuando sea necesario.

