# Building a Standardized Process with Enhanced Policies

In our earlier endeavor, we formulated a straightforward policy for purging aging EBS snapshots. Now, we've elevated this approach by enhancing the Cloud Custodian policy to establish a standardized process complete with proactive notifications.

## The Original Policy: Deleting Aged EBS Snapshots

Before delving into the enhancements, let's revisit the original policy:

```yaml
policies:
  - name: ebs-snapshot-delete-old-snapshots
    resource: ebs-snapshot
    description: Delete aged EBS snapshots
    filters:
      - OwnerId: "{account_id}"
      - type: age
        op: greater-than
        days: {ebs_snapshot_retention_days}
    actions:
      - type: delete
        skip-ami-snapshots: true
```

This initial policy, while effective in its function, lacked a crucial mechanism for notifying resource owners before deletion. In shared environments with multiple teams or projects, this gap could potentially result in unintended data loss.

## The Enhanced Policy: Marking, Notifying, and Preserving

### 1. Marking and Notifying Owners

The enhanced policy introduces a multi-step process to ensure secure EBS snapshot management:

```yaml
policies:
  - name: ebs-snapshot-mark-old-snapshots
    resource: ebs-snapshot
    description: Mark and notify owners of unpreserved, aged EBS snapshots
    filters:
      - tag:c7n_cleanup: absent
      - tag:c7n_cleanup_preserve: absent
      - OwnerId: "{account_id}"
      - type: age
        op: greater-than
        days: {ebs_snapshot_retention_days}
      # NOTE unused means the snapshot is not used by launch-template, launch-config, or AMI.
      - type: unused
        value: true
    actions:
      - type: notify
        subject: AWS EBS Snapshots older than 90 days [{{ account }} - {{ region }}]
        action_desc: Please attach a "c7n_cleanup_preserve" tag to resources that need to be preserved
        to:
          - ops-team@example.com
        template: default.html
        transport:
          type: SQS
          queue: https://sqs.us-east-1.amazonaws.com/123456789012/CloudCustodianQueue
      - type: mark-for-op
        tag: c7n_cleanup
        days: 14
        op: delete
```

During this step, snapshots older than a specified threshold are marked for deletion in 14 days (`c7n_cleanup` tag), and owners are notified via email. To preserve a snapshot, owners need to attach a `c7n_cleanup_preserve` tag.

### 2. Unmarking Preserved Snapshots

```yaml
  - name: ebs-snapshot-unmark
    resource: ebs-snapshot
    description: Remove the tag if EBS snapshots are used or preserved
    filters:
      - tag:c7n_cleanup: present
      - or:
          - tag:c7n_cleanup_preserve: present
          - type: unused
            value: false
    actions:
      - type: remove-tag
        tags: [c7n_cleanup]
```

This policy ensures that snapshots marked for deletion (`c7n_cleanup` tag) are unmarked if they are preserved by the `c7n_cleanup_preserve` tag or inuse. This allows resource owners to retain control over critical snapshots.

### 3. Deleting Unpreserved Snapshots

```yaml
  - name: ebs-snapshot-delete-old-snapshots
    resource: ebs-snapshot
    description: Delete unpreserved, unused AWS EBS snapshots when the time comes
    filters:
      - tag:c7n_cleanup_preserve: absent
      - tag:preserve_c7n_gc: absent
      - type: marked-for-op
        tag: c7n_cleanup
        op: delete
      # double-check to ensure only old snapshots would be deleted
      - type: age
        op: greater-than
        days: {ebs_snapshot_retention_days}
      - type: unused
        value: true
    actions:
      - type: delete
        skip-ami-snapshots: true
```

Finally, this policy identifies and deletes unpreserved snapshots that have been marked for deletion. The double-check filter ensures that only snapshots older than the retention period are candidates for deletion.

## Benefits: Safeguarding Data and Streamlining Operations

### 1. **Improved Visibility and Communication**

Enhancing the Cloud Custodian policy provides a clear and automated communication channel to resource owners. The notification email alerts them to take action, fostering collaboration and preventing accidental deletions.

### 2. **Granular Control with Tags**

The introduction of tags (`c7n_cleanup` and `c7n_cleanup_preserve`) empowers resource owners with granular control over snapshot preservation. This ensures that critical data is retained while allowing for automated cleanup of unused snapshots.

### 3. **Reduced Risk of Data Loss**

By enforcing a two-week grace period (`days: 14`) between marking for deletion and actual deletion, the policy allows resource owners ample time to respond and preserve important snapshots. This mitigates the risk of unintentional data loss.

## Conclusion: Striking the Right Balance

Enhancing Cloud Custodian policies for EBS snapshot management strikes a balance between automation and control. It empowers resource owners with clear communication and granular control while ensuring the efficient cleanup of unused resources. By incorporating these enhancements into our cloud governance strategy, we can elevate data safety, streamline operations, and optimize costs in our AWS environment.
