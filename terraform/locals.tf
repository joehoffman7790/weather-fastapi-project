locals {
  # All resource names derived from prefix so they're consistent and predictable
  resource_group_name = "${var.prefix}-rg"
  acr_name            = "${var.prefix}acr"         # ACR names: alphanumeric only, 5-50 chars
  key_vault_name      = "${var.prefix}-kv"         # Key Vault names: 3-24 chars, alphanumeric + hyphens
  app_service_plan    = "${var.prefix}-plan"
  app_service_name    = "${var.prefix}-app"

  # Secret names in Key Vault — use hyphens, not underscores (KV convention)
  kv_secret_owm   = "OPENWEATHER-API-KEY"
  kv_secret_django = "DJANGO-SECRET-KEY"

  common_tags = {
    project     = "weather-django"
    environment = "production"
    managed_by  = "terraform"
  }
}
