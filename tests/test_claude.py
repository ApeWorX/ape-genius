import unittest
import os
from unittest.mock import patch, MagicMock
from anthropic import Anthropic
import tempfile
import yaml
import base64

class TestAnthropicPrompt(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, 'anthropic_config.yml')
        self.test_key = "test-api-key"
        
        # Create test config file
        with open(self.config_file, 'w') as f:
            yaml.dump({'api_key': base64.b64encode(self.test_key.encode('utf-8')).decode('utf-8')}, f)
        
        # Create test source files
        self.source_dir = os.path.join(self.temp_dir, 'test_source')
        os.makedirs(self.source_dir)
        with open(os.path.join(self.source_dir, 'test.py'), 'w') as f:
            f.write('def test_function():\n    return "test"')
        
        # Set up Anthropic client
        self.client = Anthropic(api_key=self.test_key)

    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_anthropic_client(self):
        """Test Anthropic client initialization"""
        self.assertIsInstance(self.client, Anthropic)
        self.assertEqual(self.client.api_key, self.test_key)

    def test_concatenate_sources(self):
        """Test source file concatenation"""
        def concatenate_sources(source_dirs):
            content = ""
            for dir_path in source_dirs:
                for root, _, files in os.walk(dir_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r') as f:
                            content += f"# {file_path}\n{f.read()}\n\n"
            return content

        result = concatenate_sources([self.source_dir])
        self.assertIn('test_function', result)
        self.assertIn('return "test"', result)

    @patch('anthropic.resources.messages.Messages.create')
    def test_send_prompt(self, mock_create):
        """Test sending prompt to Anthropic API"""
        # Mock API response
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Test response")]
        mock_create.return_value = mock_response

        # Test data
        test_content = "Test content"
        test_prompt = "Test prompt"
        
        # Send prompt
        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": f"{test_prompt}\n\n{test_content}"
            }]
        )
        
        # Verify response
        self.assertEqual(response.content[0].text, "Test response")
        mock_create.assert_called_once()

    @patch('anthropic.resources.messages.Messages.create')
    def test_api_error(self, mock_create):
        """Test API error handling"""
        mock_create.side_effect = Exception("API Error")
        
        with self.assertRaises(Exception) as context:
            self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": "test"}]
            )
        
        self.assertEqual(str(context.exception), "API Error")

    def test_environment_config(self):
        """Test environment configuration"""
        with patch.dict(os.environ, {'CLAUDE_KEY': self.test_key}):
            client = Anthropic(api_key=os.getenv('CLAUDE_KEY'))
            self.assertEqual(client.api_key, self.test_key)

if __name__ == '__main__':
    unittest.main()