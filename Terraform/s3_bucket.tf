resource "aws_s3_bucket" "my-weather-pipeline-bucket" {
  bucket = "my-weather-pipeline-bucket"

  force_destroy = true

  tags = {
    Name        = "weather-pipeline-bucket"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.my-weather-pipeline-bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}
