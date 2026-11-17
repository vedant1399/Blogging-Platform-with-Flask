"""Gunicorn Production Server Configuration."""
import os
import multiprocessing

# Network binding
bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:5000')

# Worker processes & concurrency
workers = int(os.environ.get('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
threads = int(os.environ.get('GUNICORN_THREADS', 2))
worker_class = 'sync'

# Timeout & connection handling
timeout = int(os.environ.get('GUNICORN_TIMEOUT', 60))
keepalive = int(os.environ.get('GUNICORN_KEEPALIVE', 5))

# Logging to standard output for container compatibility
accesslog = '-'
errorlog = '-'
loglevel = os.environ.get('GUNICORN_LOG_LEVEL', 'info')

# Process naming
proc_name = 'blogging_platform_flask'
