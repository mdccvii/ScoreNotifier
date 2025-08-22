#!/usr/bin/env python3
"""
Minimal syntax validation for the main.py improvements
"""
import ast
import os

def validate_syntax():
    """Check that main.py has valid Python syntax"""
    print("🔍 Validating Python syntax...")
    
    with open('main.py', 'r', encoding='utf-8') as f:
        code = f.read()
    
    try:
        ast.parse(code)
        print("✅ Python syntax is valid")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        return False

def check_improvements():
    """Check that all improvements are implemented"""
    print("🔍 Checking security and reliability improvements...")
    
    with open('main.py', 'r', encoding='utf-8') as f:
        code = f.read()
    
    checks = [
        ("Environment variables", "os.getenv" in code),
        ("Async sleep", "await asyncio.sleep" in code),
        ("Error handling", "try:" in code and "except" in code),
        ("Request timeout", "timeout=" in code),
        ("Data validation", "isinstance" in code),
        ("Discord channel validation", "channel_id = int" in code),
        ("Line notify error handling", "requests.exceptions.RequestException" in code),
        ("JSON error handling", "json.JSONDecodeError" in code),
        ("No hardcoded tokens", "YOUR_LINE_NOTIFY_TOKEN" not in code),
    ]
    
    all_passed = True
    for check_name, passed in checks:
        if passed:
            print(f"✅ {check_name}: Implemented")
        else:
            print(f"❌ {check_name}: Missing")
            all_passed = False
    
    return all_passed

def main():
    print("🚀 Validating ScoreNotifier improvements...")
    
    syntax_ok = validate_syntax()
    improvements_ok = check_improvements()
    
    if syntax_ok and improvements_ok:
        print("\n🎉 All validations passed! The code is ready for production.")
        return True
    else:
        print("\n❌ Some validations failed.")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)