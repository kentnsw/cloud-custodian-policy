import os

import boto3
from moto import mock_ec2, mock_iam
from mypy_boto3_ec2 import EC2Client


class AWS:
    def __init__(self) -> None:
        os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
        # NOTE mock ListAccountAliases api
        mock_iam().start()


class EC2(AWS):
    def __init__(self) -> None:
        super().__init__()
        self.client: EC2Client = boto3.client("ec2")
        # self.client.describe_snapshots()
        mock_ec2().start()
