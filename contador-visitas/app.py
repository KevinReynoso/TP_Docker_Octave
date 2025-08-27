from flask import Flask

from splitio import get_factory
from splitio.exceptions import TimeoutException

import redis
import time
import os

import sys
import logging

app = Flask(__name__)

# se descargan y se obtienen las reglas y configuraciones de todos los feature flags definidos
factory = get_factory('8njq4vpuuor0al7nk0t9tek77cr4d05crqs1')
try:
    factory.block_until_ready(5)
except TimeoutException:
    # The SDK failed to initialize in 5 seconds. Abort!
    sys.exit()

# crea y devuelve una instancia del cliente del SDK
split = factory.client()


def wait_for_redis():
    """Esperar a que Redis esté disponible"""
    max_retries = 10
    retry_delay = 1
    
    for i in range(max_retries):
        try:
            redis_client = redis.Redis(host='localhost', port=6379, db=0)
            redis_client.ping()
            print("✅ Redis conectado exitosamente")
            return redis_client
        except redis.ConnectionError:
            print(f"⏳ Esperando por Redis... ({i+1}/{max_retries})")
            time.sleep(retry_delay)
    
    raise Exception("❌ No se pudo conectar a Redis")

@app.route('/')
def contador_visitas():
    try:
        redis_client = wait_for_redis()
        visitas = redis_client.incr('visitas')

        # realiza la consulta respecto al treatment en el feature flag especificado y al id del cliente
        treatment = split.get_treatment(visitas, # unique identifier for your user
                                'test_split')
        if treatment == 'on':
        # insert on code here
            return f'''
            <html>
               <body style="font-family: Arial; text-align: center; padding: 50px;">
                  <h1>📊 Contador de Visitas</h1>
                  <p style="font-size: 24px;">¡Número de visitas: <strong>{visitas}</strong>! 🎉</p>
                  <p>✅ Redis funcionando correctamente</p>
                  <a href="/reiniciar">🔄 Reiniciar contador</a> | 
                   <a href="/health">❤️ Health check</a>
             </body>
            </html>
           '''
        elif treatment == 'off':
            return f'''
            <html>
               <body style="font-family: Arial; text-align: center; padding: 50px;">
                  <h1>No tiene acceso. Lo sentimos.</h1>
             </body>
            </html>
           '''
        else:
            # insert control code here
            pass
    except Exception as e:
        return f'❌ Error: {str(e)}'

@app.route('/reiniciar')
def reiniciar_contador():
    try:
        redis_client = wait_for_redis()
        redis_client.set('visitas', 0)
        return '✅ ¡Contador reiniciado! <a href="/">Volver</a>'
    except Exception as e:
        return f'❌ Error: {str(e)}'

@app.route('/health')
def health_check():
    try:
        redis_client = wait_for_redis()
        redis_client.ping()
        return '✅ Health check: Todo funciona correctamente (Flask + Redis)'
    except Exception as e:
        return f'❌ Health check failed: {str(e)}'

if __name__ == '__main__':
    print("🚀 Iniciando aplicación Flask + Redis...")
    app.run(host='0.0.0.0', port=5000)