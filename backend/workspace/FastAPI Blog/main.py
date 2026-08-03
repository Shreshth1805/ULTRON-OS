```python
from fastapi import FastAPI
from app.routes.blog import router
from app.database.db import engine
from app.models.blog import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
```