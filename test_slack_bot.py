import unittest
from unittest.mock import Mock, patch
import slack_bot  # Import the slack_bot module

class TestBot(unittest.TestCase):

    @patch("slack_bot.openai.ChatCompletion.create")
    def test_mention_handler(self, mock_openai_create):
        # Set up mock objects
        mock_openai_create.return_value = Mock(choices=[{"message": {"content": "Test reply"}}])
        mock_say = Mock()

        # Set up a sample event body
        event_body = {
            "event": {
                "text": "<@U12345678> Test message",
                "user": "U12345678",
            }
        }

        # Call the mention_handler function
        slack_bot.mention_handler(event_body, mock_say)  # Use slack_bot.mention_handler

        # Check if the openai.ChatCompletion.create function was called with the expected arguments
        mock_openai_create.assert_called_once_with(
            model="gpt-3.5-turbo",
            messages=slack_bot.messages,  # Use slack_bot.messages
            temperature=0.8,
            max_tokens=300,
        )

        # Check if the say function was called with the expected arguments
        mock_say.assert_called_once_with("<@U12345678> Test reply")

if __name__ == "__main__":
    unittest.main()
