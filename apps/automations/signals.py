import os
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.conf import settings
from .models import LLMProvider, AIModel

@receiver(post_migrate)
def setup_default_llm_providers(sender, **kwargs):
    if sender.name == 'apps.automations':
        for provider_config in settings.DEFAULT_LLM_PROVIDERS:
            provider, created = LLMProvider.objects.get_or_create(
                name=provider_config['name'],
                defaults={
                    'provider_class': provider_config['provider_class'],
                    'base_url': provider_config['base_url'],
                    'api_key': os.getenv(provider_config['api_key_env'])
                }
            )
            
            # Add default models for each provider
            if provider.name == 'HuggingFace' and created:
                AIModel.objects.create(
                    name='Mixtral 8x7B',
                    model_id='mistralai/Mixtral-8x7B-Instruct-v0.1',
                    provider=provider,
                    model_type='text',
                    description='Mixtral 8x7B instruction-tuned model'
                )
                AIModel.objects.create(
                    name='Stable Diffusion XL',
                    model_id='stabilityai/stable-diffusion-xl-base-1.0',
                    provider=provider,
                    model_type='image',
                    description='Stable Diffusion XL image generation'
                )
            elif provider.name == 'OpenAI' and created:
                AIModel.objects.create(
                    name='GPT-4 Turbo',
                    model_id='gpt-4-turbo-preview',
                    provider=provider,
                    model_type='text',
                    description='OpenAI GPT-4 Turbo model'
                )
                AIModel.objects.create(
                    name='Text Embedding 3',
                    model_id='text-embedding-3-large',
                    provider=provider,
                    model_type='embedding',
                    description='OpenAI text embedding model'
                )
