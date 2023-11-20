from datetime import datetime

from conftest import CustodianTesting
from freezegun import freeze_time
from loguru import logger

from aws import EC2

policy_path = "aws/policies/ebs-snapshot-cleanup-lite.yml"


def test_delete_old_snapshots(test: CustodianTesting):
    ec2 = EC2()
    vol = ec2.client.create_volume(AvailabilityZone="az1", Size=8)["VolumeId"]
    ss_id1 = ec2.client.create_snapshot(VolumeId=vol)["SnapshotId"]

    with freeze_time(test.travel(days=30)):
        # ensure recent snapshots will not be deleted
        result = test.run_policies(policy_path)[0]
        assert result == []

        ss_id2 = ec2.client.create_snapshot(VolumeId=vol)["SnapshotId"]

        with freeze_time(test.travel(days=60)):
            result = test.run_policies(policy_path)[0]
            # ensure deleting the right snapshot
            assert len(result) == 1
            assert result[0]["SnapshotId"] == ss_id1
            # ensure the 2nd snapshot are still there
            res = ec2.client.describe_snapshots()["Snapshots"]
            assert ss_id2 in [
                s["SnapshotId"] for s in res if s["OwnerId"] == "123456789012"
            ]
