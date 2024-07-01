

resource "aws_iam_role" "pdf_to_md_lambda_role" {
  name               = "pdf_to_md_lambda_role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

resource "aws_iam_role_policy_attachment" "pdf_to_md_basic" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.pdf_to_md_lambda_role.name
}

resource "aws_cloudwatch_log_group" "pdf_to_md_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.pdf_to_md_lambda.function_name}"
  retention_in_days = 14
}

resource "aws_iam_role_policy_attachment" "pdf_to_md_lambda_logs" {
  role       = aws_iam_role.pdf_to_md_lambda_role.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

resource "aws_iam_role_policy_attachment" "pdf_to_md_bedrock_access" {
  role       = aws_iam_role.pdf_to_md_lambda_role.name
  policy_arn = aws_iam_policy.bedrock_access_policy.arn
}

resource "aws_iam_role_policy_attachment" "pdf_to_md_s3_access" {
  role       = aws_iam_role.pdf_to_md_lambda_role.name
  policy_arn = aws_iam_policy.s3_access_policy.arn
}

data "aws_ecr_image" "pdf_to_md_image" {
  repository_name = aws_ecr_repository.pdf_to_md.name
  image_tag       = var.pdf_to_md_image_tag
}

# NOTE: To push the image:
# aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 533267152364.dkr.ecr.us-east-1.amazonaws.com/pdf-to-md
# docker build --platform linux/amd64 -t 533267152364.dkr.ecr.us-east-1.amazonaws.com/pdf-to-md:latest .
# docker push 533267152364.dkr.ecr.us-east-1.amazonaws.com/pdf-to-md:latest

resource "aws_lambda_function" "pdf_to_md_lambda" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  function_name = "pdf_to_md_lambda"
  role          = aws_iam_role.pdf_to_md_lambda_role.arn
  timeout       = 900

  # TODO: try with arm64
  architectures = ["x86_64"]
  package_type  = "Image"
  # runtime = "python3.11"
  image_uri = data.aws_ecr_image.pdf_to_md_image.image_uri

  image_config {
    command = ["pdf_to_md.lambda_handler"]
  }

  environment {
    variables = {
      DATASETS_BUCKET = "s3://${aws_s3_bucket.datasets.bucket}"
    }
  }
}

resource "aws_lambda_function_event_invoke_config" "pdf_to_md_lambda" {
  function_name          = aws_lambda_function.pdf_to_md_lambda.function_name
  maximum_retry_attempts = 0
}

resource "aws_s3_bucket" "input_pdfs" {
  bucket = "collega-input-pdfs-${var.aws_account_id}"
}

resource "aws_s3_bucket_notification" "cds_upload_trigger" {
  bucket = aws_s3_bucket.input_pdfs.bucket

  lambda_function {
    lambda_function_arn = aws_lambda_function.pdf_to_md_lambda.arn
    events              = ["s3:ObjectCreated:*"]
    filter_suffix       = ".pdf"
  }
}

resource "aws_lambda_permission" "invoke_pdf_to_md" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.pdf_to_md_lambda.arn
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.input_pdfs.arn
}
