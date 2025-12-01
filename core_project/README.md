Project Overview
This is a modular, scalable test automation framework built using Selenium for automated testing of web applications. The framework follows a hybrid architecture that separates reusable core components from project-specific implementations, enabling maximum code reuse and maintainability across multiple projects

**Core Framework Components**
The core_project/ directory contains framework-level code that is completely independent of any specific application under test. This separation provides several key advantages:
What's in Core:
Base Classes: BasePage, BaseTest, WebDriverFactory
Reusable Components: Common UI patterns (modals, navigation bars, tables)
Framework Services: API clients, database connectors, reporting services
Utilities: Screenshot capture, data generators, file handlers
Configuration Framework: Settings management, environment handlers

**Project-Specific Implementation**
The herokuapp/ and amazon/ directories contains application-specific code that extends the core framework:

What's in Project:
Application Pages: Herokuapp/Amazon pages objects
Test Suites: Tests targeting Herokuapp/Amazon functionality
Project Config: Application-specific settings and data

## Project Overview

This framework showcases enterprise-level test automation with:
- **Core Technologies** for global framework
- **Selenium WebDriver** for UI testing
- **Page Object Model** with service layer abstraction
- **API Testing** with Requests library
- **Mock/Stub** testing with WireMock
- **Database Testing** with PostgreSQL - in progress
- **CI/CD Integration** with Jenkins - in progress 
- **Containerization** with Docker - in progress
- **Advanced Reporting** with Allure
- **Centralized Logging** 
- **Centralized configuration management**

**Running**
cd core_project
# Run tests
pytest {project_name}/tests/ -v --project={project_name} --alluredir=reports/allure-results
# Run specific Amazon test
pytest {project_name}/tests/test_samsung_phone_purchase.py::TestSamsungPhonePurchase::test_complete_samsung_phone_purchase -v -s --project={project_name}
# Run headless more
pytest {project_name}/tests/ -v --project={project_name} --headless --alluredir=reports/allure-results

Advantages of This Separation
1. Code Reusability & DRY Principle
``````
python
# CORE - Reusable base class
class BasePage:
    def __init__(self, driver):
        self.driver = driver
    
    def find_element(self, locator):
        # Reusable element finding with wait
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(locator)
        )

# PROJECT - Extends core without duplication
class LoginPage(BasePage):
    def login(self, username, password):
        # Uses core methods
        self.find_element(LOCATORS.USERNAME).send_keys(username)
        self.find_element(LOCATORS.PASSWORD).send_keys(password)
        self.find_element(LOCATORS.SUBMIT).click()
``````
2. Framework Standardization
Consistent Patterns: All projects follow the same architecture
Standardized Practices: Common coding standards and conventions
Unified Reporting: Same reporting format across all projects
Shared Utilities: Common helpers available to all projects

3. Reduced Maintenance Overhead
Single Point Updates: Fix core bugs once, benefit all projects
Independent Evolution: Core framework can be upgraded without breaking projects
Clear Boundaries: No accidental coupling between project logic

4. Multi-Project Support
bash
core_project/
├── core/                          # SHARED BY ALL PROJECTS
├── herokuapp/             # Project A
├── amazon/             # Project B - New project, same core!
├── admin-panel-project/           # Project C
└── shared_resources/              # Shared by all

5. Team Collaboration Efficiency
Framework Team: Maintains and enhances the core framework
Project Teams: Focus on application-specific test development
Knowledge Sharing: Core expertise centralized, project knowledge distributed

6. Easier Onboarding
New Team Members: Learn core framework once, apply to any project
Project Switching: Easy movement between different project teams
Documentation: Core documentation applicable across all projects

7. Improved Test Stability
Battle-Tested Core: Core utilities refined through multiple project usage
Consistent Patterns: Reliable patterns established across projects
Shared Best Practices: Lessons learned benefit all implementations

**Technologies Used**
Python 3.11+ - Primary programming language
Selenium WebDriver 4.0+ - Browser automation
Pytest - Test framework and runner
Allure-pytest - Test reporting and visualization
Pytest-xdist - Parallel test execution
WebDriver Manager - Automated driver management

**Supporting Libraries**
Pydantic - Data validation and settings management
Python-dotenv - Environment variables management
Loguru/Python logging - Structured logging
Requests - API testing capabilities
PyYAML - Configuration file parsing

**Infrastructure & Tools**
Docker - Containerization for test execution
Jenkins - CI/CD pipeline automation
Git - Version control
Allure Report - Test reporting dashboard
BrowserStack/Selenium Grid - Cross-browser testing (optional)