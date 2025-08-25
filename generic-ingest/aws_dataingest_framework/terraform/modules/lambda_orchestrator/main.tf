
resource "aws_lambda_function" "orchestrator" {
  function_name = "${var.resource_prefix}orquestador-${var.env}"
  handler       = "app.handler"
  runtime       = "python3.9"
  role          = var.iam_role_arn

  filename         = var.lambda_package_path
  source_code_hash = filebase64sha256(var.lambda_package_path)

  environment {
    variables = {
      CONFIG_TABLE = var.config_table_name
    }
  }
}
