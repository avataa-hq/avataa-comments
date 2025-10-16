## Inventory Comments

## Environment variables

```toml
DB_HOST=pgbouncer
DB_NAME=inventory_comments
DB_PASS=27j6mbN0pgJGDxBO
DB_PORT=5432
DB_TYPE=postgresql
DB_USER=comments_admin
DOCS_CUSTOM_ENABLED=True
DOCS_REDOC_JS_URL=https://redoc.avataa.dev/redoc.standalone.js
DOCS_SWAGGER_CSS_URL=https://swagger-ui.avataa.dev/swagger-ui.css
DOCS_SWAGGER_JS_URL=https://swagger-ui.avataa.dev/swagger-ui-bundle.js
KEYCLOAK_CLIENT_ID=inventory-comments
KEYCLOAK_CLIENT_SECRET=Lx9258P3y6THU11VqGvZdgPbfybJsPZi
KEYCLOAK_HOST=keycloak
KEYCLOAK_PORT=8080
KEYCLOAK_PROTOCOL=http
KEYCLOAK_REALM=avataa
KEYCLOAK_REDIRECT_HOST=auth.avataa.dev
KEYCLOAK_REDIRECT_PORT=443
KEYCLOAK_REDIRECT_PROTOCOL=https
UVICORN_WORKERS=3
```

### Explanation

#### Compose

- `REGISTRY_URL` - Docker regitry URL, e.g. `harbor.avataa.dev`
- `PLATFORM_PROJECT_NAME` - Docker regitry project Docker image can be downloaded from, e.g. `avataa`