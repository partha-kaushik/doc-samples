# terraform sample
This terraform code creates a VCP for an existing project in GCP (Google Cloud Platform). It further creates four private subnets, two with Google Services access and two without.

A router is created, with NAT provision for two of the above subnets. The router is allocated two external IP addresses.

The project name, zone and region,  and VPN name and zone are parametrized. The subnets are hard-coded. The whole network setup is effected tru a 'network' module.
