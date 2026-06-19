resource "aws_security_group" "bastion_sg" {
  name        = "smart-voting-bastion-sg"
  description = "Bastion uses SSM"
  vpc_id      = aws_vpc.main.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "smart-voting-bastion-sg" }
}

resource "aws_instance" "bastion" {
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = "t3.micro"
  key_name               = "devops-key"
  subnet_id              = aws_subnet.public[1].id
  vpc_security_group_ids = [aws_security_group.bastion_sg.id]

  associate_public_ip_address = true

  iam_instance_profile = aws_iam_instance_profile.ssm_profile.name

  tags = { Name = "bastion-host" }
}