import os

BACKEND_BASE_URL = os.environ["TA_BACKEND_BASE_URL"]

SESSION_TTL_HOURS = 10
DATABASE_DSN = os.environ["TA_DATABASE_DSN"]

AUTO_RELOAD = bool(os.environ.get("TA_AUTO_RELOAD"))

PROMETHEUS_NAME_PREFIX = os.environ.get("TA_PROMETHEUS_NAME_PREFIX")
PROMETHEUS_PORT = int(os.environ.get("TA_PROMETHEUS_PORT", 9100))

SENTRY_DSN = os.environ["TA_SENTRY_DSN"]
ENVIRONMENT = os.environ.get("TA_ENVIRONMENT", "unknown")

STATIC_DIR = os.path.join("/app", "taskapp", "static")

APP_NAME = os.environ.get("TA_APP_NAME")
