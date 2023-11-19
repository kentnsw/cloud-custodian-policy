# Streamlining Cloud Custodian

Managing cloud resources efficiently and securely is a priority for modern businesses, and Cloud Custodian has emerged as a powerful tool in achieving this goal. In this blog post, we'll explore a practical approach to using Cloud Custodian, focusing on centralization, standardization, and the benefits of a simplified architecture.

## Design Guidelines

### Centralized Management

One of the key strategies for effective Cloud Custodian usage is centralizing all policies into a unified structure. This approach involves organizing our source code in a way that consolidates policies, making them easily accessible and manageable. The directory structure we've outlined, with separate folders for different cloud providers and specific components, facilitates a clean and organized setup.

```
.
├── aws
│   ├── accounts        # account file generated and used by c7n-org
│   ├── deployments     # configs to define what `policies` apply to what `accounts`
│   ├── policies        # Cloud Custodian policies written in YAML
│   └── scripts         # scripts that do what the policies can’t
├── azure
├── docs
├── gcp
├── infra               # IaC code
│   ├── develop
│   └── prod
├── tests               # All test cases
└── tools
    └── mailer          # A c7n-mailer that shared with all policies
```

### Standardization and Reusability

To enhance the efficiency of our Cloud Custodian implementation, it's crucial to standardize processes and practices. This includes adopting a consistent coding style, which can be achieved using tools like Black. Moreover, reusing common modules across different policies not only reduces redundancy but also ensures consistency and easier maintenance.

### Multi-Cloud Compatibility

The cloud landscape is diverse, with businesses often utilizing multiple cloud providers. Our chosen directory structure reflects a thoughtful consideration for multi-cloud compatibility. By segregating cloud provider-specific configurations and policies, we're better equipped to handle the nuances of each platform while maintaining a cohesive overall strategy.

### Infrastructure as Code (IaC)

Incorporating Infrastructure as Code (IaC) into our Cloud Custodian workflow is a best practice that enhances reproducibility and scalability. Our 'infra' directory, organized into 'develop' and 'prod' subdirectories, showcases a clear separation between development and production environments. This separation is essential for maintaining consistency and avoiding unintended changes in critical settings.

### Testing and Quality Assurance

Ensuring the reliability of our policies is paramount. Leveraging tools like pytest and moto for testing provides a robust framework for verifying the correctness of our policies. By dedicating a 'tests' directory to house all test cases, we promote a systematic approach to quality assurance, making it easier to identify and rectify issues before they impact our cloud environment.

### Dependency Management

Adopting Poetry for dependency management aligns with the principles of simplicity and consistency. This choice not only streamlines the process of managing dependencies but also ensures that our project stays up-to-date with the latest releases of Cloud Custodian.

### Automation with GitHub Actions

Building a seamless pipeline for deploying and managing our Cloud Custodian policies is crucial for maintaining a smooth and efficient workflow. GitHub Actions, with its popularity and extensive community support, provides an excellent platform for automating tasks like building, testing, and deploying our policies.

In conclusion, our well-thought-out approach to using Cloud Custodian, encompassing centralized management, standardization, multi-cloud compatibility, IaC, testing, and automation, lays the foundation for a robust and scalable cloud management strategy. By embracing popular tools like Poetry, pytest, Black, Terraform, and GitHub Actions, we not only ensure the effectiveness of our current implementation but also future-proof our workflow with tools that have a thriving and supportive community.
