output "ue1_out_public_subnet_name" {
  value = google_compute_instance.default.google_compute_subnetwork.public_subnet.name
}

output "ue1_pub_address" {
  value = google_compute_instance.default.public_ip_address
  description = "Public IP of ue1 instance"
}

output "ue1_pri_address" {
  value = google_compute_instance.default.private_ip_address
  description = "Private IP of ue1 instance"
}