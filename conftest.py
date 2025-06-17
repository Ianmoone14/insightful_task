import pytest
import os
from datetime import datetime


@pytest.fixture(scope="session")
def browser_launch_args():
    """Configure browser launch arguments - controlled by pytest.ini environment variables."""
    # Read from environment variables set in pytest.ini
    headed_env = os.getenv("BROWSER_HEADED", "true")
    headed = headed_env.lower() == "true"
    slow_mo = int(os.getenv("BROWSER_SLOW_MO", "500"))
    
    # Debug output
    print(f"BROWSER_HEADED env var: '{headed_env}' -> headed: {headed}")
    print(f"BROWSER_SLOW_MO env var: '{os.getenv('BROWSER_SLOW_MO', '500')}' -> slow_mo: {slow_mo}")
    print(f"Final browser config: headless={not headed}, slow_mo={slow_mo}")
    
    return {
        "headless": not headed,
        "slow_mo": slow_mo,
    }


@pytest.fixture(scope="session")
def browser_context_args():
    """Configure browser context arguments."""
    return {
        "viewport": {"width": 1280, "height": 720},
        "locale": "en-US",
    }


@pytest.fixture(scope="session", autouse=True)
def setup_reports_directory():
    """Create reports directory if it doesn't exist."""
    os.makedirs("reports", exist_ok=True)
    

# Global storage for verification results
verification_results_storage = []


@pytest.fixture(scope="session")
def test_data():
    """Test data for currency conversion."""
    return {
        "amounts": [1000, 2000, 3000],
        "source_currency": "RSD",
        "target_currencies": ["EUR", "USD"],
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S")
    }


@pytest.fixture(scope="function")
def verification_collector():
    """Fixture to collect verification results from tests."""
    def collect_result(verification_result):
        verification_results_storage.append(verification_result)
    
    return collect_result


def pytest_sessionfinish(session, exitstatus):
    """Hook that runs after all tests complete to print summary."""
    if verification_results_storage:
        try:
            # Print summary
            total_tests = len(verification_results_storage)
            passed_tests = sum(1 for result in verification_results_storage 
                             if result["overall_stats"]["verification_passed"])
            
            print(f"\n{'='*80}")
            print("CONSOLIDATED VERIFICATION REPORT SUMMARY")
            print(f"{'='*80}")
            print(f"Total verification tests: {total_tests}")
            print(f"Tests passed: {passed_tests}")
            print(f"Tests failed: {total_tests - passed_tests}")
            print(f"{'='*80}")
            
        except Exception as e:
            print(f"\nError generating consolidated report summary: {str(e)}")


def _get_test_logs() -> str:
    """Read the current test logs."""
    try:
        # Get today's log file
        today = datetime.now().strftime("%Y%m%d")
        log_file_path = f"logs/insightful_{today}.log"
        
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r', encoding='utf-8') as f:
                logs = f.read()
            
            # Limit logs to last 15000 characters to avoid huge HTML files
            if len(logs) > 15000:
                logs = "... (showing last 15000 characters) ...\n\n" + logs[-15000:]
            
            # Escape HTML characters
            logs = logs.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
            return logs
        else:
            return f"Log file not found: {log_file_path}"
            
    except Exception as e:
        return f"Error reading logs: {str(e)}"
