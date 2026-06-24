# Data source for AMI
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }
}

# Bastion Server
resource "aws_instance" "bastion" {
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = "t3.medium"
  key_name               = "devops_ssh"
  subnet_id              = aws_subnet.public[0].id # First public subnet
  vpc_security_group_ids = [aws_security_group.bastion_sg.id]

  associate_public_ip_address = true

  iam_instance_profile = aws_iam_instance_profile.ssm_profile.name

  tags = {
    Name        = "crawler-bastion"
    Project     = "crawler"
    Environment = var.environment
    Tier        = "bastion"
  }

  user_data = <<-EOF
    #!/bin/bash
    dnf update -y
    dnf install -y python3 python3-pip
    echo "Bastion host ready"
  EOF
}