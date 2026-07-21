terraform {
  backend "s3" {
    bucket = "tonni-projects-terraform-state"
    key    = "weather-project/terraform.tfstate"
    region = "eu-central-1"
  }
}
