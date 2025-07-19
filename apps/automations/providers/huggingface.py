import os
from huggingface_hub import InferenceClient
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class HuggingFaceProvider:
    def __init__(self, api_key=None, base_url=None):
        self.api_key = api_key or os.getenv('HUGGINGFACE_API_KEY')
        self.base_url = base_url or "https://api-inference.huggingface.co"
        self.client = InferenceClient(
            token=self.api_key,
            base_url=self.base_url
        )

    def execute(self, model_id, input_data, agent_config):
        try:
            task_type = agent_config.get('task_type', 'text')
            
            if task_type == 'text':
                return self._handle_text_generation(model_id, input_data, agent_config)
            elif task_type == 'image':
                return self._handle_image_generation(model_id, input_data, agent_config)
            else:
                raise ValueError(f"Unsupported task type: {task_type}")
                
        except Exception as e:
            logger.error(f"HuggingFace error: {str(e)}")
            raise

    def _handle_text_generation(self, model_id, input_data, config):
        prompt = input_data.get('prompt', '')
        parameters = {
            'max_new_tokens': config.get('max_tokens', 200),
            'temperature': config.get('temperature', 0.7),
            'top_p': config.get('top_p', 0.9),
            'repetition_penalty': config.get('repetition_penalty', 1.2),
        }
        
        response = self.client.text_generation(
            model=model_id,
            prompt=prompt,
            **parameters
        )
        
        return {
            'response': response,
            'model': model_id,
            'parameters': parameters
        }

    def _handle_image_generation(self, model_id, input_data, config):
        prompt = input_data.get('prompt', '')
        parameters = {
            'negative_prompt': config.get('negative_prompt', ''),
            'guidance_scale': config.get('guidance_scale', 7.5),
            'num_inference_steps': config.get('steps', 50),
        }
        
        response = self.client.text_to_image(
            model=model_id,
            prompt=prompt,
            **parameters
        )
        
        return {
            'images': response,
            'model': model_id,
            'parameters': parameters
        }
