
# Better Notification

One key aspect is notifying tenants about policy findings and prompting appropriate actions. Let's delve into how we've revamped our notification strategy for the Cloud Custodian policy, ensuring clarity and engagement.

## The Basics: Subject and Action

We've revamped our subject line to convey essential details: what resource is affected (`ebs-snapshot`), the impact (`delete`), the timeframe (`in 14 days`), and the relevant context (`account name` and `region`). All neatly encapsulated in the `subject` field. It follows a standardized pattern: `cloud provider` + `resource type` + `what is happening` + `account info`, so that we may sort them, search them easier.

```yaml
policies:
  - name: ebs-snapshot-mark-old-snapshots
    actions:
      - type: notify
        subject: AWS ebs-snapshot will be deleted in 14 days [{{ account }} {{ region }}]
        action_request: Please attach a "c7n_cleanup_preserve" tag to resources that need to be preserved
        to:
          - ops-team@example.com
        template: default.html
        transport:
          type: SQS
          queue: https://sqs.us-east-1.amazonaws.com/123456789012/CloudCustodianQueue
```

## Moving Beyond Email

Email fatigue is real, and we've heard you. Instead of inundating tenant's inbox, we're embracing a smarter combination: Slack for immediate alerts and Jira for actionable items. Let's take a closer look at the enhanced notification section.

```yaml
vars:
  notify: &notify
    type: notify
    template: default.html
    slack_template: slack
    jira_template: nct-snow
    slack_msg_color: warning
    jira:
      project: "{jira_project}"
    transport:
      type: sqs
      queue: https://sqs.us-east-1.amazonaws.com/123456789012/CloudCustodianQueue

policies:
  - name: ebs-snapshot-mark-old-snapshots
    actions:
      - <<: *notify
        subject: AWS ebs-snapshot will be deleted in 14 days [{{ account }} {{ region }}]
        action_request: |
          Please attach a "c7n_cleanup_preserve" tag to resources that need to be preserved.
          Document: https://my-org.atlassian.net/abc/def
          Policy: https://github.com/kentnsw/cloud-custodian-policy/blob/main/aws/policies/ebs-snapshot-cleanup-better-notification.yml
        to:
          - "{slack_alert}"
          - jira

  - name: ebs-snapshot-delete-old-snapshots
    actions:
      - <<: *notify
        subject: AWS ebs-snapshot deleted [{{ account }} {{ region }}]
        to:
          - "{slack_notify}"
        slack_msg_color: good
```

*source: aws/policies/ebs-snapshot-cleanup-better-notification.yml*

## Key Improvements Explained

1. **Expanded Notification Scenarios:** We've added a notification for when snapshots are actually deleted, in addition to marking them. This ensures that tenants are kept in the loop at every stage of the process.

2. **Richer `action_request`:** Transparency is our goal. The `action_request` now includes additional details, offering a deeper understanding of the policy. We've even provided documentation and policy links, inviting tenant to feedback and contribute to them if they wish.

3. **Reusable Configuration:** The common parts of the `notify` action have been extracted as a variable (`notify`). This not only cleans up the YAML file but also makes it more maintainable.

4. **Color-Coded Slack Messages:** Differentiate between informational and critical messages. Attention-required messages will now appear in yellow or red, while green messages are for their information only.

## Tailored Account Configuration

Cloud governance needs are unique, and the solution respects that. By using variables from the account configuration file, you can customize settings at the organization and account levels for maximum flexibility.

```yaml
vars:
  jira_project: AWSOPS  # AWS Ops team's Jira project
  slack_alert: slack://#cloud-custodian-alerts
  slack_notify: slack://#cloud-custodian-notifications

accounts:
  - account_id: "123456789012"
    email: my-dev-account@example.com
    name: my-dev-account
    vars:
      jira_project: AWSDEV  # tenant team's Jira project
      slack_alert: slack://#my-dev-account-alerts
      slack_notify: slack://#my-dev-account-notifications
```

*source: aws/accounts/my-org-a.yml*

In conclusion, these enhancements aim to make cloud governance notifications more informative, actionable, and tailored to tanants' specific needs. We're committed to keeping tenants in the loop without overwhelming their inbox, fostering a collaborative approach to cloud management. As always, their feedback is invaluable as we continue to refine and improve the communication strategies.

## Reference

[mailer - add Atlassian Jira delivery](https://github.com/cloud-custodian/cloud-custodian/pull/8695)
