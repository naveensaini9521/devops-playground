# boto3 and botocore

sudo apt update
sudo apt install python3-pip -y
pip3 install --user boto3 botocore

# install required Ansible AWS collection

ansible-galaxy collection install amazon.aws

# Then test again

ansible-inventory -i aws_ec2.yml --list

## Test

# List inventory to see the group and hosts

ansible-inventory --list

cd ../ansible/

# 3a. Check inventory

ansible-inventory --graph

# 3b. Test SSH connectivity (Python is installed!)

ansible tier_app -m ping
ansible tag_Role_master -m ping
ansible tag_Role_slave -m ping

# 3c. Configure application servers

ansible-playbook setup-vm.yaml
ansible-playbook deploy-docker.yaml

# 3d. Configure database servers

ansible-playbook configure-database.yaml

# Check System Status on the Slave Node

sudo mysql -e "SHOW SLAVE STATUS\G"

# Run a Functional Replication Test

sudo mysql -e "USE crawlerdb; CREATE TABLE replication_test (id INT AUTO_INCREMENT PRIMARY KEY, tested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP); INSERT INTO replication_test () VALUES ();"

# Get ALB DNS

ALB_DNS=$(terraform -chdir=../terraform/ output -raw alb_dns_name)
curl "http://${ALB_DNS}/health"
