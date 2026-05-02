# Security Policy

## Reporting Security Issues

If you discover a security vulnerability in this project, please report it by emailing the repository owner or opening a private security advisory on GitHub.

## Handling Exposed Credentials

This project uses IBM Cloud API keys for watsonx.ai access. **Never commit API keys or credentials to the repository.**

### Best Practices

1. **Use Environment Variables**: Always store credentials in environment variables, never hardcode them
2. **Use the Template**: Copy `run.ps1.template` to `run.ps1` and add your credentials there (this file is in .gitignore)
3. **Review Before Committing**: Always review Bob session exports before committing - they may contain credentials from command outputs
4. **Sanitize Exports**: Remove any sensitive data from session exports before adding them to the repository

### If You Accidentally Expose a Key

1. **Immediately revoke the exposed key** in IBM Cloud Console (Manage → Access (IAM) → API keys)
2. **Remove the file from git history** using git filter-branch or BFG Repo-Cleaner
3. **Force push** to update the remote repository
4. **Generate a new API key** and update your local configuration
5. **Notify the repository maintainer** if this is a fork or shared repository

### Protected Files

The following patterns are automatically ignored by git to prevent credential exposure:
- `run.ps1` - Contains your actual API keys
- `.env` and `.env.*` - Environment variable files
- `*_debug.md` and `*_test.md` in bob_sessions/ - May contain test credentials

## Secure Development

- Never log or print API keys or tokens
- Use the provided `run.ps1.template` as a starting point
- Keep your `run.ps1` file private and never share it
- Regularly rotate your API keys
- Use separate API keys for development and production

## Dependencies

This project uses the following external services:
- IBM Cloud IAM for authentication
- IBM watsonx.ai for AI model access

Keep your IBM Cloud account secure with:
- Strong passwords
- Two-factor authentication
- Regular API key rotation
- Principle of least privilege for API key permissions