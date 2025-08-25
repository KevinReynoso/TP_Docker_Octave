# 📊 Contador de Visitas con Flask + Redis

## 📋 Descripción
Aplicación web que cuenta visitas usando Flask como frontend y Redis como base de datos. Todo en un solo contenedor Docker.

## 💡 Warning
Las siguientes `warnings` son para crear el `dockerfile`
 * Se recomienda empezar desde la siguiente imagen: `python:3.9-slim`
 * No olvidar copiar los files dentro del docker
 * No olvidar instalar las dependencias durante el building del `docker image`
````bash
# Ejecutar el comando
apt-get update && apt-get install -y \
    redis-server \
    && rm -rf /var/lib/apt/lists/*

# Este comando tambien es necesario
pip install --no-cache-dir -r requirements.txt
````
 * Se tiene que exponer el `port` 5000. Podes hacerlo usando
````bash
# Exponer  el puerto 5000
EXPOSE 5000
````
 * Se tiene que dar permiso de ejecucion la fichero `start.sh`
````bash
# Asignar permiso de ejecución
chmod +x start.sh
````
 * Es fundamental que se ejecute el comando `CMD` al runnear la `docker image`
````bash
# Ejecutar el proyecto
./start.sh
````

## 🚀 Actividades
Deben hacer el `DOCKER_SETUP.md` teniendo las siguientes consideraciones
* ¿Qué pasa si corremos la `docker image` sin asignar ninguna flag a `docker run`? ¿Podemos usar la misma terminal para correr otros comandos?
** La respuesta es no, ya que la ejecución de la instancia de la imagen se realiza en la misma terminal. Para evitar esto, se debe añadir el flag -d para que la ejecución se realice en segundo plano.
 * El proyecto usa el usa el port `5000`. Intentar hacer `docker run` con y sin el parametro correspondiente. ¿Qué ocurre en cada caso?
 * Ejecutar `docker stop <container>`. ¿Qué pasa si al hacer `docker run` no le asigno un nombre al contenedor? ¿Qué debo poner en `<container>`para poder hacer `docker stop <container>`?
 * Si corro el contenedor en segundo plano, no veo información de la dirección IP que necesito para usar mi proyecto. Documentar qué se debe poner en el navegador
