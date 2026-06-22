Test SSH connectivity via bastion manually:

bash
ssh -i ~/Desktop/AWS/devops-key.pem -o ProxyCommand="ssh -W %h:%p -i ~/Desktop/AWS/devops-key.pem ec2-user@<BASTION_IP>" ec2-user@<PRIVATE_IP_OF_INSTANCE>
