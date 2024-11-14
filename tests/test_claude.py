import unittest
import os
from unittest.mock import patch, MagicMock
from anthropic import Anthropic
import tempfile
import yaml
import base64
from claude import load_api_key, send_claude_prompt, concatenate_sources

class TestClaudePrompt(unittest.TestCase):
    def setUp(self):
        # Create temporary directories and files
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, 'claude_config.yml')
        self.test_key = "test-api-key"
        
        # Create test config file
        with open(self.config_file, 'w') as f:
            yaml.dump({'api_key': base64.b64encode(self.test_key.encode('utf-8')).decode('utf-8')}, f)
        
        # Create test source files
        self.source_dir = os.path.join(self.temp_dir, 'test_source')
        os.makedirs(self.source_dir)
        with open(os.path.join(self.source_dir, 'test.py'), 'w') as f:
            f.write('def test_function():\n    return "test"')

    def tearDown(self):
        # Clean up temporary files
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_load_api_key(self):
        with patch('claude.CONFIG_FILE', self.config_file):
            key = load_api_key()
            self.assertEqual(key, self.test_key)

    def test_concatenate_sources(self):
        result = concatenate_sources([self.source_dir])
        self.assertIn('test_function', result)
        self.assertIn('return "test"', result)

    @patch('anthropic.Anthropic')
    def test_send_claude_prompt(self, mock_anthropic):
        # Mock Claude's response
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Test response")]
        mock_anthropic.return_value.messages.create.return_value = mock_response

        test_content = "Test content"
        test_prompt = "Test prompt"
        
        with patch('claude.load_api_key', return_value=self.test_key):
            response = send_claude_prompt(test_content, test_prompt)
        
        self.assertEqual(response, "Test response")
        mock_anthropic.return_value.messages.create.assert_called_once()

    def test_send_claude_prompt_error(self):
        with patch('claude.load_api_key', return_value=self.test_key):
            with patch('anthropic.Anthropic') as mock_anthropic:
                mock_anthropic.return_value.messages.create.side_effect = Exception("API Error")
                
                with self.assertRaises(SystemExit):
                    send_claude_prompt("content", "prompt")

if __name__ == '__main__':
    unittest.main()