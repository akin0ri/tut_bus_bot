resource "random_id" "storage" {
  byte_length = 4
}

resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_storage_account" "main" {
  name                     = lower(substr("${random_id.storage.hex}${var.storage_account_name}", 0, 24))
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_service_plan" "main" {
  name                = var.app_service_plan_name
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "Y1" # Consumption Plan
}

resource "azurerm_linux_function_app" "main" {
  name                       = var.function_app_name
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  service_plan_id            = azurerm_service_plan.main.id
  storage_account_name       = azurerm_storage_account.main.name
  storage_account_access_key = azurerm_storage_account.main.primary_access_key
  site_config {
    application_stack {
      python_version = "3.10"
    }
  }
  app_settings = {
    FUNCTIONS_WORKER_RUNTIME      = "custom"
    WEBSITE_RUN_FROM_PACKAGE      = "1"
    LINE_CHANNEL_ACCESS_TOKEN     = var.line_channel_access_token
    LINE_CHANNEL_SECRET           = var.line_channel_secret
    SECRET_KEY                    = var.secret_key
  }
} 