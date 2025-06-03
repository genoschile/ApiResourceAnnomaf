"""
# This module defines the Celery task for executing Nextflow scripts.
"""
import subprocess
import json
import os
import uvicorn
from fastapi import FastAPI
from task import run_nextflow
from pydantic import BaseModel
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

@app.post("/run")
def run_job():
    """
    Endpoint to trigger the Nextflow job asynchronously.
    """
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
    return {"message": "Server running!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
