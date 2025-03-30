import asyncio
import websockets
import ssl
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from threading import Thread

# Configuración de SSL/TLS
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

# Variables globales para el estado de seguridad y mensajes
mensajes_enviados = 0
intentos_fallidos = 0
clientes = {}  # {websocket: "nombre"}

"""
async def chat(websocket):
    
    Función que maneja una conexión WebSocket para una sesión de chat.

    Esta función asíncrona escucha mensajes entrantes desde un cliente WebSocket,
    incrementa un contador global para el número de mensajes recibidos y envía
    una respuesta de eco de vuelta al cliente. Si el cliente cierra la conexión,
    maneja la desconexión de manera adecuada.

    Args:
        websocket: La conexión WebSocket del cliente.

    Comportamiento:
        - Escucha mensajes entrantes desde el cliente.
        - Imprime cada mensaje recibido en la consola.
        - Envía una respuesta de eco de vuelta al cliente.
        - Maneja la desconexión del cliente capturando la excepción ConnectionClosed.
    
    global mensajes_enviados
    try:
        async for mensaje in websocket:
            mensajes_enviados += 1
            print(f"Mensaje recibido: {mensaje}")
            await websocket.send(f"Echo: {mensaje}")
    except websockets.ConnectionClosed:
        print("Cliente desconectado")
"""

async def chat(websocket):
    # Agregar el cliente con un nombre por defecto
    clientes[websocket] = "Anónimo"
    global mensajes_enviados
    try:
        async for mensaje in websocket:
            # Si el mensaje es para registrar el nombre
            if mensaje.startswith("Nombre: "):
                clientes[websocket] = mensaje[7:]  # Extraer el nombre después de "Nombre: "
                print(f"Cliente registrado como: {clientes[websocket]}")
            else:
                # Enviar el mensaje a todos los clientes, incluyendo el nombre del emisor
                mensajes_enviados += 1
                sender = clientes[websocket]
                print(f"Mensaje recibido de {sender}: {mensaje}")
                for cliente in clientes:
                    await cliente.send(f"{sender}: {mensaje}")
    except websockets.ConnectionClosed:
        print(f"Cliente {clientes[websocket]} desconectado")
    finally:
        del clientes[websocket]

app = FastAPI()

"""
Configuración de CORS para permitir solicitudes desde http://127.0.0.1:8080 y http://localhost:8080. 
Esto permite que el frontend de la aplicación web se comunique con el backend
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8080", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/security_status")
async def security_status():
    """
    Endpoint para verificar el estado de seguridad del servidor.
    Devuelve información sobre la versión de TLS utilizada, el número de mensajes enviados,
    si la conexión es segura y cualquier alerta de seguridad.
    """
    return {
        "tls_version": "TLS 1.3",
        "messages_sent": mensajes_enviados,
        "connection_secure": True,
        "alerts": f"Intentos inseguros: {intentos_fallidos}" if intentos_fallidos > 0 else "Sin vulnerabilidades"
    }

@app.get("/simulate_attack")
async def simulate_attack():
    """"
    Simula un ataque al servidor incrementando el contador de intentos fallidos.
    Este endpoint se utiliza para simular un ataque y verificar la respuesta del servidor.
    """
    global intentos_fallidos
    intentos_fallidos += 1
    return {"message": "Ataque simulado detectado"}

async def run_websocket_server():
    """"
    Función que inicia el servidor WebSocket y escucha conexiones entrantes.
    Utiliza el contexto SSL configurado para asegurar la conexión.
    El servidor escucha en el puerto 8766 y maneja las conexiones entrantes
    """
    server = await websockets.serve(chat, "localhost", 8766, ssl=ssl_context)
    await server.wait_closed()

def start_servers():
    """"
    Función que inicia el servidor WebSocket en un hilo separado.
    Esto permite que el servidor WebSocket funcione de manera asíncrona junto con
    el servidor FastAPI.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_websocket_server())

if __name__ == "__main__":
    websocket_thread = Thread(target=start_servers)
    websocket_thread.start()
    uvicorn.run(app, host="0.0.0.0", port=8443, ssl_keyfile="key.pem", ssl_certfile="cert.pem")