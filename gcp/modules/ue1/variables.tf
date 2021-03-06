variable "network_self_link" {
  description = "The network link"
}

variable "subnetwork1" {
  description = "subnework of ue1"
}

variable "env" {
  description = "dev/test/prod"
}

variable "company" {
  description = "company"
}

variable "var_ue1_private_subnet" {
  description = "the private subnet for ue1"
}

variable "var_ue1_public_subnet" {
  description = "the public subnet for ue1"
}

variable "region_map" {
  default = "na"
  description = "Atlas location of the region"
}