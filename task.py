"""
asynchronous task to run a Nextflow script
"""
import subprocess
from celery import Celery

celery_app = Celery("tasks", broker="redis://redis:6379/0", backend="redis://redis:6379/0")

@celery_app.task
def run_nextflow():
    """
    Executes a Nextflow script using subprocess.
    """
    # espacio ram

    try:
        result = subprocess.run(
            ["nextflow", "run", "nf_script.nf"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Nextflow failed:\n{e.stderr}"
    except OSError as e:
        return f"Execution failed (possibly command not found or permission issue):\n{str(e)}"

# saber cuando termino, y si termino 
