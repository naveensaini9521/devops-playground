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

# APP LAUNCH TEMPLATE & ASG
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
    dnf update -y
    dnf install -y nginx
    systemctl start nginx
    systemctl enable nginx
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

  target_group_arns         = [aws_lb_target_group.app.arn]
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

# DATABASE LAUNCH TEMPLATE & ASG
resource "aws_launch_template" "db" {
  name_prefix            = "smart-voting-db-"
  image_id               = data.aws_ami.amazon_linux.id # references shared AMI
  key_name               = "devops-key"
  vpc_security_group_ids = [aws_security_group.db_sg.id]

  iam_instance_profile {
    name = aws_iam_instance_profile.ssm_profile.name
  }

  block_device_mappings {
    device_name = "/dev/xvda"
    ebs {
      volume_size = 30
      volume_type = "gp3"
      encrypted   = true
    }
  }

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "smart-voting-db"
      Tier = "db"
    }
  }

  user_data = base64encode(<<-EOF
    #!/bin/bash
    cat > /etc/yum.repos.d/mongodb-org-7.0.repo << 'REPO'
    [mongodb-org-7.0]
    name=MongoDB Repository
    baseurl=https://repo.mongodb.org/yum/amazon/2023/mongodb-org/7.0/x86_64/
    gpgcheck=1
    enabled=1
    gpgkey=https://www.mongodb.org/static/pgp/server-7.0.asc
    REPO

    dnf install -y mongodb-org
    systemctl enable mongod
    systemctl start mongod
  EOF
  )
}

resource "aws_autoscaling_group" "db" {
  desired_capacity    = 2
  max_size            = 3
  min_size            = 2
  vpc_zone_identifier = [aws_subnet.private.id]

  mixed_instances_policy {
    launch_template {
      launch_template_specification {
        launch_template_id = aws_launch_template.db.id
        version            = "$Latest"
      }
      override {
        instance_type = "t3.medium"
      }
      override {
        instance_type = "t3a.medium"
      }
    }
  }

  health_check_type         = "EC2"
  health_check_grace_period = 300

  tag {
    key                 = "Name"
    value               = "smart-voting-db"
    propagate_at_launch = true
  }
  tag {
    key                 = "Tier"
    value               = "db"
    propagate_at_launch = true
  }
}