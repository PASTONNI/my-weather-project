# Output variable definitions

output "arn" {
  description = "ARN of the bucket"
  value       = aws_s3_bucket.my-weather-pipeline-bucket.arn
}

output "bucket_name" {
  description = "Name (id) of the bucket"
  value       = aws_s3_bucket.my-weather-pipeline-bucket.id
}

output "db_endpoint" {
  value = aws_db_instance.weather_db.address
}

output "db_port" {
  value = aws_db_instance.weather_db.port
}
