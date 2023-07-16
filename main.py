from fastapi import FastAPI

from api.routes import contacts, auth, users
from fastapi_limiter import FastAPILimiter
from api.conf.config import settings
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as redis
from api.services.cors import CORS


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS.origins,
    allow_credentials=CORS.allow_credentials,
    allow_methods=CORS.allow_methods,
    allow_headers=CORS.allow_headers
)

app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)


@app.get("/")
def read_root():
    return {"message": "Welcome to PyWebEduHT11!"}
