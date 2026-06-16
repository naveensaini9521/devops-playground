Test SSH connectivity via bastion manually:

bash
ssh -i ~/Desktop/AWS/devops-key.pem -o ProxyCommand="ssh -W %h:%p -i ~/Desktop/AWS/devops-key.pem ec2-user@<BASTION_IP>" ec2-user@<PRIVATE_IP_OF_INSTANCE>

# 1. Apply with higher parallelism

terraform apply -parallelism=20 -auto-approve

# 2. If you want to skip refresh for speed

terraform apply -parallelism=20 -refresh=false -auto-approve

# 3. Destroy with higher parallelism

terraform destroy -parallelism=20 -auto-approve
