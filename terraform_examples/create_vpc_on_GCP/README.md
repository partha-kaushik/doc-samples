# terraform sample
This terraform code creates a VCP for an existing project in GCP (Google Cloud Platform). It further creates four private subnets, two with Google Services access and two without.

A router is created, with NAT provision for two of the above subnets. The router is allocated two external IP addresses.

The project name, zone and region,  and VPN name and zone are parametrized. The subnets are hard-coded. The whole network setup is effected through a 'network' module.

## Pre-reqs
The project must already exis in GCP, and a Service Access Key in JSON format must have been created for it. The JSON file must be placed in the main module of this terraform code.
