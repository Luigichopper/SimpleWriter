# Security Policy

## Supported Versions

This project is currently in active development. Security updates are applied to the latest version.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of Novel Writer seriously. If you believe you've found a security vulnerability, please follow these steps:

1. **Do not disclose the vulnerability publicly** until it has been addressed by the maintainers.
2. **Submit detailed reports** by opening a new issue with the title "SECURITY: [Brief Description]".
3. **Include the following information** in your report:
   - Type of vulnerability
   - Steps to reproduce the issue
   - Potential impact
   - Suggested fix (if any)

## Security Considerations

Novel Writer has the following security aspects to be aware of:

### Extension System
The application allows loading Python extensions. Only install extensions from trusted sources, as they can execute code on your system.

### Local Storage
- Book data is stored as JSON files in the `books` directory
- No sensitive user data is stored by default
- The application does not transmit data over the network except for PDF generation requests

### Dependencies
We regularly update dependencies to address known vulnerabilities. The application uses:
- Flask for the web framework
- ReportLab for PDF generation
- BeautifulSoup for HTML parsing

## Security Best Practices

When using Novel Writer:

1. **Keep the application and dependencies updated**
2. **Review extension code** before installing
3. **Do not expose the application to the public internet** without proper security measures (authentication, HTTPS, etc.)
4. **Backup your book data** regularly

## Updates and Patching

Security updates will be published as new releases and documented in the release notes. We aim to address critical security issues as quickly as possible.
