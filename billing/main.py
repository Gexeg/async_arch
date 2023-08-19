import uvicorn
from settings import settings
from adapters.db.db_init import db_init


if __name__ == "__main__":
    db_init()
    uvicorn.run(
        "entrypoints.views.billing:app",
        host=settings.service_host,
        port=settings.service_port,
    )
