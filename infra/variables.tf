variable "resource_group_name" {
  default = "tutbusbotG"
}

variable "location" {
  default = "japaneast"
}

variable "storage_account_name" {
  default = "tutbusbotSG"
}

variable "function_app_name" {
  default = "tutbusbotAPP"
}

variable "app_service_plan_name" {
  default = "tutbusbotPN"
}

variable "line_channel_access_token" {
  description = "LINE channel authentication token"
  type        = string
  sensitive   = true
}

variable "line_channel_secret" {
  description = "LINE channel secret"
  type        = string
  sensitive   = true
}

variable "secret_key" {
  description = "Flask secret key"
  type        = string
  sensitive   = true
} 