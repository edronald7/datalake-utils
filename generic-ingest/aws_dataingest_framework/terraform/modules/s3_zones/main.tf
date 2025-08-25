
resource "aws_s3_bucket" "landing" {
  bucket = "${var.resource_prefix}landing-${var.env}"
  force_destroy = true
}

resource "aws_s3_bucket" "refined" {
  bucket = "${var.resource_prefix}refined-${var.env}"
  force_destroy = true
}

resource "aws_s3_bucket" "trusted" {
  bucket = "${var.resource_prefix}trusted-${var.env}"
  force_destroy = true
}
