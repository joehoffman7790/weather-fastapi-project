# Resource Group — single container for all project resources
resource "azurerm_resource_group" "rg" {
  name     = local.resource_group_name
  location = var.location
  tags     = local.common_tags
}

# Data source: current Azure client config
# Used to get tenant_id and object_id for Key Vault RBAC and policy
data "azurerm_client_config" "current" {}
