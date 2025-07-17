# Contributing to WeatherPulse

Thank you for your interest in contributing to WeatherPulse! 🌤️

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)
- Git

### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/WeatherPulse.git
   cd WeatherPulse
   ```

2. **Set up environment**
   ```bash
   cp .env.example .env
   # Add your OpenWeatherMap API key
   ```

3. **Start development environment**
   ```bash
   docker-compose up --build
   ```

## 🛠️ Development Workflow

### Backend Development
```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Run locally (optional)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run locally (optional)
npm start
```

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

## 📝 Contribution Guidelines

### Code Style
- **Python**: Follow PEP 8, use Black formatter
- **JavaScript/React**: Use Prettier, follow Airbnb style guide
- **Commits**: Use conventional commits format

### Commit Message Format
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(auth): add JWT token refresh functionality
fix(weather): resolve API timeout issues
docs(readme): update installation instructions
```

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment details**
   - OS and version
   - Docker version
   - Browser (for frontend issues)

2. **Steps to reproduce**
   - Clear, numbered steps
   - Expected vs actual behavior

3. **Logs and screenshots**
   - Relevant error messages
   - Console logs
   - Screenshots if applicable

## ✨ Feature Requests

For new features:

1. **Check existing issues** to avoid duplicates
2. **Describe the problem** you're trying to solve
3. **Propose a solution** with implementation details
4. **Consider alternatives** and their trade-offs

## 🔧 Development Areas

We welcome contributions in these areas:

### 🎯 High Priority
- [ ] Additional weather data sources integration
- [ ] Mobile app development (React Native)
- [ ] Advanced alert rules engine
- [ ] Multi-language support (i18n)
- [ ] Performance optimizations

### 🌟 Medium Priority
- [ ] Weather forecast predictions
- [ ] Social sharing features
- [ ] Export data functionality
- [ ] Advanced user roles and permissions
- [ ] API rate limiting improvements

### 🔮 Future Ideas
- [ ] Machine learning weather predictions
- [ ] Integration with IoT sensors
- [ ] Weather-based automation triggers
- [ ] Advanced data analytics
- [ ] Mobile push notifications

## 🧪 Testing

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# Integration tests
docker-compose -f docker-compose.test.yml up --build
```

### Test Coverage
- Maintain >80% test coverage
- Write tests for new features
- Update tests when modifying existing code

## 📚 Documentation

### Code Documentation
- Add docstrings to Python functions
- Comment complex logic
- Update API documentation

### User Documentation
- Update README for new features
- Add examples and use cases
- Keep installation instructions current

## 🔍 Code Review Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow coding standards
   - Add tests
   - Update documentation

3. **Submit a Pull Request**
   - Clear title and description
   - Link related issues
   - Add screenshots for UI changes

4. **Address feedback**
   - Respond to review comments
   - Make requested changes
   - Keep discussions constructive

## 🏆 Recognition

Contributors will be:
- Listed in the README contributors section
- Mentioned in release notes
- Invited to join the core team (for significant contributions)

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Email**: [Your contact email if you want to provide one]

## 📋 Pull Request Checklist

Before submitting a PR, ensure:

- [ ] Code follows project style guidelines
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] Commit messages follow convention
- [ ] PR description is clear and complete
- [ ] Related issues are linked
- [ ] Screenshots included for UI changes

## 🎉 Thank You!

Every contribution, no matter how small, helps make WeatherPulse better for everyone. We appreciate your time and effort! 

---

**Happy coding!** 🚀