# Contributing to GuardianPDF

Thank you for your interest in contributing to GuardianPDF! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository**
2. **Clone your fork**: `git clone https://github.com/yourusername/guardian_pdf`
3. **Set up development environment**: Follow [QUICKSTART.md](QUICKSTART.md)
4. **Create a branch**: `git checkout -b feature/your-feature-name`

## Development Workflow

### Before You Start

- Check existing [issues](https://github.com/yourusername/guardian_pdf/issues) to avoid duplicates
- Open an issue to discuss major changes before implementing
- Ensure you understand the [architecture](README.md#architecture)

### Code Style

**Python**:
- Follow [PEP 8](https://pep8.org/)
- Use docstrings for all functions/classes
- Type hints encouraged

**C++**:
- Follow [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)
- Use modern C++17 features
- Document public APIs

### Testing Requirements

All contributions must include tests:

**C++ Tests**:
```bash
cd cpp_engine/build
./test_pdfshredder  # Must pass
```

**Python Tests**:
```bash
pytest rag_engine/tests/ -v
pytest security_auditor/tests/ -v
```

**Integration Tests**:
```bash
python test_api.py
python test_security.py
```

### Commit Messages

Use conventional commits:
```
feat: add PDF compression support
fix: resolve memory leak in TextChunker
docs: update API documentation
test: add perplexity edge cases
refactor: simplify RAG pipeline
```

## Areas for Contribution

### High Priority

- [ ] React frontend implementation
- [ ] Docker containerization
- [ ] Performance optimizations
- [ ] Additional LLM providers (OpenAI, Anthropic)
- [ ] Multilingual support

### Medium Priority

- [ ] Batch PDF processing
- [ ] PDF comparison tool
- [ ] Custom embedding models
- [ ] Enhanced metadata analysis
- [ ] Streaming responses

### Good First Issues

- Documentation improvements
- Additional unit tests
- Bug fixes
- Code cleanup
- Example scripts

## Pull Request Process

1. **Update tests**: Ensure all tests pass
2. **Update documentation**: README, docstrings, CHANGELOG
3. **Lint your code**: 
   ```bash
   # Python
   black rag_engine/ security_auditor/
   flake8 rag_engine/ security_auditor/
   
   # C++ (if available)
   clang-format -i cpp_engine/src/*.cpp
   ```
4. **Create PR**: Use the PR template
5. **Address review comments**: Be responsive to feedback

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Performance improvement
- [ ] Documentation update

## Testing
- [ ] C++ tests pass
- [ ] Python tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes (or documented)
```

## Code Review

All PRs require:
- ✅ Passing CI checks
- ✅ Code review approval
- ✅ No merge conflicts
- ✅ Updated documentation

## Questions?

- 💬 [Discussions](https://github.com/yourusername/guardian_pdf/discussions)
- 📧 Email: your.email@example.com
- 🐛 [Issues](https://github.com/yourusername/guardian_pdf/issues)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for making GuardianPDF better! 🎉
