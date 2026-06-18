# Amazon Linux 2023 ARM64 AMI
data "aws_ami" "amazon_linux" {
  most_recent = true

  owners = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"] # x86_64 architecture
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

resource "aws_instance" "smart_voting_server" {
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = "t2.micro"
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