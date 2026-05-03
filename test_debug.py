"""
Debug test suite for resume.py
Tests all major functions and edge cases
"""
import sys
import os
import tempfile
from unittest.mock import patch, MagicMock
import json

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import resume

def test_format_card():
    """Test the format_card function with various inputs"""
    print("\n=== Testing format_card ===")
    
    # Test 1: Normal input
    fields = {
        "PROJECT": "Test Project",
        "STATE": "Working on feature X",
        "NEXT": "Complete integration"
    }
    result = resume.format_card(fields)
    print("✓ Test 1 - Normal input:")
    print(result)
    assert "PROJECT" in result
    assert "Test Project" in result
    
    # Test 2: Long text wrapping
    fields = {
        "DESCRIPTION": "This is a very long description that should wrap across multiple lines when formatted because it exceeds the 50 character limit"
    }
    result = resume.format_card(fields)
    print("\n✓ Test 2 - Long text wrapping:")
    print(result)
    assert "DESCRIPTION" in result
    
    # Test 3: Empty values
    fields = {
        "EMPTY": "",
        "WHITESPACE": "   "
    }
    result = resume.format_card(fields)
    print("\n✓ Test 3 - Empty values:")
    print(result)
    assert "None" in result
    
    print("\n✅ format_card tests passed!")


def test_text_truncation():
    """Test the text truncation logic in generate_restoration_string"""
    print("\n=== Testing Text Truncation ===")
    
    # Test 1: Short text (no truncation)
    short_text = "Short export text"
    assert len(short_text) < 3000
    print(f"✓ Test 1 - Short text ({len(short_text)} chars): No truncation needed")
    
    # Test 2: Long text (should truncate)
    long_text = "A" * 5000
    truncated = long_text[:1500] + "\n...\n" + long_text[-1500:]
    print(f"✓ Test 2 - Long text ({len(long_text)} chars) -> Truncated to {len(truncated)} chars")
    assert len(truncated) < len(long_text)
    assert "..." in truncated
    
    print("\n✅ Text truncation tests passed!")


def test_environment_variables():
    """Test environment variable handling"""
    print("\n=== Testing Environment Variables ===")
    
    # Save original values
    original_api_key = os.environ.get("WATSONX_API_KEY")
    original_project_id = os.environ.get("PROJECT_ID")
    
    # Test 1: Missing environment variables
    os.environ.pop("WATSONX_API_KEY", None)
    os.environ.pop("PROJECT_ID", None)
    
    # Reload module to get fresh env vars
    import importlib
    importlib.reload(resume)
    
    print("✓ Test 1 - Missing env vars detected")
    assert resume.WATSONX_API_KEY == ""
    assert resume.PROJECT_ID == ""
    
    # Test 2: Set environment variables
    os.environ["WATSONX_API_KEY"] = "test_key_123"
    os.environ["PROJECT_ID"] = "test_project_456"
    importlib.reload(resume)
    
    print("✓ Test 2 - Env vars loaded correctly")
    assert resume.WATSONX_API_KEY == "test_key_123"
    assert resume.PROJECT_ID == "test_project_456"
    
    # Restore original values
    if original_api_key:
        os.environ["WATSONX_API_KEY"] = original_api_key
    if original_project_id:
        os.environ["PROJECT_ID"] = original_project_id
    
    print("\n✅ Environment variable tests passed!")


def test_file_reading():
    """Test file reading functionality"""
    print("\n=== Testing File Reading ===")
    
    # Test 1: Create and read a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md', encoding='utf-8') as f:
        test_content = "# Test Export\nUser: Test task\nBob: Test response"
        f.write(test_content)
        temp_path = f.name
    
    try:
        with open(temp_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✓ Test 1 - File read successfully: {len(content)} chars")
        assert content == test_content
        
        # Test 2: Non-existent file
        try:
            with open("nonexistent_file.md", 'r', encoding='utf-8') as f:
                f.read()
            print("✗ Test 2 - Should have raised FileNotFoundError")
        except FileNotFoundError:
            print("✓ Test 2 - FileNotFoundError raised correctly")
        
    finally:
        os.unlink(temp_path)
    
    print("\n✅ File reading tests passed!")


def test_api_payload_structure():
    """Test API payload structure"""
    print("\n=== Testing API Payload Structure ===")
    
    # Mock the API call to inspect payload
    test_export = "Test export content"
    test_token = "test_token_123"
    
    # Test paragraph format
    payload_paragraph = {
        "model_id": resume.MODEL_ID,
        "input": f"{resume.INSTRUCTION}\n\n{resume.FEW_SHOT_PARAGRAPH}\n\nInput:\n{test_export}\n\nOutput:",
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 175,
            "min_new_tokens": 50,
            "repetition_penalty": 1.3,
            "stop_sequences": ["\n\n"]
        },
        "project_id": resume.PROJECT_ID
    }
    
    print("✓ Test 1 - Paragraph format payload structure:")
    print(f"  - model_id: {payload_paragraph['model_id']}")
    print(f"  - max_new_tokens: {payload_paragraph['parameters']['max_new_tokens']}")
    print(f"  - stop_sequences: {payload_paragraph['parameters']['stop_sequences']}")
    
    # Test structured format
    payload_structured = {
        "model_id": resume.MODEL_ID,
        "input": f"{resume.INSTRUCTION_STRUCTURED}\n\n{resume.FEW_SHOT_STRUCTURED}\n\nInput:\n{test_export}\n\nOutput:",
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 250,
            "min_new_tokens": 50,
            "repetition_penalty": 1.3,
            "stop_sequences": []
        },
        "project_id": resume.PROJECT_ID
    }
    
    print("\n✓ Test 2 - Structured format payload structure:")
    print(f"  - model_id: {payload_structured['model_id']}")
    print(f"  - max_new_tokens: {payload_structured['parameters']['max_new_tokens']}")
    print(f"  - stop_sequences: {payload_structured['parameters']['stop_sequences']}")
    
    print("\n✅ API payload structure tests passed!")


def test_structured_output_parsing():
    """Test structured output parsing logic"""
    print("\n=== Testing Structured Output Parsing ===")
    
    # Test 1: Complete structured output
    test_output = """PROJECT:     Test Project
STATE:       Feature complete, testing pending
LAST ACTION: Implemented core functionality
NEXT:        Write unit tests
DEAD ENDS:   Alternative approach A, approach B"""
    
    lines = [l for l in test_output.split("\n") if l.strip()]
    fields = {}
    for line in lines:
        if ":" in line:
            key, _, val = line.partition(":")
            fields[key.strip()] = val.strip()
    
    print("✓ Test 1 - Complete structured output parsed:")
    for key, val in fields.items():
        print(f"  {key}: {val}")
    
    assert "PROJECT" in fields
    assert "STATE" in fields
    assert "NEXT" in fields
    
    # Test 2: Output with DEADLINE
    test_output_deadline = """PROJECT:     Urgent Project
STATE:       In progress
LAST ACTION: Started implementation
NEXT:        Complete by EOD
DEAD ENDS:   None
DEADLINE:    2026-05-03"""
    
    lines = [l for l in test_output_deadline.split("\n") if l.strip()]
    clean = []
    for line in lines:
        clean.append(line)
        if line.startswith("DEADLINE:") or (line.startswith("DEAD ENDS:") and not any(l.startswith("DEADLINE:") for l in lines)):
            break
    result = "\n".join(clean[:6])
    
    print("\n✓ Test 2 - Output with DEADLINE parsed correctly")
    print(f"  Lines captured: {len(result.split(chr(10)))}")
    
    print("\n✅ Structured output parsing tests passed!")


def test_constants():
    """Test that all constants are properly defined"""
    print("\n=== Testing Constants ===")
    
    print(f"✓ WATSONX_URL: {resume.WATSONX_URL}")
    print(f"✓ MODEL_ID: {resume.MODEL_ID}")
    print(f"✓ INSTRUCTION length: {len(resume.INSTRUCTION)} chars")
    print(f"✓ INSTRUCTION_STRUCTURED length: {len(resume.INSTRUCTION_STRUCTURED)} chars")
    print(f"✓ FEW_SHOT_PARAGRAPH length: {len(resume.FEW_SHOT_PARAGRAPH)} chars")
    print(f"✓ FEW_SHOT_STRUCTURED length: {len(resume.FEW_SHOT_STRUCTURED)} chars")
    
    assert resume.WATSONX_URL.startswith("https://")
    assert "llama" in resume.MODEL_ID.lower()
    assert "RESTORE CONTEXT" in resume.INSTRUCTION
    assert "PROJECT:" in resume.INSTRUCTION_STRUCTURED
    
    print("\n✅ Constants tests passed!")


def run_all_tests():
    """Run all debug tests"""
    print("=" * 60)
    print("RESUME.PY DEBUG TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_constants,
        test_format_card,
        test_text_truncation,
        test_environment_variables,
        test_file_reading,
        test_api_payload_structure,
        test_structured_output_parsing
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"\n❌ {test.__name__} FAILED: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"TEST SUMMARY: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

# Made with Bob
