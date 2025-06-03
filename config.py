"""
create a config.py file to store configuration settings for the application.
This file contains settings for Celery broker and result backend,
"""
import os

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
NEXTFLOW_PIPELINES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '')
