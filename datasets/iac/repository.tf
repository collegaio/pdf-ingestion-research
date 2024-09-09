resource "aws_ecr_repository" "pdf_to_md" {
  name                 = "pdf-to-md"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "md_to_vectorstore" {
  name                 = "md-to-vectorstore"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "md_to_df" {
  name                 = "md-to-df"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
