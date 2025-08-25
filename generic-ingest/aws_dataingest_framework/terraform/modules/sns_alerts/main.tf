
resource "aws_sns_topic" "data_quality_alerts" {
  name = "${var.resource_prefix}data-quality-alerts"
}
