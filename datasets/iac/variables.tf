variable "aws_account_id" {
  type    = string
  default = "533267152364"
  # default = "939879343571"
}

variable "pdf_to_md_image_tag" {
  type    = string
  default = "latest"
}

variable "md_to_vectorstore_image_tag" {
  type    = string
  default = "latest"
}

variable "md_to_df_image_tag" {
  type    = string
  default = "latest"
}
