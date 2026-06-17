data "aws_ami" "ubuntu" {
  most_recent = true

  owners = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "smart_voting_server" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  key_name               = "devops-key"
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.smart_voting_sg.id]

  tags = {
    Name = var.instance_name
  }

  timeouts {
    create = "5m"
  }
}