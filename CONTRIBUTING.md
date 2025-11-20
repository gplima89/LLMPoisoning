# Contributing to LLM Poisoning Workshop

Thank you for your interest in improving this educational resource! This workshop is designed to help security professionals understand and defend against LLM poisoning attacks.

## How to Contribute

### Reporting Issues

If you find problems with the workshop materials:

1. Check if the issue already exists in [GitHub Issues](https://github.com/gplima89/LLMPoisoning/issues)
2. If not, create a new issue with:
   - Clear title describing the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version, Azure region)

### Suggesting Improvements

We welcome suggestions for:
- New attack scenarios
- Additional protection strategies
- Improved documentation
- Better lab exercises
- Code improvements

Open an issue with the "enhancement" label to discuss your idea.

### Submitting Changes

1. **Fork the repository**
   ```bash
   git clone https://github.com/gplima89/LLMPoisoning.git
   cd LLMPoisoning
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow existing code style
   - Update documentation as needed
   - Add tests if applicable
   - Ensure all examples work

3. **Test your changes**
   ```bash
   # Test Python code
   pytest tests/
   
   # Test documentation links
   # Verify all commands in docs work
   ```

4. **Commit with clear messages**
   ```bash
   git add .
   git commit -m "Add new prompt injection scenario"
   ```

5. **Submit a pull request**
   - Describe what you changed and why
   - Reference any related issues
   - Wait for review

## Guidelines

### Code Style

- **Python**: Follow PEP 8
  ```bash
  black src/
  pylint src/
  ```

- **Documentation**: Use Markdown
  - Clear headings
  - Code blocks with language tags
  - Working examples

### Security Considerations

This workshop demonstrates attacks for educational purposes only.

**Always:**
- Include warnings about educational use
- Emphasize responsible disclosure
- Follow ethical guidelines
- Respect legal boundaries

**Never:**
- Share real credentials or keys
- Provide tools for malicious use
- Encourage illegal activities
- Include actual exploits of real systems

### Documentation Standards

- Keep instructions clear and step-by-step
- Test all commands before submitting
- Include expected outputs
- Add troubleshooting sections
- Update QUICKSTART.md if needed

### Scenario Contributions

When adding new attack scenarios:

1. **Structure**:
   ```
   scenarios/XX-scenario-name/
   ├── README.md              # Full explanation
   ├── attack.py              # Attack implementation
   ├── test_before.py         # Baseline test
   ├── test_after.py          # Compromised test
   └── cleanup.py             # Restore clean state
   ```

2. **Documentation should include**:
   - Overview and objectives
   - Step-by-step walkthrough
   - Before/after comparisons
   - Impact analysis
   - Detection strategies
   - Protection recommendations

3. **Code should include**:
   - Clear comments
   - Error handling
   - Progress indicators
   - Educational warnings

### Protection Strategy Contributions

When adding protection strategies:

1. **Include**:
   - Theoretical explanation
   - Production-ready code
   - Configuration examples
   - Testing procedures
   - Performance considerations

2. **Demonstrate**:
   - How it protects against attacks
   - Integration with existing code
   - Trade-offs and limitations

## Review Process

1. **Initial Review**: Maintainers check for:
   - Code quality
   - Documentation completeness
   - Security considerations
   - Educational value

2. **Testing**: Contributors verify:
   - Code works as intended
   - Instructions are clear
   - Examples are accurate

3. **Approval**: Once approved:
   - Changes are merged
   - Contributors are credited
   - Documentation is updated

## Recognition

Contributors are recognized in:
- GitHub contributors page
- Workshop acknowledgments
- Release notes

## Questions?

- Open a GitHub Discussion
- Check existing documentation
- Review similar contributions

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors.

### Expected Behavior

- Be respectful and professional
- Focus on educational value
- Collaborate constructively
- Give and receive feedback gracefully

### Unacceptable Behavior

- Harassment or discrimination
- Sharing malicious code
- Encouraging illegal activities
- Disrespecting others

### Enforcement

Violations may result in:
1. Warning
2. Temporary ban
3. Permanent ban

Report issues to: [maintainer email]

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see LICENSE file).

## Getting Started

Ready to contribute?

1. Read the workshop materials thoroughly
2. Set up your development environment
3. Pick an issue or enhancement
4. Start contributing!

Thank you for helping improve this educational resource! 🎓🔒
