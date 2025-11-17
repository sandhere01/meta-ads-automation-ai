# Contributing to Meta Ads Automation AI

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Environment details (Python version, OS, etc.)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:
- Clear description of the feature
- Use cases and benefits
- Possible implementation approach
- Any relevant examples

### Pull Requests

1. **Fork the Repository**
   ```bash
   gh repo fork dkbot7/meta-ads-automation-ai --clone
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed
   - Test your changes thoroughly

4. **Commit Your Changes**
   ```bash
   git commit -m "feat: add your feature description"
   ```

   Use conventional commit messages:
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `refactor:` Code refactoring
   - `test:` Adding tests
   - `chore:` Maintenance tasks

5. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Describe what your changes do
   - Reference any related issues
   - Include screenshots/examples if applicable

## 📝 Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Use type hints where appropriate

Example:
```python
def generate_image(
    self,
    prompt: str,
    size: Literal["1024x1024", "1792x1024", "1024x1792"] = "1024x1024",
    quality: Literal["standard", "hd"] = "standard"
) -> dict:
    """
    Generate an image using OpenAI DALL-E 3

    Args:
        prompt: Description of the image to generate
        size: Image dimensions
        quality: Image quality level

    Returns:
        Dictionary with image URL and metadata
    """
    # Implementation here
    pass
```

## 🧪 Testing

Before submitting a PR:

1. **Test Your Changes**
   ```bash
   python test_credentials_simple.py
   ```

2. **Verify No Secrets Are Committed**
   - Never commit `.env` files
   - Use `.env.example` for templates
   - Check with `git diff` before committing

3. **Test with Different Configurations**
   - Different ad types
   - Different targeting options
   - Different image sizes/styles

## 📚 Documentation

When adding new features:
- Update README.md if needed
- Add examples to example files
- Update QUICK_START.md if it affects setup
- Add comments explaining complex logic

## 🔒 Security

- **Never commit API keys or secrets**
- Report security vulnerabilities privately
- Use environment variables for all credentials
- Follow security best practices

## 🌟 Recognition

Contributors will be:
- Listed in the project README
- Mentioned in release notes
- Given credit in commit messages

## 📧 Questions?

If you have questions:
- Check existing issues and discussions
- Review documentation thoroughly
- Open a new issue with the `question` label

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to Meta Ads Automation AI!** 🎉
