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

ansible tag_smart_voting_server -m ping

cd ../ansible/

# 3a. Check inventory

ansible-inventory --graph

# 3b. Test SSH connectivity (Python is installed!)

ansible tier_app -m ping
ansible tag_Role_master -m ping
ansible tag_Role_slave -m ping

# 3c. Configure application servers

ansible-playbook setup-vm.yaml
ansible-playbook deploy-web-crawler.yaml

# 3d. Configure database servers

ansible-playbook configure-database.yaml

# 4. Verify everything

# Check application health

ansible tier_app -m shell -a "curl -s localhost:8000/health"

# Check database master

ansible tag_Role_master -m shell -a "mysql -u root -p'Admin#123' -e 'SHOW DATABASES;'"

# Check replication

ansible tag_Role_slave -m shell -a "mysql -u root -p'Admin#123' -e 'SHOW SLAVE STATUS\G' | grep -E 'Slave_IO_Running|Slave_SQL_Running'"

# Get ALB DNS

ALB_DNS=$(terraform -chdir=../terraform/ output -raw alb_dns_name)
curl "http://${ALB_DNS}/health"
