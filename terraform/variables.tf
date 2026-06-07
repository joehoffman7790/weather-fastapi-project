variable "prefix" {
  description = "Short prefix used to name all resources. Keep it lowercase, no spaces."
  type        = string
  default     = "weatherdjango"
}

variable "location" {
  description = "Azure region for all resources."
  type        = string
  default     = "westus2"
}

variable "openweather_api_key" {
  description = "OpenWeatherMap API key. Passed in via CI/CD secret or local tfvars — never committed."
  type        = string
  sensitive   = true
}

variable "django_secret_key" {
  description = "Django SECRET_KEY. Generate with: python -c \"import secrets; print(secrets.token_urlsafe(50))\""
  type        = string
  sensitive   = true
}

variable "app_service_sku" {
  description = "App Service Plan SKU. B1 for basic, P1v2 for production."
  type        = string
  default     = "B1"
}

variable "acr_sku" {
  description = "ACR SKU. Basic is sufficient for a single app."
  type        = string
  default     = "Basic"
}

variable "postgres_user" {
  description = "PostgreSQL administrator login. Must not be 'azure_superuser', 'admin', or 'administrator'."
  type        = string
  sensitive   = true
}

variable "postgres_password" {
  description = "PostgreSQL administrator password. Min 8 chars, must include uppercase, lowercase, and a number."
  type        = string
  sensitive   = true
}