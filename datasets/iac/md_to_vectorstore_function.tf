

resource "aws_iam_role" "md_to_vectorstore_lambda_role" {
  name               = "md_to_vectorstore_lambda_role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

resource "aws_iam_role_policy_attachment" "md_to_vectorstore_basic" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.md_to_vectorstore_lambda_role.name
}

resource "aws_cloudwatch_log_group" "md_to_vectorstore_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.md_to_vectorstore_lambda.function_name}"
  retention_in_days = 14
}

resource "aws_iam_role_policy_attachment" "md_to_vectorstore_lambda_logs" {
  role       = aws_iam_role.md_to_vectorstore_lambda_role.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

resource "aws_iam_role_policy_attachment" "md_to_vectorstore_bedrock_access" {
  role       = aws_iam_role.md_to_vectorstore_lambda_role.name
  policy_arn = aws_iam_policy.bedrock_access_policy.arn
}

resource "aws_iam_role_policy_attachment" "md_to_vectorstore_s3_access" {
  role       = aws_iam_role.md_to_vectorstore_lambda_role.name
  policy_arn = aws_iam_policy.s3_access_policy.arn
}

resource "aws_iam_role_policy_attachment" "md_to_vectorstore_dynamodb_access" {
  role       = aws_iam_role.md_to_vectorstore_lambda_role.name
  policy_arn = aws_iam_policy.dynamodb_access_policy.arn
}

data "aws_ecr_image" "md_to_vectorstore_image" {
  repository_name = aws_ecr_repository.md_to_vectorstore.name
  image_tag       = var.md_to_vectorstore_image_tag
}

# NOTE: To push the image:
# aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 533267152364.dkr.ecr.us-east-1.amazonaws.com/md-to-vectorstore
# docker build --platform linux/amd64 -t 533267152364.dkr.ecr.us-east-1.amazonaws.com/md-to-vectorstore:latest .
# docker push 533267152364.dkr.ecr.us-east-1.amazonaws.com/md-to-vectorstore:latest

resource "aws_secretsmanager_secret" "pinecone_api_key" {
  name = "pinecone-api-key"
}

data "aws_secretsmanager_secret_version" "pinecone_api_key" {
  secret_id = aws_secretsmanager_secret.pinecone_api_key.id
}

resource "aws_lambda_function" "md_to_vectorstore_lambda" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  function_name = "md_to_vectorstore_lambda"
  role          = aws_iam_role.md_to_vectorstore_lambda_role.arn
  timeout       = 60

  # TODO: try with arm64
  architectures = ["x86_64"]
  memory_size   = 512
  package_type  = "Image"
  image_uri     = data.aws_ecr_image.md_to_vectorstore_image.image_uri

  image_config {
    command = ["md_to_vectorstore.lambda_handler"]
  }

  environment {
    variables = {
      PINECONE_API_KEY = jsondecode(data.aws_secretsmanager_secret_version.pinecone_api_key.secret_string)["PINECONE_API_KEY"]
    }
  }
}

resource "aws_lambda_function_event_invoke_config" "md_to_vectorstore_lambda" {
  function_name          = aws_lambda_function.md_to_vectorstore_lambda.function_name
  maximum_retry_attempts = 0
}

resource "aws_s3_bucket_notification" "md_upload_trigger" {
  bucket = aws_s3_bucket.datasets.bucket

  lambda_function {
    lambda_function_arn = aws_lambda_function.md_to_vectorstore_lambda.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "cds-files"
    filter_suffix       = ".md"
  }
}

resource "aws_lambda_permission" "invoke_md_to_vectorstore" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.md_to_vectorstore_lambda.arn
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.datasets.arn
}
