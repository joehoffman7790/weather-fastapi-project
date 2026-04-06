output "resource_group_name" {
  description = "Name of the resource group"
  value       = azurerm_resource_group.main.name
}

output "acr_login_server" {
  description = "ACR login server URL"
  value       = azurerm_container_registry.acr.login_server
}

output "acr_admin_username" {
  description = "ACR admin username"
  value       = azurerm_container_registry.acr.admin_username
  sensitive   = true
}

output "acr_admin_password" {
  description = "ACR admin password"
  value       = azurerm_container_registry.acr.admin_password
  sensitive   = true
}

output "app_url" {
  description = "URL of the deployed application"
  value       = "https://${azurerm_linux_web_app.app.default_hostname}"
}

output "app_name" {
  description = "Name of the App Service"
  value       = azurerm_linux_web_app.app.name
}