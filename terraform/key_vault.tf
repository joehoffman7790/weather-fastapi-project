data "azurerm_client_config" "current" {}

resource "random_string" "suffix" {
  length  = 6
  special = false
  upper   = false
}

resource "azurerm_key_vault" "weather" {
  name                       = "kv-weather-${random_string.suffix.result}"
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  enable_rbac_authorization  = true
  purge_protection_enabled   = false
  soft_delete_retention_days = 7
}

# Grant admin access so you no longer write secrets via Terraform / az cli
resource "azurerm_role_assignment" "me_kv_admin" {
  scope                = azurerm_key_vault.weather.id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id         = data.azurerm_client_config.current.object_id
}

# Grant the App Service's managed identity read access to secrets
resource "azurerm_role_assignment" "app_kv_reader" {
  scope                = azurerm_key_vault.weather.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = one(azurerm_linux_web_app.app.identity).principal_id
}

resource "azurerm_key_vault_secret" "openweather" {
  name         = "openweather-api-key"
  value        = var.openweather_api_key
  key_vault_id = azurerm_key_vault.weather.id

  depends_on = [azurerm_role_assignment.me_kv_admin]
}