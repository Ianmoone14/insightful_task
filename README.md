# Currency Conversion Testing Suite

An automated testing tool that verifies currency conversion accuracy across different platforms and applications.

## What Does This Do?

This tool automatically:
- Tests currency conversion on popular websites (XE.com, Wise.com)
- Compares results with your computer's built-in calculator
- Generates detailed reports showing conversion accuracy
- Saves all results and logs for review

## Quick Start

### Step 1: Get Everything Ready
Run the setup script - it will install everything you need automatically:

**Windows:**
```
python scripts/setup_environment.py
```

**Linux:**
```
python3 scripts/setup_environment.py
```

The setup will:
- Create a safe testing environment
- Download the browser needed for testing
- Install all required tools
- Create easy-to-use run scripts

### Step 2: Run Your Tests

**Windows:**
Double-click `run_tests.bat` or run it from command line

**Linux:**
```
./run_tests.sh
```

That's it! The tests will run automatically with the browser window visible so you can watch what's happening.

## What You'll Get

### Real-Time Testing
- Watch as the browser automatically visits currency websites
- See live currency conversion testing in action
- Browser runs in visible mode so you can observe the process

### Detailed Reports
- **HTML Report**: `reports/pytest_report.html` - Beautiful, detailed test results
- **Log Files**: `logs/` folder - Complete execution history with timestamps
- **Console Output**: Real-time feedback during test runs

### Comprehensive Coverage
Tests multiple scenarios:
- Different currency amounts (1000, 2000, 3000)
- Various currency pairs (RSD to EUR, RSD to USD)
- Cross-platform verification (web vs calculator)

## What's Under the Hood

This project uses reliable, industry-standard tools:
- **Browser Testing**: Playwright for accurate web automation
- **Calculator Integration**: Smart detection of your system's calculator
- **Report Generation**: Professional HTML reports with charts and details
- **Cross-Platform**: Works on both Windows and Linux
- **Logging**: Complete audit trail of all test activities

## Supported Platforms

- **Windows 10/11** with built-in Calculator app
- **Linux** with GNOME Calculator (Ubuntu, Debian, etc.)
- **Python 3.8+** required

## File Structure

```
├── run_tests.bat          # Windows: Click to run tests
├── run_tests.sh           # Linux: Script to run tests
├── reports/               # Test results and HTML reports
├── logs/                  # Detailed execution logs
├── tests/                 # Test definitions
├── pages/                 # Website interaction logic
├── calculators/           # Calculator automation
└── utils/                 # Supporting tools
```

## Technical Documentation

### Test Plan & Methodology

This project implements a comprehensive automated testing strategy for currency conversion verification:

**Test Scope:**
- **Websites**: XE.com and Wise.com currency converters
- **Amounts**: 1000, 2000, 3000 RSD
- **Target Currencies**: EUR and USD
- **Platforms**: Windows and Linux operating systems
- **Verification**: Cross-validation between web results and system calculator

**Test Architecture:**
```
Test Flow: Web Scraping → Calculator Automation → Result Comparison → Assertion
├── Browser Automation (Playwright)
├── Calculator Integration (PyAutoGUI + PyWinAuto)
├── Data Collection & Storage
└── Verification Engine with Tolerance Checking
```

### Technical Approach

**Framework Selection:**
- **Playwright**: Chosen for reliable cross-browser automation and excellent element detection
- **pytest**: Industry-standard testing framework with rich reporting capabilities
- **PyAutoGUI/PyWinAuto**: Platform-specific calculator automation for accurate desktop app interaction

**Key Technical Decisions:**
1. **Page Object Model**: Organized web interactions into reusable page classes
2. **Service Layer**: Abstracted calculator operations for different OS platforms
3. **Tolerance-Based Assertions**: Accounts for minor rounding differences (±0.01 tolerance)
4. **Comprehensive Logging**: Detailed execution tracking for debugging and audit trails

**Data Flow:**
1. Extract exchange rates from websites using CSS/XPath selectors
2. Perform calculations via system calculator automation
3. Store results in structured format with timestamps
4. Apply tolerance-based comparison logic
5. Generate detailed verification reports

### Challenges Encountered & Solutions

**Challenge 1: Cross-Platform Calculator Automation**
- **Problem**: Different calculator apps across Windows/Linux with varying interfaces
- **Solution**: Implemented platform-specific service classes with unified interface
- **Implementation**: Automatic OS detection and appropriate calculator service instantiation

**Challenge 2: Dynamic Website Elements**
- **Problem**: Currency converter websites use dynamic loading and changing selectors
- **Solution**: Robust element waiting strategies and multiple selector fallbacks
- **Implementation**: Playwright's auto-waiting combined with custom retry logic

**Challenge 3: Floating Point Precision**
- **Problem**: Minor calculation differences between web and calculator results
- **Solution**: Tolerance-based assertions (±0.01) instead of exact equality
- **Implementation**: Custom comparison functions with configurable precision

**Challenge 4: Reliable Browser Automation**
- **Problem**: Ensuring consistent behavior across different environments
- **Solution**: Headful mode for visibility, slow motion for reliability, comprehensive error handling
- **Implementation**: Configurable browser settings via environment variables

**Challenge 5: Result Persistence & Reporting**
- **Problem**: Need for detailed audit trails and result tracking
- **Solution**: Multi-format output (HTML reports, structured logs, timestamped files)
- **Implementation**: pytest-html integration with custom verification collectors

### Test Case Structure

**Organized Testing Hierarchy:**
```
tests/
├── test_xe_verification.py      # XE.com conversion tests
└── test_wise_verification.py    # Wise.com conversion tests

Each test implements:
├── Setup: Browser initialization & navigation
├── Execution: Rate extraction & calculator verification  
├── Verification: Tolerance-based result comparison
└── Cleanup: Resource management & result storage
```

**Assertion Strategy:**
- **Primary**: Numerical comparison with ±0.01 tolerance
- **Secondary**: Verification of successful data extraction
- **Tertiary**: Cross-platform result consistency validation

### Quality Assurance Features

**Reliability Measures:**
- Automatic retry mechanisms for flaky network operations
- Comprehensive error logging with stack traces
- Browser automation with visible feedback
- Platform-specific optimizations for calculator interaction

**Validation Layers:**
1. **Data Extraction Validation**: Ensures valid numerical data retrieval
2. **Calculation Accuracy**: Verifies mathematical operations
3. **Cross-Platform Consistency**: Confirms identical behavior across OS platforms
4. **Tolerance Management**: Handles acceptable precision differences

This technical implementation ensures robust, maintainable, and reliable currency conversion testing across multiple platforms and data sources.
