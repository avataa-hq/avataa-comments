import os

# DATABASE
DB_TYPE = os.environ.get("DB_TYPE", "postgresql")
DB_USER = os.environ.get("DB_USER", "inventory_comments_admin")
DB_PASS = os.environ.get("DB_PASS", "")
DB_HOST = os.environ.get("DB_HOST", "pgbouncer")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "inventory_comments")

DATABASE_URL = f"{DB_TYPE}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# KEYCLOAK
KEYCLOAK_PROTOCOL = os.environ.get("KEYCLOAK_PROTOCOL", "http")
KEYCLOAK_HOST = os.environ.get("KEYCLOAK_HOST", "keycloak")
KEYCLOAK_PORT = os.environ.get("KEYCLOAK_PORT", "8080")
KEYCLOAK_REDIRECT_PROTOCOL = os.environ.get("KEYCLOAK_REDIRECT_PROTOCOL", None)
KEYCLOAK_REDIRECT_HOST = os.environ.get("KEYCLOAK_REDIRECT_HOST", None)
KEYCLOAK_REDIRECT_PORT = os.environ.get("KEYCLOAK_REDIRECT_PORT", None)
KEYCLOAK_REALM = os.environ.get("KEYCLOAK_REALM", "avataa")
KEYCLOAK_CLIENT_ID = os.environ.get("KEYCLOAK_CLIENT_ID")
KEYCLOAK_CLIENT_SECRET = os.environ.get("KEYCLOAK_CLIENT_SECRET", None)


if KEYCLOAK_REDIRECT_PROTOCOL is None:
    KEYCLOAK_REDIRECT_PROTOCOL = KEYCLOAK_PROTOCOL
if KEYCLOAK_REDIRECT_HOST is None:
    KEYCLOAK_REDIRECT_HOST = KEYCLOAK_HOST
if KEYCLOAK_REDIRECT_PORT is None:
    KEYCLOAK_REDIRECT_PORT = KEYCLOAK_PORT

KEYCLOAK_URL = f"{KEYCLOAK_PROTOCOL}://{KEYCLOAK_HOST}:{KEYCLOAK_PORT}"
KEYCLOAK_PUBLIC_KEY_URL = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}"
KEYCLOAK_REDIRECT_URL = f"{KEYCLOAK_REDIRECT_PROTOCOL}://{KEYCLOAK_REDIRECT_HOST}:{KEYCLOAK_REDIRECT_PORT}"
KEYCLOAK_TOKEN_URL = f"{KEYCLOAK_REDIRECT_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
KEYCLOAK_AUTHORIZATION_URL = f"{KEYCLOAK_REDIRECT_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/auth"

# OTHER
DEBUG = os.environ.get("DEBUG", "False").upper() in ("TRUE", "Y", "YES", "1")
UVICORN_WORKERS = os.environ.get("UVICORN_WORKERS", None)

# DOCUMENTATION
DOCS_ENABLED = os.environ.get("DOCS_ENABLED", "True").upper() in (
    "TRUE",
    "Y",
    "YES",
    "1",
)
DOCS_CUSTOM_ENABLED = os.environ.get(
    "DOCS_CUSTOM_ENABLED", "False"
).upper() in ("TRUE", "Y", "YES", "1")
SWAGGER_JS_URL = os.environ.get("DOCS_SWAGGER_JS_URL", None)
SWAGGER_CSS_URL = os.environ.get("DOCS_SWAGGER_CSS_URL", None)
REDOC_JS_URL = os.environ.get("DOCS_REDOC_JS_URL", None)
