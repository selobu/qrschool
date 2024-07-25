from os import getenv

workers = int(getenv("GUNICORN_PROCESSES", "2"))

threads = int(getenv("GUNICORN_THREADS", "4"))

timeout = int(getenv("GUNICORN_TIMEOUT", "120"))

port = int(getenv("SERVING_PORT", "8080"))

bind = getenv("GUNICORN_BIND", f"0.0.0.0:{port}")

forwarded_allow_ips = "*"

secure_scheme_headers = {"X-Forwarded-Proto": "https"}
