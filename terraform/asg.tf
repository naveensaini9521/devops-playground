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

resource "aws_launch_template" "app" {
  name_prefix            = "smart-voting-app-"
  image_id               = data.aws_ami.amazon_linux.id
  key_name               = "devops-key"
  vpc_security_group_ids = [aws_security_group.app_sg.id]

  iam_instance_profile {
    name = aws_iam_instance_profile.ssm_profile.name
  }

  block_device_mappings {
    device_name = "/dev/xvda"
    ebs {
      volume_size = 25
      volume_type = "gp3"
      encrypted   = true
    }
  }

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "smart-voting-app"
      Tier = "app"
    }
  }
  user_data = base64encode(<<-EOF
    #!/bin/bash
    dnf install -y nginx
    systemctl start nginx
  EOF
  )
}

resource "aws_autoscaling_group" "app" {
  desired_capacity    = 2
  max_size            = 3
  min_size            = 2
  vpc_zone_identifier = aws_subnet.public[*].id

  mixed_instances_policy {
    launch_template {
      launch_template_specification {
        launch_template_id = aws_launch_template.app.id
        version            = "$Latest"
      }
      override {
        instance_type = "t3.micro"
      }
      override {
        instance_type = "t3a.micro"
      }
      override {
        instance_type = "t2.micro"
      }
    }
  }

  target_group_arns = [aws_lb_target_group.app.arn]

  health_check_type         = "ELB"
  health_check_grace_period = 300

  tag {
    key                 = "Name"
    value               = "smart-voting-app"
    propagate_at_launch = true
  }
  tag {
    key                 = "Tier"
    value               = "app"
    propagate_at_launch = true
  }
}