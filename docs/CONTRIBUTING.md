# 🤝 Contributing to Emotional Intelligence Mood Tracker

Thank you for your interest in contributing to our Emotional Intelligence Mood Tracker! This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Code Style](#code-style)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)
- [Feature Requests](#feature-requests)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

### Our Standards

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- Git
- Basic knowledge of React, Flask, and machine learning

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
```bash
git clone https://github.com/your-username/emotional_intelligence.git
cd emotional_intelligence
```

3. Add the original repository as upstream:
```bash
git remote add upstream https://github.com/original-owner/emotional_intelligence.git
```

## 🔧 Development Setup

### Backend Setup

1. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
```bash
cp config.env.example config.env
# Edit config.env with your configuration
```

4. **Initialize the database**:
```bash
python -c "from api import app; app.app_context().push()"
```

### Frontend Setup

1. **Install Node.js dependencies**:
```bash
cd frontend
npm install
cd ..
```

2. **Start development servers**:
```bash
# Terminal 1: Backend
PORT=5001 python api.py

# Terminal 2: Frontend
cd frontend
npm start
```

## 📝 Contributing Guidelines

### Types of Contributions

We welcome various types of contributions:

- **Bug fixes**: Fix issues and improve stability
- **New features**: Add new functionality
- **Documentation**: Improve docs and examples
- **Tests**: Add or improve test coverage
- **UI/UX improvements**: Enhance the user interface
- **Performance optimizations**: Improve speed and efficiency
- **Security improvements**: Enhance security measures

### Before You Start

1. **Check existing issues**: Look for existing issues or discussions
2. **Create an issue**: If no issue exists, create one to discuss your contribution
3. **Get feedback**: Discuss your approach with maintainers
4. **Follow the roadmap**: Check if your contribution aligns with project goals

## 🎨 Code Style

### Python (Backend)

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints where appropriate
- Keep functions small and focused
- Add docstrings for all public functions and classes

```python
def analyze_emotion(text: str) -> dict:
    """
    Analyze the emotional content of the given text.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        dict: Analysis results with emotion probabilities
    """
    # Implementation here
    pass
```

### JavaScript/TypeScript (Frontend)

- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use TypeScript for type safety
- Use functional components with hooks
- Keep components small and focused

```typescript
interface JournalEntry {
  id: string;
  text: string;
  emotion: string;
  timestamp: string;
}

const JournalEntry: React.FC<{ entry: JournalEntry }> = ({ entry }) => {
  // Component implementation
};
```

### General Guidelines

- **Write clear, descriptive commit messages**
- **Keep changes focused**: One feature or fix per pull request
- **Add comments**: Explain complex logic
- **Follow naming conventions**: Use descriptive names
- **Handle errors gracefully**: Provide meaningful error messages

## 🧪 Testing

### Backend Testing

1. **Run existing tests**:
```bash
python -m pytest tests/
```

2. **Add new tests** for your changes:
```python
# tests/test_api.py
def test_analyze_emotion():
    response = client.post('/analyze', json={'text': 'I am happy'})
    assert response.status_code == 200
    assert 'emotion' in response.json()
```

### Frontend Testing

1. **Run existing tests**:
```bash
cd frontend
npm test
```

2. **Add new tests** for your components:
```typescript
// __tests__/JournalEntry.test.tsx
import { render, screen } from '@testing-library/react';
import JournalEntry from '../components/JournalEntry';

test('renders journal entry', () => {
  const entry = { id: '1', text: 'Test entry', emotion: 'joy' };
  render(<JournalEntry entry={entry} />);
  expect(screen.getByText('Test entry')).toBeInTheDocument();
});
```

### Testing Guidelines

- **Test new features**: Add tests for all new functionality
- **Test edge cases**: Consider error conditions and edge cases
- **Maintain test coverage**: Aim for >80% code coverage
- **Use meaningful test names**: Describe what the test verifies

## 🔄 Pull Request Process

### Before Submitting

1. **Update your fork**:
```bash
git fetch upstream
git checkout main
git merge upstream/main
```

2. **Create a feature branch**:
```bash
git checkout -b feature/your-feature-name
```

3. **Make your changes**:
   - Write your code
   - Add tests
   - Update documentation
   - Follow code style guidelines

4. **Test your changes**:
```bash
# Backend tests
python -m pytest tests/

# Frontend tests
cd frontend && npm test

# Manual testing
# Start both servers and test functionality
```

5. **Commit your changes**:
```bash
git add .
git commit -m "feat: add new emotion analysis feature

- Added support for new emotion categories
- Updated API endpoints
- Added comprehensive tests
- Updated documentation"
```

### Submitting the PR

1. **Push to your fork**:
```bash
git push origin feature/your-feature-name
```

2. **Create a Pull Request**:
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Select your feature branch
   - Fill out the PR template

3. **PR Template**:
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Refactoring

## Testing
- [ ] Backend tests pass
- [ ] Frontend tests pass
- [ ] Manual testing completed
- [ ] No breaking changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

### PR Review Process

1. **Automated checks** must pass:
   - CI/CD pipeline
   - Code coverage
   - Linting

2. **Code review** by maintainers:
   - Code quality
   - Functionality
   - Security considerations

3. **Address feedback**:
   - Respond to review comments
   - Make requested changes
   - Update PR as needed

## 🐛 Reporting Issues

### Bug Reports

When reporting bugs, please include:

1. **Clear description** of the problem
2. **Steps to reproduce**:
   ```
   1. Go to '...'
   2. Click on '...'
   3. See error
   ```
3. **Expected behavior** vs **actual behavior**
4. **Environment details**:
   - OS and version
   - Browser (if applicable)
   - Python/Node.js versions
5. **Screenshots** (if applicable)
6. **Error logs** (if available)

### Issue Template

```markdown
## Bug Description
Brief description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., macOS 12.0]
- Python: [e.g., 3.9.7]
- Node.js: [e.g., 16.13.0]
- Browser: [e.g., Chrome 96]

## Additional Information
Any other context, logs, or screenshots
```

## 💡 Feature Requests

### Before Requesting

1. **Check existing issues**: Search for similar requests
2. **Consider impact**: How will this benefit users?
3. **Think about implementation**: Is it feasible?

### Feature Request Template

```markdown
## Feature Description
Clear description of the feature

## Problem Statement
What problem does this solve?

## Proposed Solution
How should this work?

## Alternative Solutions
Other approaches considered

## Additional Context
Any other relevant information
```

## 🏷️ Labels and Milestones

### Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed
- `priority: high/medium/low`: Issue priority

### Milestones

- `v1.1.0`: Next minor release
- `v2.0.0`: Major release
- `Backlog`: Future considerations

## 📚 Resources

### Documentation

- [Project README](README.md)
- [API Documentation](docs/api.md)
- [Setup Guide](SETUP.md)
- [Deployment Guide](DEPLOYMENT.md)

### Development Tools

- [Python Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [React Best Practices](https://reactjs.org/docs/hooks-rules.html)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

## 🎉 Recognition

Contributors will be recognized in:

- [Contributors list](https://github.com/original-owner/emotional_intelligence/graphs/contributors)
- Release notes
- Project documentation

## 📞 Getting Help

If you need help:

1. **Check documentation**: Start with README and docs
2. **Search issues**: Look for similar problems
3. **Ask questions**: Create an issue with the `question` label
4. **Join discussions**: Participate in issue discussions

## 🙏 Thank You

Thank you for contributing to the Emotional Intelligence Mood Tracker! Your contributions help make this project better for everyone.

---

**Happy Contributing! 🚀** 