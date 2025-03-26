import multiprocessing
import os

# Configuración básica
bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
keepalive = 5

# Configuración de logging
accesslog = "/public_html/api/logs/access.log"
errorlog = "/public_html/api/logs/error.log"
loglevel = "info"

# Configuración de procesos
daemon = True
pidfile = "/public_html/api/gunicorn.pid"
user = "u547715306"
group = "u547715306"

# Configuración de SSL
keyfile = "/etc/letsencrypt/live/radhikatmosphere.com/privkey.pem"
certfile = "/etc/letsencrypt/live/radhikatmosphere.com/fullchain.pem"

# Configuración de seguridad
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190 