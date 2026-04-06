terraform {
  required_version = ">= 1.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location

  tags = {
    Environment = var.environment
    Project     = "weather-api"
    ManagedBy   = "Terraform"
  }
}

# Container Registry
resource "azurerm_container_registry" "acr" {
  name                = var.acr_name
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "Basic"
  admin_enabled       = true

  tags = {
    Environment = var.environment
  }
}

# App Service Plan
resource "azurerm_service_plan" "plan" {
  name                = "${var.app_name}-plan"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = var.app_service_sku

  tags = {
    Environment = var.environment
  }
}

# Web App
resource "azurerm_linux_web_app" "app" {
  name                = var.app_name
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  service_plan_id     = azurerm_service_plan.plan.id

  site_config {
    always_on = var.app_service_sku == "F1" ? false : true

    application_stack {
  docker_image_name        = "weather-api:latest"  # Remove the server prefix
  docker_registry_url      = "https://${azurerm_container_registry.acr.login_server}"
  docker_registry_username = azurerm_container_registry.acr.admin_username
  docker_registry_password = azurerm_container_registry.acr.admin_password
}
  }

  app_settings = {
    "WEBSITES_PORT"                    = "8000"
    "OPENWEATHER_API_KEY"              = var.openweather_api_key
    "DOCKER_REGISTRY_SERVER_URL"       = "https://${azurerm_container_registry.acr.login_server}"
    "DOCKER_REGISTRY_SERVER_USERNAME"  = azurerm_container_registry.acr.admin_username
    "DOCKER_REGISTRY_SERVER_PASSWORD"  = azurerm_container_registry.acr.admin_password
  }

  tags = {
    Environment = var.environment
  }
}