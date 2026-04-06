variable "resource_group_name" {
  description = "Name of the Azure resource group"
  type        = string
  default     = "weather-api-rg"
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "eastus"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "prod"
}

variable "acr_name" {
  description = "Name of the Azure Container Registry (must be globally unique)"
  type        = string
}

variable "app_name" {
  description = "Name of the App Service (must be globally unique)"
  type        = string
}

variable "app_service_sku" {
  description = "App Service SKU (F1 = free, B1 = basic, S1 = standard)"
  type        = string
  default     = "F1"
}

variable "openweather_api_key" {
  description = "OpenWeather API key"
  type        = string
  sensitive   = true
}