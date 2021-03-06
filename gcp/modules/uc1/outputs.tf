#subnetwork1 = module.uc1.uc1_out_public_subnet_name
output "uc1_out_public_subnet_name" {
  value = google_compute_instance.default.google_compute_subnetwork.public_subnet.name
}

output "uc1_pub_address" {
  value = google_compute_instance.default.public_ip_address
  description = "Public IP of uc1 instance"
}

output "uc1_pri_address" {
  value = google_compute_instance.default.private_ip_address
  description = "Private IP of uc1 instance"
}
