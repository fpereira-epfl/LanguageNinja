# gunicorn.conf.py
import os
bind = f"0.0.0.0:{os.getenv('PORT', '8080')}"   # Cloud Run injects PORT
workers = 2
worker_class = "uvicorn.workers.UvicornWorker"
