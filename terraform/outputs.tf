# ACR login server — used in GitHub Actions to tag and push the image
output "acr_login_server" {
  description = "ACR login server URL. Used in CI/CD: docker tag <img> <this>/<name>:latest"
  value       = azurerm_container_registry.acr.login_server
}

# App Service URL — the public URL for the deployed app
output "app_service_url" {
  description = "Public URL of the deployed Django app."
  value       = "https://${azurerm_linux_web_app.app.default_hostname}"
}

# Key Vault URI — needed if you want to reference it outside Terraform
output "key_vault_uri" {
  description = "Key Vault URI. Set as KEY_VAULT_URI env var for local dev against real secrets."
  value       = azurerm_key_vault.kv.vault_uri
}

# App Service managed identity principal ID — useful for debugging RBAC issues
output "app_service_principal_id" {
  description = "Managed identity principal ID of the App Service. Used for RBAC role assignments."
  value       = azurerm_linux_web_app.app.identity[0].principal_id
}

# ACR name — used in CI/CD workflow to run `az acr build` or `docker push`
output "acr_name" {
  description = "ACR resource name. Used in CI/CD: az acr build --registry <this>"
  value       = azurerm_container_registry.acr.name
}
