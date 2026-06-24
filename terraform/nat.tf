# Elastic IP for NAT Gateway
resource "aws_eip" "nat" {
  domain = "vpc"

  tags = {
    Name        = "crawler-nat-eip"
    Project     = "crawler"
    Environment = var.environment
  }
}

# NAT Gateway in first public subnet
resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public[0].id

  tags = {
    Name        = "crawler-nat"
    Project     = "crawler"
    Environment = var.environment
  }

  depends_on = [aws_internet_gateway.igw]
}