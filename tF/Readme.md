# Readme
# Aplicación de Organización de Partidos de Fútbol

Esta aplicación permite a los usuarios organizar y gestionar partidos de fútbol, incluyendo la creación de eventos, la inscripción de jugadores y la edición de eventos. Está construida con Flask y utiliza MySQL como base de datos.

## Características
- Registro y autenticación de usuarios
- Creación de partidos de fútbol
- Inscripción de jugadores en partidos
- Edición y cancelación de partidos
- Gestión de usuarios y contraseñas hasheadas

## Tecnologías Utilizadas
- Python
- Flask
- Flask-SQLAlchemy
- MySQL
- Docker (opcional para despliegue)


## Instalación

### Requisitos Previos
- Python 3.8+
- MySQL
- pip
- virtualenv

### Clonar el Repositorio
```sh
git clone https://github.com/tu-usuario/futbol-app.git
cd futbol-app



## Despliegue

### Despliegue con Docker
1. Construir la imagen Docker:
    ```sh
    docker build -t futbol-app .
    ```

2. Ejecutar el contenedor:
    ```sh
    docker run -d -p 8000:8000 futbol-app
    ```

### Despliegue en AWS EC2
1. Lanza una instancia EC2 y conéctate a ella.
2. Instala Docker en la instancia:
    ```sh
    sudo yum update -y
    sudo yum install docker -y
    sudo systemctl start docker
    sudo systemctl enable docker
    ```

3. Copia tu archivo `.pem` a la instancia y configura SSH.
4. Pulla la imagen Docker y ejecuta el contenedor en la instancia:
    ```sh
    docker pull tu-usuario-dockerhub/futbol-app:latest
    docker run -d -p 8000:8000 tu-usuario-dockerhub/futbol-app:latest
    ```

5. (Opcional) Configura Nginx como proxy inverso para la aplicación.
