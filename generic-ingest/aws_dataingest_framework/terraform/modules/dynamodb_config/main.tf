
resource "aws_dynamodb_table" "config_ingestas" {
  name         = "${var.resource_prefix}ingesta_config_${var.env}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "dataset_name"

  attribute {
    name = "dataset_name"
    type = "S"
  }
}

resource "aws_dynamodb_table" "cola_ingestas" {
  name         = "${var.resource_prefix}cola_ingestas_${var.env}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "job_id"

  attribute {
    name = "job_id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "log_ingestas" {
  name         = "${var.resource_prefix}log_ingestas_${var.env}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "execution_id"

  attribute {
    name = "execution_id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "metricas_calidad" {
  name         = "${var.resource_prefix}metricas_calidad_${var.env}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "dataset_name"

  attribute {
    name = "dataset_name"
    type = "S"
  }
}

resource "aws_dynamodb_table" "log_anonimizacion" {
  name         = "${var.resource_prefix}log_anonimizacion_${var.env}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "execution_id"

  attribute {
    name = "execution_id"
    type = "S"
  }
}
