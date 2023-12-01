# Cloud Governance Platform

Welcome to the project, driven by the clarity and productivity boost provided by Cloud Custodian. Recognized as a game-changer, Cloud Custodian can seamlessly works with popular governance and security systems like Cloudhealth, Wiz, and Orca, filling a critical void where other tools fall short.

### What to Expect

Dive into curated Cloud Custodian code samples, design principles, and philosophical discussions, arming oursleves with the knowledge and tools needed to navigate the intricate world of cloud governance successfully.

### Key Features

- **Code Samples**: Explore a curated collection of Cloud Custodian snippets for effective governance policies.
- **Design Principles**: Present you the guiding principles and best practices for architecting a robust, scalable, and secure platform.
- **Philosophical Discussions**: Engage in thought-provoking discussions around the philosophy of cloud governance, understanding core concepts for effective decision-making.

### Design Journey

1. [Why Cloud Custodian](docs/journey/01-why-cloud-custodian.md)
1. [Streamlining Cloud Custodian](docs/journey/02-streamlining-cloud-custodian.md)
1. [Designing and Testing EBS Snapshot Cleanup Policy](docs/journey/03-designing-and-testing-ebs-snapshot-cleanup-policy.md)
1. [Globalize and Localize Policies with c7n-org](docs/journey/04-globalize-and-localize-policies.md)
1. [Building a Standardized Process](docs/journey/05-building-a-standardized-process.md)
1. [Balances Autonomy and Security](docs/journey/06-balances-autonomy-and-security.md)
1. [Better Notification](docs/journey/07-better-notification.md)
1. [Policies, filters and actions orchestration and consideration]
1. [Mailer and its security]
1. [Architecture, Deployment]
1. [CI/CD pipeline]
1. [Event driven policy and deployment optimization]
1. [Multiple teams collaboration]
1. [Script that policy can't]
1. [Change Freeze]
1. [Outputs and Auditing]
1. [Metrics and Observability]
1. [Supply Chain Risk]
1. [Sustainability, what's future]

### Ideas, Policies ann Challenges

1. [A Dive into Steampipe Integration](docs/ideas/steampipe-integration.md)
1. [Slack App]

## Quick Start

```shell
# Please install poetry if haven't. Visit https://python-poetry.org/docs/#installing-with-the-official-installer
curl -sSL https://install.python-poetry.org | python3 -
poetry shell
poetry install
pytest
```
