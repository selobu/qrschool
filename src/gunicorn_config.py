from os import environ

workers = int(environ.get("GUNICORN_PROCESSES", "2"))

threads = int(environ.get("GUNICORN_THREADS", "4"))

timeout = int(environ.get("GUNICORN_TIMEOUT", "120"))

port = int(environ.get("SERVING_PORT", "8080"))

bind = environ.get("GUNICORN_BIND", f"0.0.0.0:{port}")

forwarded_allow_ips = "*"

secure_scheme_headers = {"X-Forwarded-Proto": "https"}
