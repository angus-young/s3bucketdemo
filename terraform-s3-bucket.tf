terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

variable "REGION" {
    type = string
}

variable "BUCKET" {
    type = string
}

variable "ACCESS_KEY" {
    type = object({
        ID    = string
        VALUE = string
    })
    sensitive = true
}

provider "aws" {
  region     = var.REGION
  access_key = var.ACCESS_KEY.ID
  secret_key = var.ACCESS_KEY.VALUE
}

module "aws_s3" {
  source = "terraform-aws-modules/s3-bucket/aws"

  bucket = var.BUCKET
  acl    = "private"
  force_destroy = true
}

output "region" {
  value = module.aws_s3.s3_bucket_region
}

output "bucket" {
  value = module.aws_s3.s3_bucket_id
}

output "aws_access_key_id" {
  value     = var.ACCESS_KEY.ID
  sensitive = true
}

output "aws_secret_access_key" {
  value     = var.ACCESS_KEY.VALUE
  sensitive = true
}
