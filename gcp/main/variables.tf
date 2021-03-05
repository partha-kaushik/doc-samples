variable "cp2_project" {
  description = "The name of the GCP Project where all resources will be launched."
  type        = string
}

variable "cp2_srvc_acct_key_file" {
description = "Full path of project's service-account key file"
}

variable "cp2_region" {
  description = "The Region in which all GCP resources will be launched."
  type        = string
}

variable "cp2_zone" {
  description = "The zone for the resources"
  type        = string
}

variable "var_env" {
        default = "dev"
    }
variable "var_company" { 
        default = "nimbus"
    }
variable "uc1_private_subnet" {
    default = "10.26.1.0/24"
}
variable "uc1_public_subnet" {
    default = "10.26.2.0/24"
}
variable "ue1_private_subnet" {
    default = "10.26.3.0/24"
}
variable "ue1_public_subnet" {
    default = "10.26.4.0/24"
}

#variable "vpc_network_name" { 
#  description = "The name of the VPC network being created" 
#}
#variable "routing_mode" { 
#  description = "REGIONAL or GLOBAL"
#}