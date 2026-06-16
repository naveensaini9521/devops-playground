resource "aws_security_group" "smart_voting_sg" {

  name        = "smart-voting-sg"
  description = "Security Group for Smart Voting"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
# EC2 instance

resource "aws_instance" "smart_voting_server" {

  ami           = "ami-006f82a1d5a27da54"
  instance_type = "t2.micro"

  key_name = "devops-key"

  vpc_security_group_ids = [
    aws_security_group.smart_voting_sg.id
  ]

  root_block_device {
    volume_size = 25
    volume_type = "gp3"
  }

  user_data = file("user-data.sh")

  tags = {
    Name = "smart-voting-server"
  }
}