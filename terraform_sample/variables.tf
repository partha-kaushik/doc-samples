variable "project" {
  description = "The name of the GCP Project where all resources will be launched."
  type        = string
}

variable "region" {
  description = "The Region in which all GCP resources will be launched."
  type        = string
}

variable "zone" {
  description = "The zone for the resources"
  type        = string
}
variable "vpc_network_name" { 
  description = "The name of the VPC network being created" 
}
variable "routing_mode" { 
  description = "REGIONAL or GLOBAL"
}
