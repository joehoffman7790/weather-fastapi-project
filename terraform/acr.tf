# Azure Container Registry — stores the Docker image for the Django app
resource "azurerm_container_registry" "acr" {
  name                = local.acr_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = var.acr_sku

  # Admin credentials disabled — App Service authenticates via managed identity instead
  admin_enabled = false

  tags = local.common_tags
}
