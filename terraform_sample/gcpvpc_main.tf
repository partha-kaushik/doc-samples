terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "3.5.0"
    }
  }
}

provider "google" {

  credentials = file("uniproject-32470-717b9616b07f.json")

  project = var.project
  region  = var.region
  zone    = var.zone
}

module "vpc_main" {
  source = "./modules/network"  

  vpc_network_name = var.vpc_network_name
  routing_mode = var.routing_mode
}