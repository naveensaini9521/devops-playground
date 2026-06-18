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

# Run ansible playbook

ansible-playbook setup-vm.yml
