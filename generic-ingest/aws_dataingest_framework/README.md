
# 🧩 Framework de Ingesta de Datos en AWS

Este repositorio contiene la infraestructura como código (IaC) para desplegar un **framework de ingesta de datos reutilizable y gobernado** en AWS. Está diseñado para facilitar el trabajo de:

- **Data Engineers**: configuración de nuevas ingestas, orquestación, transformación.
- **Equipos DevOps / Data Platform**: despliegue y mantenimiento de la infraestructura base del framework.

## 🧱 Arquitectura General

El framework se compone de tres zonas principales dentro de un Data Lake:

| Zona           | Función Principal                         | Servicios Principales                      |
|----------------|--------------------------------------------|--------------------------------------------|
| **Landing**    | Recepción de datos crudos                  | S3, Lambda, DynamoDB                       |
| **Refined**    | Transformación y validación                | S3, Glue, Lambda, Data Catalog, DynamoDB   |
| **Trusted**    | Publicación de datos anonimizados confiables | S3, Lambda, Athena, DynamoDB, SNS          |

## 📁 Estructura del Repositorio

```
terraform/
├── modules/
│   ├── s3_zones/
│   ├── lambda_orchestrator/
│   ├── glue_job/
│   ├── dynamodb_config/
│   ├── sns_alerts/
│   └── iam_roles/
├── environments/
│   ├── dev/
│   └── prod/
├── data-config/
│   └── datasets/
├── lambda_jobs/
│   ├── orchestrator/
│   ├── data_quality/
│   └── anonymizer/
└── scripts/glue/
```

## 🚀 Despliegue de la Infraestructura Base (DevOps)

### 1. Requisitos

- AWS CLI configurado
- Terraform ≥ 1.3.0
- Permisos para crear recursos (S3, Lambda, Glue, DynamoDB, IAM)

### 2. Variables clave

- `env`: entorno (`dev`, `prod`, etc.)
- `resource_prefix`: prefijo para identificar recursos del framework (por defecto `dlgi_`)

### 3. Pasos de despliegue

```bash
cd terraform/environments/dev

terraform init
terraform apply -var="env=dev" -var="resource_prefix=dlgi_"
```

## ⚙️ Configuración de nuevas ingestas (Data Engineers)

Cada dataset se declara como un archivo Terraform en `data-config/datasets/`.

### Ejemplo: `clientes_ingesta.tf`

```hcl
resource "aws_dynamodb_table_item" "ingesta_clientes" {
  table_name = "dlgi_ingesta_config_dev"
  hash_key   = "dataset_name"

  item = <<ITEM
{
  "dataset_name": {"S": "clientes"},
  "job_type": {"S": "glue"},
  "frecuencia": {"S": "diaria"},
  "path_landing": {"S": "clientes/"},
  "output_table": {"S": "clientes_refined"}
}
ITEM
}
```

### Aplicar cambios:

```bash
cd terraform/data-config
terraform init
terraform apply -var="env=dev" -var="resource_prefix=dlgi_"
```

## 📦 Código fuente Lambda

Los siguientes lambdas están incluidos con su código de ejemplo en `lambda_jobs/`:

| Lambda             | Función                                     |
|--------------------|---------------------------------------------|
| `orchestrator`     | Decide el tipo de job a ejecutar (Glue o Lambda) |
| `data_quality`     | Aplica reglas básicas de calidad            |
| `anonymizer`       | Enmascara o elimina datos sensibles         |

## 🧪 Glue ETL de ejemplo

Archivo: `scripts/glue/default_etl.py`

Funcionalidad:

- Lee desde `landing`
- Elimina duplicados
- Escribe en formato Parquet a `refined`

## 🔒 Seguridad y Gobernanza

- Recursos con prefijo (`dlgi_`) para fácil trazabilidad.
- IAM policy de ejemplo incluida.
- Compatible con Lake Formation para control avanzado.

## 📬 Soporte

Contacta al equipo de Data Engineering o DevOps responsable del Lakehouse.
