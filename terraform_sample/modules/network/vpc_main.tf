# Terraform config for GCP VPC

resource "google_compute_network" "vpc_network" {
  name = var.vpc_network_name
  routing_mode = var.routing_mode
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "private-subnet-1" {
  name          = "private-subnet-1"
  ip_cidr_range = "10.0.0.0/23"
  region        = "us-west1"
  private_ip_google_access = true
  network       = google_compute_network.vpc_network.id
}

resource "google_compute_subnetwork" "private-subnet-2" {
  name          = "private-subnet-2"
  ip_cidr_range = "10.0.2.0/23"
  region        = "us-west1"
  private_ip_google_access = true
  network       = google_compute_network.vpc_network.id
}



resource "google_compute_subnetwork" "private_plusgoogle_subnet_3" {
  name          = "private-subnet-3"
  ip_cidr_range = "10.0.4.0/23"
  region        = "us-west1"
  private_ip_google_access = false
  network       = google_compute_network.vpc_network.id
}

resource "google_compute_subnetwork" "private_plusgoogle_subnet_4" {
  name          = "private-subnet-4"
  ip_cidr_range = "10.0.6.0/23"
  region        = "us-west1"
  private_ip_google_access = false
  network       = google_compute_network.vpc_network.id
}

resource "google_compute_router" "router" {
  name    = "uni-router"
  region  = google_compute_subnetwork.private_plusgoogle_subnet_4.region
  network = google_compute_network.vpc_network.id
}

resource "google_compute_address" "address" {
  count  = 2
  name   = "nat-manual-ip-${count.index}"
  region = google_compute_subnetwork.private_plusgoogle_subnet_4.region
}

resource "google_compute_router_nat" "nat_manual" {
  name   = "my-router-nat"
  router = google_compute_router.router.name
  region = google_compute_router.router.region

  nat_ip_allocate_option = "MANUAL_ONLY"
  nat_ips                = google_compute_address.address.*.self_link

  source_subnetwork_ip_ranges_to_nat = "LIST_OF_SUBNETWORKS"
  subnetwork {
    name                    = google_compute_subnetwork.private_plusgoogle_subnet_3.id
    source_ip_ranges_to_nat = ["ALL_IP_RANGES"]
  }
  subnetwork {
    name                    = google_compute_subnetwork.private_plusgoogle_subnet_4.id
    source_ip_ranges_to_nat = ["ALL_IP_RANGES"]
  }
}