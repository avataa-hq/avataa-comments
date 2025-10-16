from fastapi.params import Security
from starlette.middleware.cors import CORSMiddleware

from init_app import create_app
from routers.comments import comments, default_comments
from security import oauth2_scheme
from settings.settings import DEBUG

prefix = "/api/inventory_comments"
app_title = "Inventory Comments"

app = create_app(root_path=prefix)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app_version = "1"
v1_options = {
    "root_path": f"{prefix}/v{app_version}",
    "title": app_title,
    "version": app_version,
}
if DEBUG:
    """
    In case of debug mode, it sets access with any login parameters
    """
    v1_options["debug"] = True
else:
    v1_options["dependencies"] = [Security(oauth2_scheme)]
app_v1 = create_app(**v1_options)

app_v1.include_router(comments.router)
app_v1.include_router(default_comments.router)

app.mount(v1_options["root_path"], app_v1)
