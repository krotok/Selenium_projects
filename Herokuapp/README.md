# Herokuapp Test Automation Framework

## Senior-Level Test Automation Project

A comprehensive test automation framework demonstrating advanced testing concepts and best practices for Herokuapp applications.

## Project Overview

This framework showcases enterprise-level test automation with:
- **Selenium WebDriver** for UI testing
- **Page Object Model** with service layer abstraction
- **API Testing** with Requests library
- **Mock/Stub** testing with WireMock
- **Database Testing** with PostgreSQL
- **CI/CD Integration** with Jenkins
- **Containerization** with Docker
- **Advanced Reporting** with Allure
- **Professional Logging** and configuration management

## 🏗️ Architecture
📦 herokuapp-test-framework
├── 📁 config/ # Environment configurations
├── 📁 pages/ # Page Object classes
├── 📁 services/ # API, DB, WireMock services
├── 📁 tests/ # Test implementations
├── 📁 utils/ # Custom utilities
├── 📁 docker/ # Docker configurations
├── 📁 jenkins/ # CI/CD pipelines
└── 📁 reports/ # Test reports and outputs



## 🛠️ Technologies Used

- **Python 3.9** - Primary programming language
- **Selenium 4** - Web automation
- **Pytest** - Test framework
- **Allure** - Test reporting
- **Requests** - API testing
- **PostgreSQL** - Database testing
- **WireMock** - Mock service testing
- **Docker** - Containerization
- **Jenkins** - CI/CD pipeline
- **Page Object Pattern** - Maintainable UI tests

## 📁 Key Features

### 🔧 Advanced Testing Patterns
- **Page Object Model** with service layer abstraction
- **Custom waits and retry mechanisms**
- **Environment-specific configurations**
- **Comprehensive fixture management**

### 🧪 Test Types
- **UI Tests** - Selenium-based browser automation
- **API Tests** - REST API validation
- **Integration Tests** - Multi-system testing
- **Mock Tests** - Service virtualization

### 📊 Reporting & Logging
- **Allure Reports** with detailed attachments
- **Structured logging** with different levels
- **Screenshot capture** on failures
- **Custom test categories** and severity levels

### 🔄 CI/CD & DevOps
- **Docker containerization**
- **Jenkins pipeline** with parallel execution
- **Environment management**
- **Automated reporting**

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Chrome/Firefox browser
- Docker (optional)
- Jenkins (optional)

### Local Execution

1. **Clone and setup:**
```bash
git clone <repository-url>
cd herokuapp-test-framework
pip install -r requirements.txt
```

2. **Run all tests:**
pytest tests/ -v --alluredir=reports/allure-results

# Run specific test types
pytest tests/ -m "smoke" -v
pytest tests/ -m "api" -v
pytest tests/ -m "ui" -v

# Run with different environment
pytest tests/ --env=stage -v

3. **Generate Report:**
allure serve reports/allure-results

**Docker Execution**
1. Run complete test suite:
docker-compose up tests

2. View reports:
docker-compose up allure
# Access reports at http://localhost:5050

**Jenkins Integration**
Create pipeline job in Jenkins
Point to Jenkinsfile in repository
Configure environment variables as needed
Trigger build manually or via webhooks

This comprehensive project demonstrates:

✅ Selenium with Page Object Model - Well-structured UI automation
✅ Service Layer - Abstraction for API, DB, and mock services
✅ API Testing - Comprehensive REST API validation
✅ WireMock Integration - Service virtualization and mocking
✅ PostgreSQL Database - Database testing integration
✅ Jenkins CI/CD - Complete pipeline implementation
✅ Docker Containerization - Environment consistency
✅ Allure Reporting - Professional test reporting
✅ Advanced Logging - Structured logging system
✅ Retry Mechanisms - Fault-tolerant test execution
✅ Custom Waits - Intelligent waiting strategies
✅ Pytest Hooks & Fixtures - Advanced test configuration
✅ Environment Configs - Dev/Stage configuration management
✅ Professional README - Comprehensive documentation