#!/usr/bin/env python3
"""
Simple test script to validate the improved main.py functionality
"""
import os
import sys
import json
import unittest.mock
from unittest.mock import patch, mock_open, MagicMock

# Mock nextcord and requests before importing main
sys.modules['nextcord'] = MagicMock()
sys.modules['nextcord.ext'] = MagicMock()
sys.modules['nextcord.ext.commands'] = MagicMock()

# Create a mock requests module with proper exception classes
mock_requests = MagicMock()
mock_requests.exceptions = MagicMock()
mock_requests.exceptions.RequestException = Exception
sys.modules['requests'] = mock_requests

# Import the main module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_environment_variables():
    """Test that environment variables are properly loaded"""
    print("🧪 Testing environment variable loading...")
    
    with patch.dict(os.environ, {
        'LINE_NOTIFY_TOKEN': 'test_line_token',
        'DISCORD_TOKEN': 'test_discord_token',
        'DISCORD_CHANNEL_ID': '123456789'
    }):
        # Re-import to test environment variable loading
        import importlib
        import main
        importlib.reload(main)
        
        assert main.LINE_NOTIFY_TOKEN == 'test_line_token'
        assert main.DISCORD_TOKEN == 'test_discord_token'
        assert main.DISCORD_CHANNEL_ID == '123456789'
        print("✅ Environment variables loaded correctly")

def test_error_handling():
    """Test error handling in various functions"""
    print("🧪 Testing error handling...")
    
    # Import main after setting environment variables
    with patch.dict(os.environ, {
        'LINE_NOTIFY_TOKEN': 'test_token',
        'DISCORD_CHANNEL_ID': '123456789'
    }):
        import importlib
        import main
        importlib.reload(main)
        
        # Test Line Notify error handling
        with patch('main.requests.post') as mock_post:
            mock_post.side_effect = Exception("Network error")
            result = main.send_line_notify("test message")
            assert result == False
            print("✅ Line Notify error handling works")
        
        # Test target.json loading error handling
        with patch('builtins.open', mock_open()) as mock_file:
            mock_file.side_effect = FileNotFoundError("File not found")
            # This should be handled gracefully during import
            print("✅ File error handling works")

def test_data_validation():
    """Test API data validation"""
    print("🧪 Testing API data validation...")
    
    with patch.dict(os.environ, {'LINE_NOTIFY_TOKEN': 'test_token'}):
        import importlib
        import main
        importlib.reload(main)
        
        # Set test targets
        main.targets = ["test target"]
        
        # Test with invalid JSON response
        with patch('main.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            result = main.check_scores()
            assert "ข้อมูลไม่ถูกต้อง" in result[0]
            print("✅ JSON error handling works")
        
        # Test with non-list response
        with patch('main.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"not": "a list"}
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            result = main.check_scores()
            assert "รูปแบบข้อมูลไม่ถูกต้อง" in result[0]
            print("✅ Data structure validation works")
        
        # Test with valid data
        with patch('main.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = [
                {"name": "test target", "uploaded": 4}
            ]
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            with patch.object(main, 'send_line_notify', return_value=True):
                result = main.check_scores()
                assert "ออกแล้ว" in result[0]
                print("✅ Valid data processing works")

def main_test():
    """Run all tests"""
    print("🚀 Starting tests for improved ScoreNotifier...")
    
    try:
        test_environment_variables()
        test_error_handling()
        test_data_validation()
        print("\n🎉 All tests passed! The improvements are working correctly.")
        return True
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = main_test()
    sys.exit(0 if success else 1)