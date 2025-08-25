
import json
import boto3
import os

def handler(event, context):
    print("Orquestador Lambda iniciado")
    # Aquí podrías consultar DynamoDB y decidir si ejecutar Glue o Lambda
    return {"status": "ok"}
