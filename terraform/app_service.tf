# App Service Plan — B1 Linux
resource "azurerm_service_plan" "plan" {
  name                = local.app_service_plan
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = var.app_service_sku

  tags = local.common_tags
}

# App Service — Linux container running the Django image from ACR
resource "azurerm_linux_web_app" "app" {
  name                = local.app_service_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  service_plan_id     = azurerm_service_plan.plan.id

  # System-assigned managed identity — Azure creates this automatically
  # The principal_id it generates is what we assign roles to in key_vault.tf
  identity {
    type = "SystemAssigned"
  }

  site_config {
    always_on = true # B1 supports always_on; prevents cold starts on the free tier

    application_stack {
      docker_image_name        = "${local.acr_name}.azurecr.io/${local.app_service_name}:latest"
      docker_registry_url      = "https://${azurerm_container_registry.acr.login_server}"
      docker_registry_username = null # No credentials — ACR pull auth via managed identity
      docker_registry_password = null
    }
  }

  app_settings = {
    # Tell the App Service to use managed identity for ACR pulls
    # This replaces the old admin-password approach that broke the original app
    DOCKER_ENABLE_CI                    = "true"
    WEBSITES_ENABLE_APP_SERVICE_STORAGE = "false"

    # Django runtime settings
    DJANGO_SETTINGS_MODULE = "config.settings"
    PORT                   = "8000"

    # Key Vault URI — the app reads this env var to know where to fetch secrets from
    # Actual secret values are fetched at runtime by DefaultAzureCredential, not stored here
    KEY_VAULT_URI = azurerm_key_vault.kv.vault_uri

    # Database connection string — interpolated from the Postgres Flexible Server resource
    # Password is also stored in Key Vault for reference, but App Service needs it inline here
    DATABASE_URL = "postgresql://${var.postgres_user}:${var.postgres_password}@${azurerm_postgresql_flexible_server.db.fqdn}:5432/weatherdb?sslmode=require"
  }

  tags = local.common_tags
}

# -----------------------------------------------------------------------
# RBAC: Grant the App Service managed identity "AcrPull" on the registry
# This lets App Service pull the Docker image without admin credentials
# -----------------------------------------------------------------------
resource "azurerm_role_assignment" "acr_pull" {
  scope                = azurerm_container_registry.acr.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_linux_web_app.app.identity[0].principal_id

  depends_on = [azurerm_linux_web_app.app]
}
