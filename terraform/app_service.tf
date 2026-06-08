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

  identity {
    type = "SystemAssigned"
  }

  site_config {
    always_on                               = true
    container_registry_use_managed_identity = true

    application_stack {
      docker_image_name   = "${local.app_service_name}:latest"
      docker_registry_url = "https://${azurerm_container_registry.acr.login_server}"
    }
  }

  app_settings = {
    WEBSITES_ENABLE_APP_SERVICE_STORAGE = "false"
    DOCKER_ENABLE_CI                    = "true"
    DJANGO_SETTINGS_MODULE              = "config.settings"
    PORT                                = "8000"
    WEBSITES_PORT                       = "8000"
    KEY_VAULT_URI                       = azurerm_key_vault.kv.vault_uri
    DATABASE_URL                        = "postgresql://${var.postgres_user}:${var.postgres_password}@${azurerm_postgresql_flexible_server.db.fqdn}:5432/weatherdb?sslmode=require"
    DEBUG                               = "true"
  }

  tags = local.common_tags
}

resource "azurerm_role_assignment" "acr_pull" {
  scope                = azurerm_container_registry.acr.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_linux_web_app.app.identity[0].principal_id

  depends_on = [azurerm_linux_web_app.app]
}
