# Output variable definitions

output "arn" {
  description = "ARN of the bucket"
  value       = aws_s3_bucket.my-weather-pipeline-bucket.arn
}

output "bucket_name" {
  description = "Name (id) of the bucket"
  value       = aws_s3_bucket.my-weather-pipeline-bucket.id
}
