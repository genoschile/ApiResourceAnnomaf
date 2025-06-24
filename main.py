"""
# This module defines the Celery task for executing Nextflow scripts.
"""

import subprocess
import json
import os
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from task import run_nextflow
from pydantic import BaseModel
from dotenv import load_dotenv
from celery.result import AsyncResult
from fastapi import Request
from celery_worker import celery_app
import asyncio

app = FastAPI()

load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

status_mapping = {
    "PENDING": "pending",
    "STARTED": "running",
    "RECEIVED": "running",
    "RETRY": "running",
    "SUCCESS": "done",
    "FAILURE": "fail",
    "REVOKED": "fail",
}

@app.websocket("/ws/status/{task_id}")
async def websocket_status(websocket: WebSocket, task_id: str):
    await websocket.accept()

    while True:
        result = AsyncResult(task_id, app=celery_app)
        celery_state = result.state
        mapped_state = status_mapping.get(celery_state, "pending")

        await websocket.send_json({"state": mapped_state})

        if celery_state in ("SUCCESS", "FAILURE", "REVOKED"):
            break

        await asyncio.sleep(2)

    await websocket.close()

@app.post("/run")
async def run_job(request: Request):
    body = await request.json()
    print("Payload recibido:", body)
    task = run_nextflow.delay()
    return {"task_id": task.id}

class TranslationRequest(BaseModel):
    """
    Models the request body for translation.
    """
    text: str
    source_language: str
    target_language: str

def traducir_texto(texto, idioma_origen, idioma_destino):
    """
    function to translate text using AWS Translate.
    """
    region = os.getenv("AWS_REGION")

    if not region:
        return {"error": "Falta la variable de entorno AWS_REGION."}

    comando_aws = [
        "aws", "translate", "translate-text",
        "--text", texto,
        "--source-language-code", idioma_origen,
        "--target-language-code", idioma_destino,
        "--region", region
    ]

    try:
        resultado = subprocess.run(comando_aws, capture_output=True, text=True, check=True)
        respuesta = json.loads(resultado.stdout)
        return {"translated_text": respuesta.get("TranslatedText", "No translation found")}
    except subprocess.CalledProcessError as e:
        return {"error": f"Error ejecutando AWS CLI: {e}", "stderr": e.stderr}
    except json.JSONDecodeError:
        return {"error": f"Error al procesar la respuesta JSON: {resultado.stdout}"}

@app.post("/translate/")
async def translate_text(request: TranslationRequest):
    """
    Endpoint to translate text using AWS Translate.
    """
    return traducir_texto(request.text, request.source_language, request.target_language)

@app.get("/")
def read_root():
    """
    Root endpoint to check if the server is running.
    """
    return {"message": "Server running! jeje"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
