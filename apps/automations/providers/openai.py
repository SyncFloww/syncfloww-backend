import openai
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class OpenAIProvider:
    def __init__(self, api_key=None, base_url=None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.base_url = base_url or "https://api.openai.com/v1"
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    def execute(self, model_id, input_data, agent_config):
        try:
            task_type = agent_config.get('task_type', 'chat')
            
            if task_type == 'chat':
                return self._handle_chat_completion(model_id, input_data, agent_config)
            elif task_type == 'embedding':
                return self._handle_embeddings(model_id, input_data, agent_config)
            else:
                raise ValueError(f"Unsupported task type: {task_type}")
                
        except Exception as e:
            logger.error(f"OpenAI error: {str(e)}")
            raise

    def _handle_chat_completion(self, model_id, input_data, config):
        messages = input_data.get('messages', [])
        parameters = {
            'temperature': config.get('temperature', 0.7),
            'max_tokens': config.get('max_tokens', 200),
            'top_p': config.get('top_p', 1),
            'frequency_penalty': config.get('frequency_penalty', 0),
            'presence_penalty': config.get('presence_penalty', 0),
        }
        
        response = self.client.chat.completions.create(
            model=model_id,
            messages=messages,
            **parameters
        )
        
        return {
            'response': response.choices[0].message.content,
            'model': model_id,
            'parameters': parameters
        }

    def _handle_embeddings(self, model_id, input_data, config):
        text = input_data.get('text', '')
        
        response = self.client.embeddings.create(
            model=model_id,
            input=text
        )
        
        return {
            'embeddings': response.data[0].embedding,
            'model': model_id
        }
