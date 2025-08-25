from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3
from diagrams.aws.database import Dynamodb
from diagrams.aws.integration import SNS
from diagrams.aws.analytics import Glue, Athena
from diagrams.onprem.client import Users
from diagrams.aws.storage import S3 as Storage

with Diagram("Framework de Ingesta de Datos en AWS", show=True, direction="LR"):

    with Cluster("Data Sources"):
        ftps = Storage("FTPS / Buckets")
        nifi = Custom("Apache NiFi", "./resources/nifi.png")
        ftps >> nifi

    with Cluster("Landing Zone"):
        landing_bucket = S3("Bucket Landing")
        orquestador = Lambda("Orquestador")
        config_ingesta = Dynamodb("Config. de Ingestas")
        cola_ingesta = Dynamodb("Cola de Ingestas")
        lambda_ligera = Lambda("Job Lambda\nData Liviana")
        glue_pesada = Glue("Job Glue\nData Pesada")

        nifi >> landing_bucket >> orquestador
        orquestador >> config_ingesta
        orquestador >> cola_ingesta
        orquestador >> lambda_ligera
        orquestador >> glue_pesada

    with Cluster("Refined Zone"):
        refined_bucket = S3("Bucket Refined")
        job_dataquality = Lambda("Job DataQuality")
        catalog = Glue("Data Catalog")
        log_ingestas = Dynamodb("Log de Ingestas")
        metricas_dq = Dynamodb("Métricas de Calidad")
        sns = SNS("SNS Notificaciones")

        lambda_ligera >> refined_bucket
        glue_pesada >> refined_bucket
        refined_bucket >> job_dataquality >> sns
        job_dataquality >> metricas_dq
        refined_bucket >> catalog
        refined_bucket >> log_ingestas

    with Cluster("Trusted Zone"):
        trusted_bucket = S3("Bucket Trusted")
        anon_job = Lambda("Job Anonimizador")
        log_anon = Dynamodb("Log Anonimización")

        job_dataquality >> anon_job >> trusted_bucket
        anon_job >> log_anon

    with Cluster("Athena / Acceso"):
        db_refined = Athena("db_refined")
        db_trusted = Athena("db_trusted_analytics")
        users = Users("Usuarios de Datos")

        refined_bucket >> db_refined
        trusted_bucket >> db_trusted >> users
