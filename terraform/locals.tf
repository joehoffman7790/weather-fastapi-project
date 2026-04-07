locals {
  common_tags = {
    Environment = var.environment
    Project     = "weather-fastapi"
    ManagedBy   = "terraform"
  }
}