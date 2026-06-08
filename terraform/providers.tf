terraform {
  required_version = ">= 1.7.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.110"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

provider "azurerm" {
  features {
    key_vault {
      # Keeping this as is as this is a portfolio project
      purge_soft_delete_on_destroy    = true
      recover_soft_deleted_key_vaults = false
    }
    resource_group {
    prevent_deletion_if_contains_resources = false
    }
  }
}
