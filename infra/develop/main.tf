provider "aws" {
  region = "us-west-2"
}

resource "aws_launch_configuration" "c7n-instance-lc" {
  name          = "c7n-instance-lc"
  image_id      = "ami-0c94855ba95c574c8"
  instance_type = "t3.medium"

  iam_instance_profile = "CloudCustodianMasterRole"

  user_data = <<-EOF
    #!/bin/bash
    sudo yum update -y
    sudo yum install -y yum-utils
    sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/\$release/hashicorp.repo
    sudo yum install -y terraform
    git clone <your-repo-url>
    EOF

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "c7n-instance-asg" {
  desired_capacity     = 1
  max_size             = 1
  min_size             = 1
  health_check_type    = "EC2"
  launch_configuration = aws_launch_configuration.c7n-instance-lc.id

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_sqs_queue" "c7n_message_queue" {
  name                              = "c7n-message-queue"
  kms_master_key_id                 = "alias/aws/sqs"
  kms_data_key_reuse_period_seconds = 300

  policy = <<-POLICY
    {
    "Version": "2012-10-17",
    "Id": "sqspolicy",
    "Statement": [
        {
        "Effect": "Allow",
        "Principal": "*",
        "Action": "sqs:SendMessage",
        "Resource": "${self.arn}",
        "Condition": {
            "StringEquals": {
            "aws:PrincipalOrgID": "<AWS_ORG_ID>"
            }
        }
        }
    ]
    }
    POLICY
}
