resource "aws_ecr_repository" "pdf_to_md" {
  name                 = "pdf-to-md"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
