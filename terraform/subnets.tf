# Two public subnets in different AZs for ALB
resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.main.id
  cidr_block              = element(["10.0.10.0/24", "10.0.11.0/24"], count.index) # Changed to avoid conflict
  availability_zone       = element(["ap-south-1a", "ap-south-1b"], count.index)
  map_public_ip_on_launch = true

  tags = {
    Name        = "crawler-public-subnet-${count.index + 1}"
    Project     = "crawler"
    Environment = var.environment
    Tier        = "public"
  }
}

# Single private subnet for Databases
resource "aws_subnet" "private" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.20.0/24" # Changed to avoid conflict
  availability_zone       = "ap-south-1a"
  map_public_ip_on_launch = false

  tags = {
    Name        = "crawler-private-subnet"
    Project     = "crawler"
    Environment = var.environment
    Tier        = "private"
  }
}