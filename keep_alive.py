"""
Keep-Alive Service
Mantiene el servidor activo haciendo pings periódicos
"""
import requests
import time
import schedule
from datetime import datetime

# URL de tu aplicación (cambiar después del deployment)
APP_URL = "https://tu-app.onrender.com"  # Cambiar después de deployar

def ping_server():
    """Hace ping al servidor para mantenerlo activo"""
    try:
        response = requests.get(f"{APP_URL}/ping", timeout=10)
        if response.status_code == 200:
            print(f"✓ Ping exitoso - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"⚠ Ping falló con código {response.status_code}")
    except Exception as e:
        print(f"✗ Error en ping: {e}")

def keep_alive():
    """Ejecuta pings cada 14 minutos (servicios gratuitos duermen después de 15 min)"""
    print("🚀 Keep-Alive iniciado")
    print(f"📍 Monitoreando: {APP_URL}")
    print("=" * 50)
    
    # Programar ping cada 14 minutos
    schedule.every(14).minutes.do(ping_server)
    
    # Hacer ping inicial
    ping_server()
    
    # Loop infinito
    while True:
        schedule.run_pending()
        time.sleep(60)  # Verificar cada minuto

if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════╗
    ║   Keep-Alive Service                       ║
    ║   Mantiene tu app activa 24/7             ║
    ╚════════════════════════════════════════════╝
    
    INSTRUCCIONES:
    1. Después de deployar, actualiza APP_URL con tu URL real
    2. Ejecuta este script en tu computadora o en un servidor gratuito
    3. Déjalo corriendo para mantener el servicio activo
    
    ALTERNATIVA: Usa un servicio de cron job gratis:
    - cron-job.org
    - UptimeRobot.com (recomendado)
    - Kaffeine (para Heroku)
    
    """)
    
    keep_alive()
