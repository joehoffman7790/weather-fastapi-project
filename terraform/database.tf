# Azure Database for PostgreSQL Flexible Server
resource "azurerm_postgresql_flexible_server" "db" {
  name                          = "${var.prefix}-db"
  resource_group_name           = azurerm_resource_group.rg.name
  location                      = azurerm_resource_group.rg.location
  version                       = "16"
  administrator_login           = var.postgres_user
  administrator_password        = var.postgres_password
  sku_name                      = "B_Standard_B1ms"
  storage_mb                    = 32768
  public_network_access_enabled = true

  lifecycle {
    ignore_changes = [zone]
  }

  tags = local.common_tags
}

# Allow Azure services (including App Service) to connect
resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_azure_services" {
  name      = "allow-azure-services"
  server_id = azurerm_postgresql_flexible_server.db.id

  # 0.0.0.0 to 0.0.0.0 is the Azure convention for "allow all Azure-internal traffic"
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}

# The database itself inside the server
resource "azurerm_postgresql_flexible_server_database" "weatherdb" {
  name      = "weatherdb"
  server_id = azurerm_postgresql_flexible_server.db.id
  collation = "en_US.utf8"
  charset   = "utf8"
}

# Store DB credentials in Key Vault — same pattern as OWM key
resource "azurerm_key_vault_secret" "postgres_user" {
  name         = "POSTGRES-USER"
  value        = var.postgres_user
  key_vault_id = azurerm_key_vault.kv.id
  tags         = local.common_tags
  depends_on   = [azurerm_role_assignment.kv_terraform_admin]
}

resource "azurerm_key_vault_secret" "postgres_password" {
  name         = "POSTGRES-PASSWORD"
  value        = var.postgres_password
  key_vault_id = azurerm_key_vault.kv.id
  tags         = local.common_tags
  depends_on   = [azurerm_role_assignment.kv_terraform_admin]
}
