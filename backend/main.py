# API do Alerta Golpe
# Rodar (dentro da pasta backend): uvicorn main:app --reload
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config
from routers import analises

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Alerta Golpe API", version="1.0")

# CORS restrito: só as origens do .env (o padrão é só o front local)
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.include_router(analises.router)


@app.get("/health")
def health():
    return {"status": "ok", "ia_configurada": bool(config.OPENAI_API_KEY)}
