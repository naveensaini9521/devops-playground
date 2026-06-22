output "alb_dns_name" {
  value = aws_lb.app.dns_name
}

output "bastion_public_ip" {
  value = aws_instance.bastion.public_ip
}

output "app_asg_name" {
  value = aws_autoscaling_group.app.name
}

output "db_asg_name" {
  value = aws_autoscaling_group.db.name
}

output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_id" {
  value = aws_subnet.public[*].id
}

output "private_subnet_id" {
  value = aws_subnet.private.id
}