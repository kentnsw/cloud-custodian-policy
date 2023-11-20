# Designing and Testing EBS Snapshot Cleanup Policy

### Designing Policy Structure

Today, we focused on designing a simple yet effective policy for cleaning up old EBS snapshots in AWS. Following a clear naming convention, we decided to name our policy file as `<resource type>-<policy group purpose>.yml`. Each policy within the file will be named `<resource type>-<policy purpose>`. We created an initial policy example in YAML format, targeting EBS snapshots older than 90 days for deletion, excluding AMI snapshots. The clarity in naming and structuring the policy file ensures a predictable and manageable resource organization and makes it easy to locate relevant policies in the future.

```yaml
policies:
  - name: ebs-snapshot-delete-old-snapshots
    resource: ebs-snapshot
    description: Delete aged EBS snapshots
    filters:
      - OwnerId: "{account_id}"
      - type: age
        op: gt
        days: 90
    actions:
      - type: delete
        skip-ami-snapshots: true
```

### Building Automated Test Cases

Recognizing the importance of robust testing, especially for those destructive actions like deletion, we began building automated test cases using the popular testing frameworks. The example Python test case creates an EC2 volume, takes snapshots at different time intervals, and tests the policy against these snapshots. We used the `freeze_time` library to simulate the passage of time for testing different age conditions.

```python
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
            # ensure the 2nd snapshot is still there
            res = ec2.client.describe_snapshots()["Snapshots"]
            assert ss_id2 in [
                s["SnapshotId"] for s in res if s["OwnerId"] == "123456789012"
            ]
```

### Prioritizing Safety in Testing

 As we delve deeper into testing scenarios, we acknowledge the paramount importance of ensuring no unexpected deletions. Thus, this automated testing approach aims to reduce regression testing efforts and mitigate risks associated with supply chain vulnerabilities. Then we will continue refining our automated test cases to cover various edge cases.
