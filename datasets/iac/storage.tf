resource "aws_s3_bucket" "datasets" {
  bucket = "collega-datasets-${var.aws_account_id}"
}
