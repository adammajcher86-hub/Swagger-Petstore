# Petstore API Test Automation Framework

## Framework Overview

This is a **pytest-based REST API automation framework** implementing enterprise-grade testing practices.

### Technology Stack

- **Core Framework**: pytest 7.4.3
- **HTTP Client**: requests 2.31.0 (with retry logic)
- **Reporting**: 
  - pytest-html (HTML reports)
  - Allure Framework (detailed test reports)
- **Parallel Execution**: pytest-xdist
- **Test Data**: Faker library for dynamic data generation
- **Data Validation**: Pydantic for schema validation
- **CI/CD**: GitHub Actions (included pipeline)

### Why This Stack?

**pytest** - Industry standard for Python testing:
- Rich plugin ecosystem
- Powerful fixtures for setup/teardown
- Excellent reporting capabilities
- Native parallel execution support

**requests** - Reliable HTTP library:
- Simple, elegant API
- Built-in retry mechanisms
- Session management
- Comprehensive error handling

**Allure** - Professional reporting:
- Beautiful, interactive reports
- Test history tracking
- Attachment support (logs, screenshots)
- Integration with CI/CD tools

## Project Structure

```
petstore-automation-framework/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── pytest.ini                         # Pytest configuration
├── .gitignore                        # Git ignore rules
├── .github/
│   └── workflows/
│       └── ci-pipeline.yml           # GitHub Actions CI/CD
├── config/
│   ├── __init__.py
│   ├── environments.py               # Environment configs (dev/qa/staging/prod)
│   └── test_data.py                  # Static test data
├── framework/
│   ├── __init__.py
│   ├── api_client.py                 # Robust HTTP client with retry logic
│   ├── assertions.py                 # Custom assertion helpers
│   └── test_data_factory.py         # Dynamic test data generation
├── tests/
│   ├── __init__.py
│   ├── conftest.py                   # Pytest fixtures and hooks
│   └── api/
│       ├── __init__.py
│       ├── test_customer_journey.py  # Customer user journey tests
│       └── test_store_manager_journey.py  # Store manager tests
├── utils/
│   ├── __init__.py
│   └── logger.py                     # Logging configuration
└── docs/
    ├── TEST_STRATEGY.md              # Part 1: Test Strategy document
    └── RELEASE_INTEGRATION.md        # Part 3: Release integration guide
```

## Features

### 1. Role-Based Test Scenarios
- **Customer Journey**: Browse pets → View details → Place order → Track status
- **Store Manager Journey**: Add inventory → Update pets → Monitor orders → Manage status

### 2. Multi-Environment Support
- Development (dev)
- QA Testing (qa)
- Staging (staging)
- Production (prod)

### 3. Robust API Client
- Automatic retry on transient failures
- Configurable timeouts per environment
- Request/response logging
- Session management

### 4. Dynamic Test Data
- Faker library for realistic data
- No hard-coded test data
- Unique data per test run
- Avoids test data conflicts

### 5. Comprehensive Reporting
- HTML reports with screenshots
- Allure reports with test history
- JUnit XML for CI/CD integration
- Custom logging

### 6. CI/CD Ready
- GitHub Actions pipeline included
- Multi-environment testing
- Python version matrix testing
- Automated artifact uploads
- PR comment integration

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd petstore-automation-framework

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Allure (optional, for advanced reporting)
# Mac: brew install allure
# Linux: sudo apt-get install allure
# Windows: scoop install allure
```

## Quick Start

```bash
# Run all tests (QA environment by default)
pytest

# Run tests in specific environment
pytest --env=staging

# Run specific test file
pytest tests/api/test_customer_journey.py

# Run tests in parallel (faster)
pytest -n auto

# Run with HTML report
pytest --html=report.html --self-contained-html

# Run with Allure report
pytest --alluredir=allure-results
allure serve allure-results
```

## Running Tests by User Role

```bash
# Customer journey tests only
pytest tests/api/test_customer_journey.py -v

# Store manager tests only
pytest tests/api/test_store_manager_journey.py -v
```

## Environment Configuration

Edit `config/environments.py` to customize:
- Base URLs
- Timeout values
- Retry counts
- Environment-specific settings

```python
ENVIRONMENTS = {
    "qa": {
        "base_url": "https://petstore.swagger.io/v2",
        "timeout": 15,
        "retry_count": 2
    }
}
```

## Test Execution Options

```bash
# Verbose output
pytest -v

# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Run specific test by name
pytest -k "customer_browses"

# Run tests with markers (if defined)
pytest -m smoke

# Parallel execution (4 workers)
pytest -n 4

# Generate multiple report formats
pytest --html=report.html --alluredir=allure-results --junitxml=junit.xml
```

## CI/CD Integration

### GitHub Actions (Included)

The `.github/workflows/ci-pipeline.yml` provides:

1. **Multi-environment testing**: Runs tests on qa and staging
2. **Python version matrix**: Tests on Python 3.9, 3.10, 3.11
3. **Parallel execution**: Faster test runs
4. **Automated reporting**: HTML and Allure reports
5. **Artifact uploads**: Test results stored for review
6. **PR integration**: Results posted to pull requests
7. **Scheduled runs**: Daily regression testing
8. **Production smoke tests**: Post-deployment validation

### Other CI Systems

**Jenkins**:
```groovy
stage('API Tests') {
    steps {
        sh 'pytest --env=qa --junitxml=results.xml'
    }
    post {
        always {
            junit 'results.xml'
        }
    }
}
```

**GitLab CI**:
```yaml
test:
  script:
    - pytest --env=$CI_ENVIRONMENT_NAME --junitxml=report.xml
  artifacts:
    reports:
      junit: report.xml
```

**Azure DevOps**:
```yaml
- script: pytest --junitxml=TEST-results.xml
  displayName: 'Run API Tests'
- task: PublishTestResults@2
  inputs:
    testResultsFiles: 'TEST-results.xml'
```

## Framework Design Patterns

### 1. Page Object Model (API Adaptation)
Encapsulates API endpoints in client classes for maintainability.

### 2. Factory Pattern
`TestDataFactory` generates dynamic test data, avoiding hard-coded values.

### 3. Fixture Pattern
Pytest fixtures manage test setup/teardown and resource sharing.

### 4. Separation of Concerns
- **Framework layer**: Reusable components
- **Test layer**: Business logic
- **Config layer**: Environment settings

## Best Practices Demonstrated

1. **DRY Principle**: No code duplication
2. **Single Responsibility**: Each class has one purpose
3. **Explicit Assertions**: Clear, meaningful error messages
4. **Comprehensive Logging**: Full audit trail
5. **Environment Isolation**: No cross-environment pollution
6. **Data Independence**: Tests don't interfere with each other

## Advanced Features

### Custom Assertions
```python
from framework.assertions import assert_response_status, assert_field_value

assert_response_status(response, 200, "Pet creation failed")
assert_field_value(data, "status", "available", "Wrong pet status")
```

### Retry Logic
Built-in retry for transient failures:
- 429 Too Many Requests
- 500-504 Server Errors
- Network timeouts

### Parallel Execution
```bash
# Auto-detect CPU cores
pytest -n auto

# Specify worker count
pytest -n 4
```

## Troubleshooting

### Common Issues

**Issue**: Tests failing with connection errors
**Solution**: Check base_url in environments.py, verify network access

**Issue**: Import errors
**Solution**: Ensure virtual environment is activated, run `pip install -r requirements.txt`

**Issue**: Allure command not found
**Solution**: Install Allure CLI tool (see Installation section)

**Issue**: Tests running slowly
**Solution**: Use parallel execution: `pytest -n auto`

## Extending the Framework

### Adding New Test Suites
```python
# tests/api/test_new_feature.py
import pytest
from framework.test_data_factory import TestDataFactory

class TestNewFeature:
    def test_new_scenario(self, api_client, logger):
        # Your test implementation
        response = api_client.get("/new-endpoint")
        assert response.status_code == 200
```

### Adding New Environments
```python
# config/environments.py
ENVIRONMENTS["uat"] = {
    "base_url": "https://petstore-uat.swagger.io/v2",
    "timeout": 20,
    "retry_count": 2
}
```

### Custom Fixtures
```python
# tests/conftest.py
@pytest.fixture
def custom_test_data():
    return {"key": "value"}
```

## Test Strategy

See `docs/TEST_STRATEGY.md` for the comprehensive test strategy document addressing:
- Risk-based prioritization
- Three-tier testing approach
- Smart automation framework
- Vendor collaboration
- Maintenance optimization

## Release Integration

See `docs/RELEASE_INTEGRATION.md` for release decision framework including:
- Test result classification
- Quantifiable metrics
- Risk-based scoring
- Verifiable criteria
- Business urgency handling

## Reporting

### HTML Reports
```bash
pytest --html=report.html --self-contained-html
# Open report.html in browser
```

### Allure Reports
```bash
pytest --alluredir=allure-results
allure serve allure-results
# Opens interactive report in browser
```

### JUnit XML (for CI)
```bash
pytest --junitxml=junit-results.xml
```

## Maintenance

- **Dependencies**: Update quarterly or when security patches released
- **Test Review**: Monthly review of test execution times and flaky tests
- **Documentation**: Keep README and inline comments current
- **Refactoring**: Continuous improvement of framework components

## Contributing

1. Create feature branch
2. Write tests for new features
3. Ensure all tests pass
4. Update documentation
5. Submit pull request

## License

MIT License - See LICENSE file for details

## Contact

For questions or issues, please open a GitHub issue or contact the QA team.

---

**Happy Testing! 🚀**
