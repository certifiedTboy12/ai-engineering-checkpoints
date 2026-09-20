# Docker Checkpoint: Containers, Images, Volumes, Networking & Docker Compose

## Overview

This checkpoint demonstrates the fundamental Docker concepts required to manage containers, build custom images, persist data, create container networks, and manage multi-container applications with Docker Compose.

### Objectives

By completing this checkpoint, you will demonstrate the ability to:

- Use basic Docker CLI commands.
- Pull and run Docker images.
- Create custom Docker images using Dockerfiles.
- Build and run Python applications inside Docker containers.
- Persist data using Docker volumes.
- Create custom Docker networks.
- Enable container-to-container communication.
- Configure a Flask backend and Nginx reverse proxy.
- Define multi-container applications using Docker Compose.
- Inspect containers, images, networks, volumes, and logs.
- Reproduce the entire environment from scratch.

---

# 1. Prerequisites

Install Docker Desktop.

Verify that Docker is installed:

```bash
docker --version
docker compose version
```

Example output:

```text
Docker version 28.x.x
Docker Compose version v2.x.x
```

Verify that Docker is running:

```bash
docker info
```

---

# 2. Project Structure

Create the following project structure:

```text
docker-checkpoint/
│
├── python-app/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
│
└── compose/
    ├── docker-compose.yml
    │
    ├── backend/
    │   ├── Dockerfile
    │   ├── app.py
    │   └── requirements.txt
    │
    └── nginx/
        └── nginx.conf
```

---

# Part 1: Docker Basics & CLI

## 3. Pull the Official Nginx Image

Pull the official Nginx image from Docker Hub:

```bash
docker pull nginx
```

Verify that the image was downloaded:

```bash
docker images
```

You should see an entry similar to:

```text
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
nginx        latest    xxxxxxxx       ...           ...
```

---

## 4. Run Nginx in Detached Mode

Run an Nginx container:

```bash
docker run -d --name my-nginx -p 8080:80 nginx
```

### Explanation

```text
-d
```

Runs the container in detached/background mode.

```text
--name my-nginx
```

Assigns the container the name `my-nginx`.

```text
-p 8080:80
```

Maps:

```text
Host port 8080 → Container port 80
```

Check the running container:

```bash
docker ps
```

You should see:

```text
CONTAINER ID   IMAGE   PORTS
xxxxxxxx       nginx   0.0.0.0:8080->80/tcp
```

Open the following URL in a browser:

```text
http://localhost:8080
```

You should see the Nginx welcome page.

---

# 5. Use `docker exec`

Enter the running Nginx container:

```bash
docker exec -it my-nginx /bin/bash
```

Navigate to the Nginx HTML directory:

```bash
cd /usr/share/nginx/html
```

List the files:

```bash
ls -la
```

You should see files similar to:

```text
50x.html
index.html
```

Display the default Nginx page:

```bash
cat index.html
```

Exit the container:

```bash
exit
```

You can also run a command inside the container without opening an interactive shell:

```bash
docker exec my-nginx ls -la /usr/share/nginx/html
```

---

# 6. Restart the Nginx Container

Stop the container:

```bash
docker stop my-nginx
```

Restart it:

```bash
docker start my-nginx
```

Check the container:

```bash
docker ps
```

Open:

```text
http://localhost:8080
```

The Nginx server should still work.

You can also restart it directly:

```bash
docker restart my-nginx
```

Inspect the container:

```bash
docker inspect my-nginx
```

---

# 7. Remove the Nginx Container and Image

Stop the container:

```bash
docker stop my-nginx
```

Remove the container:

```bash
docker rm my-nginx
```

Verify:

```bash
docker ps -a
```

Remove the image:

```bash
docker rmi nginx
```

Verify:

```bash
docker images
```

---

# Part 2: Docker Images & Dockerfiles

# 8. Create the Python Application

Create the directory:

```bash
mkdir python-app
```

Move into it:

```bash
cd python-app
```

Create:

```text
app.py
```

Add the following code:

```python
from http.server import BaseHTTPRequestHandler, HTTPServer


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        message = b"Hello from my custom Docker Python application!"

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(message)))
        self.end_headers()

        self.wfile.write(message)

    def log_message(self, format, *args):
        return


server = HTTPServer(("0.0.0.0", 8000), RequestHandler)

print("Python application running on port 8000")

server.serve_forever()
```

---

# 9. Create `requirements.txt`

Create:

```text
requirements.txt
```

For this application, no external Python dependencies are required.

Therefore, the file can be empty.

---

# 10. Create the Python Dockerfile

Create:

```text
Dockerfile
```

Add:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8000

CMD ["python", "app.py"]
```

## Dockerfile Explanation

### Base image

```dockerfile
FROM python:3.12-slim
```

Uses Python 3.12 Slim as the base image.

### Working directory

```dockerfile
WORKDIR /app
```

Sets `/app` as the working directory inside the container.

### Copy dependencies

```dockerfile
COPY requirements.txt .
```

Copies the local `requirements.txt` file into the container.

### Install dependencies

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

Installs the dependencies listed in `requirements.txt`.

### Copy application

```dockerfile
COPY app.py .
```

Copies `app.py` into the image.

### Expose application port

```dockerfile
EXPOSE 8000
```

Documents that the application listens on port `8000`.

### Default command

```dockerfile
CMD ["python", "app.py"]
```

Starts the Python application when the container runs.

---

# 11. Build the Custom Docker Image

Make sure you are inside:

```text
docker-checkpoint/python-app
```

Run:

```bash
docker build -t my-python-app:v1 .
```

Verify the image:

```bash
docker images
```

You should see:

```text
REPOSITORY       TAG
my-python-app    v1
```

---

# 12. Run the Custom Python Image

Run the container:

```bash
docker run -d \
  --name my-python-container \
  -p 8000:8000 \
  my-python-app:v1
```

On Windows PowerShell, you can also use:

```powershell
docker run -d --name my-python-container -p 8000:8000 my-python-app:v1
```

Check the container:

```bash
docker ps
```

Test the application in a browser:

```text
http://localhost:8000
```

Expected response:

```text
Hello from my custom Docker Python application!
```

---

# 13. Check Application Logs

Run:

```bash
docker logs my-python-container
```

Expected:

```text
Python application running on port 8000
```

Follow the logs:

```bash
docker logs -f my-python-container
```

Press:

```text
CTRL + C
```

to stop following the logs.

---

# 14. Inspect Docker Image Layers

Run:

```bash
docker history my-python-app:v1
```

This displays the layers created by the Dockerfile.

You can also inspect the image:

```bash
docker inspect my-python-app:v1
```

---

# Part 3: Docker Volumes & Storage

# 15. Create a MySQL Volume

Create a named Docker volume:

```bash
docker volume create mysql-data
```

Verify:

```bash
docker volume ls
```

Inspect the volume:

```bash
docker volume inspect mysql-data
```

---

# 16. Run MySQL With a Volume

Run MySQL:

```bash
docker run -d \
  --name mysql-db \
  -e MYSQL_ROOT_PASSWORD=rootpassword \
  -e MYSQL_DATABASE=checkpointdb \
  -v mysql-data:/var/lib/mysql \
  -p 3306:3306 \
  mysql:8.4
```

### Important options

```text
-e MYSQL_ROOT_PASSWORD=rootpassword
```

Sets the MySQL root password.

```text
-e MYSQL_DATABASE=checkpointdb
```

Creates the `checkpointdb` database.

```text
-v mysql-data:/var/lib/mysql
```

Mounts the Docker volume into MySQL's data directory.

```text
-p 3306:3306
```

Maps the host's port 3306 to MySQL's container port 3306.

Check:

```bash
docker ps
```

---

# 17. Check MySQL Logs

Run:

```bash
docker logs mysql-db
```

Wait until MySQL is ready.

You can test it with:

```bash
docker exec mysql-db mysqladmin ping \
  -uroot \
  -prootpassword
```

Expected:

```text
mysqld is alive
```

---

# 18. Connect to MySQL

Run:

```bash
docker exec -it mysql-db mysql -uroot -prootpassword
```

Select the database:

```sql
USE checkpointdb;
```

---

# 19. Create a Table

Run:

```sql
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL
);
```

Verify the table:

```sql
SHOW TABLES;
```

---

# 20. Insert Data

Run:

```sql
INSERT INTO students (name, email)
VALUES
('John Doe', 'john@example.com'),
('Jane Doe', 'jane@example.com');
```

View the data:

```sql
SELECT * FROM students;
```

Expected:

```text
+----+----------+------------------+
| id | name     | email            |
+----+----------+------------------+
|  1 | John Doe | john@example.com |
|  2 | Jane Doe | jane@example.com |
+----+----------+------------------+
```

Exit MySQL:

```sql
EXIT;
```

---

# 21. Stop and Remove the MySQL Container

Stop the container:

```bash
docker stop mysql-db
```

Remove it:

```bash
docker rm mysql-db
```

Verify:

```bash
docker ps -a
```

The container should no longer exist.

---

# 22. Create a New MySQL Container Using the Same Volume

Run:

```bash
docker run -d \
  --name mysql-db-new \
  -e MYSQL_ROOT_PASSWORD=rootpassword \
  -e MYSQL_DATABASE=checkpointdb \
  -v mysql-data:/var/lib/mysql \
  -p 3306:3306 \
  mysql:8.4
```

Wait for MySQL:

```bash
docker exec mysql-db-new mysqladmin ping \
  -uroot \
  -prootpassword
```

Connect:

```bash
docker exec -it mysql-db-new mysql -uroot -prootpassword
```

Run:

```sql
USE checkpointdb;

SELECT * FROM students;
```

The previously created records should still exist.

This demonstrates Docker volume persistence.

```text
MySQL Container 1
       |
       v
mysql-data volume
       |
       v
MySQL Container 2
```

The container was deleted, but the volume remained.

---

# Part 4: Docker Networking

# 23. Create a Custom Network

Create:

```bash
docker network create internal-net
```

Verify:

```bash
docker network ls
```

Inspect:

```bash
docker network inspect internal-net
```

---

# 24. Create Two Containers

Create the first Alpine container:

```bash
docker run -dit \
  --name server-one \
  --network internal-net \
  alpine
```

Create the second:

```bash
docker run -dit \
  --name server-two \
  --network internal-net \
  alpine
```

Check:

```bash
docker ps
```

---

# 25. Test Container-to-Container Communication

Enter `server-one`:

```bash
docker exec -it server-one sh
```

Install ping:

```bash
apk add --no-cache iputils
```

Ping the second container:

```bash
ping -c 4 server-two
```

Docker's internal DNS resolves:

```text
server-two
```

to the IP address of the second container.

Exit:

```bash
exit
```

---

# 26. Test HTTP Communication

Remove the previous containers:

```bash
docker rm -f server-one server-two
```

Create a Python web server:

```bash
docker run -dit \
  --name web-server \
  --network internal-net \
  python:3.12-slim
```

Start an HTTP server:

```bash
docker exec -d web-server \
  python -m http.server 8000 --bind 0.0.0.0
```

Create a client:

```bash
docker run -dit \
  --name client \
  --network internal-net \
  alpine
```

Enter the client:

```bash
docker exec -it client sh
```

Install curl:

```bash
apk add --no-cache curl
```

Send a request to the web server:

```bash
curl http://web-server:8000
```

The request works because Docker's internal DNS resolves:

```text
web-server
```

to the correct container.

Exit:

```bash
exit
```

Clean up:

```bash
docker rm -f client web-server
```

Remove the network:

```bash
docker network rm internal-net
```

---

# Part 5: Docker Compose

## 27. Compose Architecture

The Compose application will contain two services:

```text
                 Browser
                    |
                    |
              localhost:8080
                    |
                    v
             +-------------+
             |    Nginx    |
             | Reverse     |
             | Proxy       |
             +-------------+
                    |
                    |
              app-network
                    |
                    v
             +-------------+
             |   Flask     |
             |  Backend    |
             +-------------+
```

Nginx receives requests from the browser and forwards them to the Flask backend.

---

# 28. Create the Compose Directory

From the project root:

```bash
mkdir compose
cd compose
```

Create:

```text
backend/
nginx/
```

The structure should be:

```text
compose/
│
├── docker-compose.yml
│
├── backend/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
│
└── nginx/
    └── nginx.conf
```

---

# 29. Flask Backend

Create:

```text
backend/app.py
```

Add:

```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello from the Flask backend running inside Docker!"


@app.route("/health")
def health():
    return {
        "status": "healthy",
        "service": "flask-backend"
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

---

# 30. Flask Requirements

Create:

```text
backend/requirements.txt
```

Add:

```text
Flask==3.1.2
```

---

# 31. Backend Dockerfile

Create:

```text
backend/Dockerfile
```

Add:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

---

# 32. Nginx Configuration

Create:

```text
nginx/nginx.conf
```

Add:

```nginx
server {
    listen 80;

    location / {
        proxy_pass http://backend:5000;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

The following line is important:

```nginx
proxy_pass http://backend:5000;
```

`backend` is the Docker Compose service name.

Docker's internal DNS allows Nginx to resolve the backend service using its name.

---

# 33. Complete `docker-compose.yml`

Create:

```text
docker-compose.yml
```

Add the following:

```yaml
services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: flask-backend
    restart: unless-stopped
    environment:
      FLASK_ENV: production
    expose:
      - "5000"
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    container_name: nginx-proxy
    restart: unless-stopped
    ports:
      - "8080:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - backend
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

---

# 34. Docker Compose Configuration Explanation

## Backend Service

```yaml
backend:
```

Defines the Flask backend service.

```yaml
build:
  context: ./backend
  dockerfile: Dockerfile
```

Tells Docker Compose to build the backend image using:

```text
backend/Dockerfile
```

---

## Container Name

```yaml
container_name: flask-backend
```

Assigns the container a fixed name.

---

## Environment Variable

```yaml
environment:
  FLASK_ENV: production
```

Sets the Flask environment.

---

## Expose Port

```yaml
expose:
  - "5000"
```

Makes port 5000 available to other containers on the Docker network.

It does not publish port 5000 directly to the host.

---

# 35. Nginx Service

```yaml
nginx:
  image: nginx:alpine
```

Uses the official lightweight Nginx image.

---

## Port Mapping

```yaml
ports:
  - "8080:80"
```

Maps:

```text
Host port 8080
      ↓
Nginx port 80
```

Therefore the application is available at:

```text
http://localhost:8080
```

---

## Configuration Volume

```yaml
volumes:
  - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
```

Maps the local Nginx configuration to the configuration file inside the container.

The `ro` means read-only.

---

## Dependency

```yaml
depends_on:
  - backend
```

Tells Compose to start the backend service before starting Nginx.

---

# 36. Shared Network

Both services use:

```yaml
networks:
  - app-network
```

Therefore:

```text
Nginx
   |
   | app-network
   |
Flask Backend
```

Nginx can communicate with Flask using:

```text
backend:5000
```

---

# 37. Build and Start the Compose Application

Move into the Compose directory:

```bash
cd compose
```

Build and start:

```bash
docker compose up -d --build
```

The `-d` option runs the services in detached mode.

The `--build` option forces Docker to build the backend image.

---

# 38. Check Compose Services

Run:

```bash
docker compose ps
```

Expected:

```text
NAME             SERVICE    STATUS
flask-backend    backend    Up
nginx-proxy      nginx      Up
```

---

# 39. View Compose Logs

View all logs:

```bash
docker compose logs
```

Follow the logs:

```bash
docker compose logs -f
```

View only backend logs:

```bash
docker compose logs backend
```

View only Nginx logs:

```bash
docker compose logs nginx
```

---

# 40. Test the Application

Open:

```text
http://localhost:8080
```

Expected:

```text
Hello from the Flask backend running inside Docker!
```

Test the health endpoint:

```text
http://localhost:8080/health
```

Expected:

```json
{
  "service": "flask-backend",
  "status": "healthy"
}
```

---

# 41. Test Using Curl

Test the application:

```bash
curl http://localhost:8080
```

Expected:

```text
Hello from the Flask backend running inside Docker!
```

Test the health endpoint:

```bash
curl http://localhost:8080/health
```

Expected:

```json
{
  "service": "flask-backend",
  "status": "healthy"
}
```

---

# 42. Test Internal Container Communication

Enter the Nginx container:

```bash
docker exec -it nginx-proxy sh
```

Install curl:

```bash
apk add --no-cache curl
```

Call the Flask backend directly:

```bash
curl http://backend:5000
```

Expected:

```text
Hello from the Flask backend running inside Docker!
```

Test the health endpoint:

```bash
curl http://backend:5000/health
```

Expected:

```json
{
  "service": "flask-backend",
  "status": "healthy"
}
```

Exit:

```bash
exit
```

---

# 43. Inspect the Docker Network

List Docker networks:

```bash
docker network ls
```

Find the Compose network:

```bash
docker network ls
```

Inspect it:

```bash
docker network inspect compose_app-network
```

The exact network name may vary depending on the Compose project name.

You should find both:

```text
flask-backend
nginx-proxy
```

attached to the same network.

---

# 44. Execute Commands Through Docker Compose

Open a shell in the backend:

```bash
docker compose exec backend sh
```

Exit:

```bash
exit
```

Open a shell in Nginx:

```bash
docker compose exec nginx sh
```

Exit:

```bash
exit
```

---

# 45. Stop the Compose Application

Stop and remove the containers:

```bash
docker compose down
```

This removes:

- Containers
- Compose network

It does not normally remove the images.

---

# 46. Rebuild the Compose Application

To rebuild the application:

```bash
docker compose build
```

Start it:

```bash
docker compose up -d
```

Or perform both operations:

```bash
docker compose up -d --build
```

---

# 47. Remove Compose Images

If you want to remove locally built images:

```bash
docker compose down --rmi local
```

---

# 48. Environment Variables

For the MySQL example, the following environment variables were used:

```text
MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_DATABASE=checkpointdb
```

For a real project, passwords should not be hard-coded in source control.

A `.env` file can be used instead.

Create:

```text
.env
```

Example:

```env
MYSQL_ROOT_PASSWORD=your_secure_password
MYSQL_DATABASE=checkpointdb
```

Then a Compose service can use:

```yaml
environment:
  MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
  MYSQL_DATABASE: ${MYSQL_DATABASE}
```

Do not commit sensitive `.env` files to a public Git repository.

---

# 49. Docker Image Repositories

The project uses official Docker Hub images:

| Image              | Repository                       |
| ------------------ | -------------------------------- |
| `nginx`            | Docker Hub official Nginx image  |
| `nginx:alpine`     | Docker Hub official Nginx image  |
| `python:3.12-slim` | Docker Hub official Python image |
| `mysql:8.4`        | Docker Hub official MySQL image  |

The custom Python image:

```text
my-python-app:v1
```

is built locally.

The Flask backend image is also built locally by Docker Compose.

---

# 50. Optional: Push the Custom Image to Docker Hub

Log in:

```bash
docker login
```

Tag the image:

```bash
docker tag my-python-app:v1 YOUR_DOCKERHUB_USERNAME/my-python-app:v1
```

Push:

```bash
docker push YOUR_DOCKERHUB_USERNAME/my-python-app:v1
```

Verify the image:

```bash
docker images
```

The image can then be pulled from another computer:

```bash
docker pull YOUR_DOCKERHUB_USERNAME/my-python-app:v1
```

---

# 51. Useful Docker CLI Commands

## Images

```bash
docker images
docker pull IMAGE
docker build -t IMAGE:TAG .
docker rmi IMAGE
docker history IMAGE
docker inspect IMAGE
```

## Containers

```bash
docker ps
docker ps -a
docker run IMAGE
docker start CONTAINER
docker stop CONTAINER
docker restart CONTAINER
docker rm CONTAINER
docker rm -f CONTAINER
docker logs CONTAINER
docker logs -f CONTAINER
docker exec -it CONTAINER sh
docker inspect CONTAINER
```

## Volumes

```bash
docker volume ls
docker volume create VOLUME
docker volume inspect VOLUME
docker volume rm VOLUME
```

## Networks

```bash
docker network ls
docker network create NETWORK
docker network inspect NETWORK
docker network rm NETWORK
```

## Docker Compose

```bash
docker compose up
docker compose up -d
docker compose up -d --build
docker compose ps
docker compose logs
docker compose logs -f
docker compose logs backend
docker compose logs nginx
docker compose exec backend sh
docker compose exec nginx sh
docker compose restart
docker compose down
docker compose build
```

---

# 52. Complete Reproduction From Scratch

The following commands summarize the complete process.

## Verify Docker

```bash
docker --version
docker compose version
docker info
```

## Nginx

```bash
docker pull nginx

docker run -d \
  --name my-nginx \
  -p 8080:80 \
  nginx

docker ps

docker exec -it my-nginx /bin/bash

cd /usr/share/nginx/html

ls -la

cat index.html

exit

docker restart my-nginx

docker stop my-nginx
docker rm my-nginx
docker rmi nginx
```

---

# 53. Build the Python Application

From:

```text
docker-checkpoint/python-app
```

Run:

```bash
docker build -t my-python-app:v1 .
```

Run:

```bash
docker run -d \
  --name my-python-container \
  -p 8000:8000 \
  my-python-app:v1
```

Test:

```bash
curl http://localhost:8000
```

Inspect:

```bash
docker history my-python-app:v1
```

---

# 54. MySQL Volume

Create the volume:

```bash
docker volume create mysql-data
```

Start MySQL:

```bash
docker run -d \
  --name mysql-db \
  -e MYSQL_ROOT_PASSWORD=rootpassword \
  -e MYSQL_DATABASE=checkpointdb \
  -v mysql-data:/var/lib/mysql \
  -p 3306:3306 \
  mysql:8.4
```

Connect:

```bash
docker exec -it mysql-db mysql -uroot -prootpassword
```

Create the table:

```sql
USE checkpointdb;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL
);

INSERT INTO students (name, email)
VALUES
('John Doe', 'john@example.com'),
('Jane Doe', 'jane@example.com');

SELECT * FROM students;

EXIT;
```

Remove the container:

```bash
docker stop mysql-db
docker rm mysql-db
```

Create another container with the same volume:

```bash
docker run -d \
  --name mysql-db-new \
  -e MYSQL_ROOT_PASSWORD=rootpassword \
  -e MYSQL_DATABASE=checkpointdb \
  -v mysql-data:/var/lib/mysql \
  -p 3306:3306 \
  mysql:8.4
```

Verify:

```bash
docker exec -it mysql-db-new mysql -uroot -prootpassword
```

Then:

```sql
USE checkpointdb;

SELECT * FROM students;

EXIT;
```

---

# 55. Docker Networking

Create:

```bash
docker network create internal-net
```

Create a web server:

```bash
docker run -dit \
  --name web-server \
  --network internal-net \
  python:3.12-slim
```

Start the HTTP server:

```bash
docker exec -d web-server \
  python -m http.server 8000 --bind 0.0.0.0
```

Create a client:

```bash
docker run -dit \
  --name client \
  --network internal-net \
  alpine
```

Enter:

```bash
docker exec -it client sh
```

Install curl:

```bash
apk add --no-cache curl
```

Test:

```bash
curl http://web-server:8000
```

Exit:

```bash
exit
```

Clean up:

```bash
docker rm -f client web-server
docker network rm internal-net
```

---

# 56. Docker Compose

Move to:

```text
docker-checkpoint/compose
```

Build and start:

```bash
docker compose up -d --build
```

Check:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs
```

Test:

```bash
curl http://localhost:8080
```

Expected:

```text
Hello from the Flask backend running inside Docker!
```

Test:

```bash
curl http://localhost:8080/health
```

Expected:

```json
{
  "service": "flask-backend",
  "status": "healthy"
}
```

Stop:

```bash
docker compose down
```

---

# 57. Final Verification Checklist

## Docker Basics

- [ ] Docker installed and running.
- [ ] Nginx image pulled.
- [ ] Nginx container created.
- [ ] Port `8080` mapped to container port `80`.
- [ ] Nginx accessed through the browser.
- [ ] `docker exec` used to inspect `/usr/share/nginx/html`.
- [ ] Container restarted successfully.
- [ ] Nginx container removed.
- [ ] Nginx image removed.

## Dockerfiles

- [ ] `python:3.12-slim` used as the base image.
- [ ] `app.py` copied into the image.
- [ ] `requirements.txt` copied into the image.
- [ ] Dependencies installed.
- [ ] Default command configured.
- [ ] Image built as `my-python-app:v1`.
- [ ] Python container started.
- [ ] Application tested.
- [ ] `docker history` used.

## Docker Volumes

- [ ] `mysql-data` volume created.
- [ ] MySQL container started.
- [ ] Database created.
- [ ] Table created.
- [ ] Data inserted.
- [ ] MySQL container stopped.
- [ ] MySQL container removed.
- [ ] New MySQL container created using the same volume.
- [ ] Original data confirmed.

## Docker Networking

- [ ] `internal-net` created.
- [ ] Multiple containers attached.
- [ ] Container-to-container communication tested.
- [ ] Containers accessed by name.
- [ ] HTTP communication tested with `curl`.

## Docker Compose

- [ ] Flask backend created.
- [ ] Backend Dockerfile created.
- [ ] Nginx configuration created.
- [ ] Complete `docker-compose.yml` created.
- [ ] Shared Docker network configured.
- [ ] Backend and Nginx started.
- [ ] `docker compose ps` tested.
- [ ] `docker compose logs` tested.
- [ ] Application accessed through Nginx.
- [ ] Backend accessed internally through the Docker network.
- [ ] Compose stack successfully stopped with `docker compose down`.

---

# 58. Final Architecture

The completed environment contains the following components:

```text
                         HOST MACHINE
                              |
            +-----------------+------------------+
            |                                    |
            |                                    |
       localhost:8000                       localhost:8080
            |                                    |
            v                                    v
   +------------------+                 +----------------+
   | Python Container |                 |     Nginx      |
   | my-python-app:v1 |                 | Reverse Proxy  |
   +------------------+                 +-------+--------+
                                                |
                                                |
                                          app-network
                                                |
                                                v
                                        +---------------+
                                        | Flask Backend |
                                        |    :5000      |
                                        +---------------+


                     MySQL Persistence

                  +----------------+
                  | MySQL Container|
                  +-------+--------+
                          |
                          |
                   mysql-data
                     Volume
                          |
                          v
                  Persistent Data


                     Docker Network

                  internal-net
                       |
             +---------+---------+
             |                   |
             v                   v
        web-server            client
             |                   |
             +-------------------+
                  HTTP/curl
```

---

# 59. Conclusion

This checkpoint demonstrates the core Docker workflow:

```text
Docker Image
     |
     | docker run
     v
Container
     |
     +---- docker exec
     |
     +---- docker logs
     |
     +---- docker restart
     |
     +---- docker stop
     |
     +---- docker rm


Container
     |
     | mounted volume
     v
Persistent Storage


Container
     |
     | custom network
     v
Container-to-Container Communication


Docker Compose
     |
     +---- Flask Backend
     |
     +---- Nginx Reverse Proxy
     |
     +---- Shared Network
```

The resulting environment can be reproduced from the provided Dockerfiles, Python application files, Nginx configuration, `docker-compose.yml`, environment variables, and Docker CLI commands.
