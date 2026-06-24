resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name        = "crawler-igw"
    Project     = "crawler"
    Environment = var.environment
  }
}