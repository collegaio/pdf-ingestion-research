resource "aws_dynamodb_table" "collega_datasets" {
    name           = "collega-datasets"
    billing_mode   = "PAY_PER_REQUEST"
    hash_key       = "collection"
    range_key      = "doc_id"

    attribute {
        name = "collection"
        type = "S"
    }

    attribute {
        name = "doc_id"
        type = "S"
    }
}

resource "pinecone_index" "collega_datasets" {
  name       = "collega-datasets"
  dimension  = 1024
  metric     = "cosine"
  spec       = {
    serverless = {
      cloud  = "aws"
      region = "us-east-1"
    }
  }
}
