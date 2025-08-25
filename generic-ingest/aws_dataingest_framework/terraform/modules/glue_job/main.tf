
resource "aws_glue_job" "default" {
  name     = "${var.resource_prefix}job_glue_default"
  role_arn = var.iam_role_arn

  command {
    name            = "glueetl"
    script_location = "s3://scripts/glue/default_etl.py"
    python_version  = "3"
  }

  max_retries      = 1
  glue_version     = "3.0"
  number_of_workers = 2
  worker_type      = "G.1X"
}
