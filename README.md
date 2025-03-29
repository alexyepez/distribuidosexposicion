# Chat Seguro con TLS y Métricas en Tiempo Real
Este proyecto implementa un **chat seguro** utilizando WebSocket con TLS y una API REST con HTTPS, desarrollada con FastAPI. Incluye un sistema de métricas en tiempo real que muestra el número de mensajes enviados y detecta intentos de ataques simulados, todo protegido mediante cifrado TLS 1.3.

El objetivo es demostrar conceptos clave de seguridad web, como el uso de TLS para cifrado, la configuración de certificados autofirmados, y la resolución de problemas de CORS para integrar un frontend y un backend de manera segura.

## Características
- **Chat en Tiempo Real:** Comunicación bidireccional segura mediante WebSocket (wss://) con TLS.
- **API Segura:** Rutas HTTPS (/security_status y /simulate_attack) para métricas y simulación de ataques, construidas con FastAPI.
- **Métricas en Tiempo Real:** Muestra el número de mensajes enviados y alertas de intentos inseguros.
- **Seguridad TLS:** Conexiones cifradas usando un certificado autofirmado y TLS 1.3.
- **Solución de CORS:** Integración del frontend y backend mediante middleware CORS en FastAPI.

## Tecnologías Utilizadas
- **Python 3.13:** Backend con FastAPI y WebSocket.
- **FastAPI:** Framework para la API REST.
- **Uvicorn:** Servidor ASGI para ejecutar FastAPI con soporte HTTPS.
- **Websockets:** Biblioteca para el chat en tiempo real.
- **JavaScript/HTML:** Frontend simple con fetch para métricas y WebSocket para el chat.
- **TLS:** Cifrado mediante certificados autofirmados generados con OpenSSL.
- **http-server:** Servidor estático para el frontend.

## Requisitos Previos
- **Python 3.13+:** Asegúrate de tenerlo instalado.
- **Node.js:** Necesario para http-server.
- **OpenSSL:** Para generar certificados autofirmados (opcional si ya tienes cert.pem y key.pem).

## Instalación
1. **Clona el Repositorio:**
```bash
git clone https://github.com/alexyepez/distribuidosexposicion.git
cd https://github.com/alexyepez/distribuidosexposicion
```

2. **Instala las Dependencias de Python:**
```bash
pip install fastapi[all] uvicorn websockets
```

3. **Instala http-server para el Frontend:**
```bash
npm install -g http-server
```

4. **Genera Certificados Autofirmados (si no los tienes):**
```bash
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes
```
- Esto crea key.pem (clave privada) y cert.pem (certificado), usados para TLS.

## Ejecución
1. **Inicia el Servidor Backend:**
```bash
python server.py
```
- Escucha en https://127.0.0.1:8443 (API) y wss://127.0.0.1:8766 (WebSocket).

2. **Inicia el Servidor Frontend:**
```bash
http-server -p 8080
```
- Sirve index.html en http://127.0.0.1:8080.

3. **Accede a la Aplicación:**
- Abre tu navegador en http://127.0.0.1:8080.
- Acepta el certificado autofirmado en https://127.0.0.1:8443/security_status:
    - Chrome: Escribe thisisunsafe en la pantalla de advertencia.
    - Firefox: Haz clic en "Avanzado" > "Aceptar el riesgo y continuar".

4. **Prueba el Chat:**
- Escribe un mensaje y presiona "Enviar" para ver el eco.
- Simula un ataque abriendo https://127.0.0.1:8443/simulate_attack en otra pestaña.
- Observa cómo las métricas se actualizan con los mensajes enviados y los intentos inseguros.

 ## Estructura del Proyecto
```
chat_seguro/
│
├── server.py         # Backend con FastAPI y WebSocket
├── index.html        # Frontend con chat y métricas
├── cert.pem          # Certificado autofirmado
├── key.pem           # Clave privada
└── README.md         # Este archivo
```

## Detalles Técnicos
# Seguridad con TLS
- Se usa un contexto ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER) para configurar TLS 1.3, asegurando que las conexiones sean cifradas y seguras.
- Aunque el módulo se llama ssl, el protocolo implementado es TLS, reflejando una convención histórica en Python.

# Resolución de CORS
- El frontend (http://127.0.0.1:8080) y la API (https://127.0.0.1:8443) tienen orígenes distintos (protocolo y puerto diferentes), lo que activa la política CORS del navegador.
- Se añadió CORSMiddleware en FastAPI para permitir solicitudes desde el frontend, resolviendo el bloqueo de fetch.

# Ataque Simulado
- La ruta /simulate_attack incrementa un contador de intentos inseguros, simulando un ataque como un intento de downgrade de TLS o una intercepción MITM.
- En la vida real, esto podría permitir a un atacante leer o modificar datos si no hubiera cifrado adecuado.

## Uso
- **Chat:** Escribe mensajes en la interfaz y observa los ecos en tiempo real.
- **Métricas:** Se actualizan cada 2 segundos con fetch, mostrando:
    - Versión TLS.
    - Número de mensajes enviados.
    - Alertas de intentos inseguros.
- **Simulación de Ataque:** Accede a /simulate_attack para probar la detección de vulnerabilidades.

## Lecciones Aprendidas
- Configuración de TLS para conexiones seguras.
- Uso de FastAPI y WebSocket para aplicaciones en tiempo real.
- Resolución de problemas de CORS en integraciones frontend-backend.
- Importancia de la detección de intentos inseguros en sistemas seguros.

## Contribuciones
¡Siéntete libre de hacer un fork y contribuir! Reporta problemas o sugiere mejoras en la sección de Issues.

## Autor
- Alexander Castañeda - alexander.castaneda@utp.edu.co - alexyepez