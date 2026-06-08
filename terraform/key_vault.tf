# Key Vault — stores the OpenWeatherMap API key and Django secret key
resource "azurerm_key_vault" "kv" {
  name                = local.key_vault_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"

  # RBAC authorization mode — modern approach, replaces legacy access policies
  # Roles are assigned per-identity at the resource level instead of vault-wide policies
  enable_rbac_authorization = true

  # Soft delete is enabled by default (90 day retention) — do not disable
  # purge_protection prevents hard deletion even by vault owner (recommended for prod)
  purge_protection_enabled = false # Set to true once stable; false allows terraform destroy during dev

  tags = local.common_tags
}

# -----------------------------------------------------------------------
# RBAC: Grant the Terraform caller (you / the CI service principal)
# "Key Vault Secrets Officer" on this vault so it can write secrets.
# Without this, the azurerm_key_vault_secret resources below will 403.
# -----------------------------------------------------------------------
resource "azurerm_role_assignment" "kv_terraform_admin" {
  scope                = azurerm_key_vault.kv.id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id         = data.azurerm_client_config.current.object_id
}

# -----------------------------------------------------------------------
# Secrets — both values come from variables (never hardcoded)
# depends_on the role assignment so the write doesn't race the permission
# -----------------------------------------------------------------------
resource "azurerm_key_vault_secret" "owm_api_key" {
  name         = local.kv_secret_owm
  value        = var.openweather_api_key
  key_vault_id = azurerm_key_vault.kv.id

  tags = local.common_tags

  depends_on = [azurerm_role_assignment.kv_terraform_admin]
}

resource "azurerm_key_vault_secret" "django_secret_key" {
  name         = local.kv_secret_django
  value        = var.django_secret_key
  key_vault_id = azurerm_key_vault.kv.id

  tags = local.common_tags

  depends_on = [azurerm_role_assignment.kv_terraform_admin]
}

# -----------------------------------------------------------------------
# RBAC: Grant the App Service managed identity read-only access to secrets
# "Key Vault Secrets User" = GetSecret + ListSecrets, nothing else
# This is the identity DefaultAzureCredential uses at runtime
# -----------------------------------------------------------------------
resource "azurerm_role_assignment" "kv_app_secrets_user" {
  scope                = azurerm_key_vault.kv.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_linux_web_app.app.identity[0].principal_id

  depends_on = [azurerm_linux_web_app.app]
}
