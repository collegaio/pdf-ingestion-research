terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }

    # NOTE: must set PINECONE_API_KEY environment variable
    pinecone = { 
      source = "pinecone-io/pinecone"
      version = "~> 0.7"
    } 
  }

  backend "s3" {
    bucket = "tf-state-533267152364"
    key    = "dataset-functions"
    region = "us-east-1"
  }
}

// TODO: terraform state and lock with dynamodb + S3

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
  profile = "collega-prod"
}
