# -----------------------------------------------------------------------------
# PowerGrid Azure Infrastructure
# Provider: Azure Resource Manager (azurerm)
# Purpose: Provisions the hosting environment for the CoE microservices.
# -----------------------------------------------------------------------------

terraform {
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

# -----------------------------------------------------------------------------
# Resource Group: Logical container for PowerGrid resources
# -----------------------------------------------------------------------------
resource "azurerm_resource_group" "powergrid_rg" {
  name     = "rg-powergrid-dev-weu-001"
  location = "swedencentral"
  
  tags = {
    Environment = "Development"
    Project     = "PowerGrid"
    Owner       = "CenterOfExcellence"
  }
}

# -----------------------------------------------------------------------------
# App Service Plan: The compute resources (Server Farm)
# SKU: B1 (Basic) is cost-effective for prototypes but supports Linux.
# -----------------------------------------------------------------------------
resource "azurerm_service_plan" "powergrid_plan" {
  name                = "asp-powergrid-dev-weu-001"
  resource_group_name = azurerm_resource_group.powergrid_rg.name
  location            = azurerm_resource_group.powergrid_rg.location
  os_type             = "Linux"
  sku_name            = "B1" 
}

# -----------------------------------------------------------------------------
# Web App: Hosting the Docker Containers
# Note: In a full prod environment, we might use Azure Container Apps (ACA) 
# or Kubernetes (AKS). For a trainee MVP, a single App Service with Docker Compose 
# support is the most "Maintainable" choice.
# -----------------------------------------------------------------------------
resource "azurerm_linux_web_app" "powergrid_app" {
  name                = "app-powergrid-core-dev"
  resource_group_name = azurerm_resource_group.powergrid_rg.name
  location            = azurerm_service_plan.powergrid_plan.location
  service_plan_id     = azurerm_service_plan.powergrid_plan.id

  site_config {
    # This command instructs Azure to run the multi-container setup
    app_command_line = "docker-compose up" 
    
    application_stack {
      docker_image_name   = "nginx:latest" # Placeholder: In real deployment, this points to ACR
      docker_registry_url = "https://index.docker.io"
    }
  }

  app_settings = {
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
    "DOCKER_REGISTRY_SERVER_URL"          = "https://index.docker.io"
  }
}