import os
from transformers import pipeline
from django.conf import settings
import requests
from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional
import base64
from io import BytesIO
from PIL import Image
from diffusers import StableDiffusionPipeline
import torch

class AIService:
    def __init__(self):
        self.model_name = os.getenv('HF_MODEL_NAME', 'facebook/bart-large-cnn')
        self.summarizer = pipeline("summarization", model=self.model_name)
        self.text_generator = pipeline("text-generation", model="gpt2")
        self.image_pipe = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1")
        
    def generate_content(self, prompt: str, max_length: int = 100, temperature: float = 0.7) -> str:
        try:
            result = self.text_generator(
                prompt, 
                max_length=max_length,
                temperature=temperature,
                do_sample=True
            )
            return result[0]['generated_text']
        except Exception as e:
            print(f"Error in content generation: {str(e)}")
            return ""

    def generate_image(self, prompt: str) -> Optional[bytes]:
        try:
            image = self.image_pipe(prompt).images[0]
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode('utf-8')
        except Exception as e:
            print(f"Error generating image: {str(e)}")
            return None

    def analyze_viral_potential(self, content: str) -> Dict:
        try:
            # Simulate viral potential analysis
            score = min(len(content) / 1000, 0.95)  # Simple heuristic
            feedback = "Good potential" if score > 0.7 else "Needs improvement"
            return {
                'score': round(score, 2),
                'feedback': feedback,
                'suggestions': [
                    "Use more engaging language",
                    "Add relevant hashtags",
                    "Include a call-to-action"
                ]
            }
        except Exception as e:
            print(f"Error in viral analysis: {str(e)}")
            return {}

    def generate_content_calendar(self, brand_industry: str, goals: List[str], duration: int = 30) -> Dict:
        try:
            prompt = f"Create a {duration}-day content calendar for {brand_industry} brand aiming to {', '.join(goals)}"
            calendar = self.generate_content(prompt, max_length=500)
            return {
                'calendar': calendar,
                'events': self._parse_calendar_to_events(calendar)
            }
        except Exception as e:
            print(f"Error generating calendar: {str(e)}")
            return {}

    def _parse_calendar_to_events(self, calendar_text: str) -> List[Dict]:
        # Simplified parsing logic
        events = []
        lines = calendar_text.split('\n')
        current_date = datetime.now()
        
        for i, line in enumerate(lines[:30]):  # Max 30 events
            if line.strip():
                events.append({
                    'date': (current_date + timedelta(days=i)).strftime('%Y-%m-%d'),
                    'content': line.strip(),
                    'platforms': ['facebook', 'instagram', 'twitter']
                })
        return events

    def analyze_social_stats(self, stats_data: Dict) -> Dict:
        try:
            analysis = {}
            for platform, data in stats_data.items():
                analysis[platform] = {
                    'engagement_rate': data.get('likes', 0) / max(data.get('followers', 1), 1),
                    'growth_trend': "positive" if data.get('growth', 0) > 0 else "negative",
                    'recommendations': self._generate_recommendations(data)
                }
            return analysis
        except Exception as e:
            print(f"Error analyzing stats: {str(e)}")
            return {}

    def _generate_recommendations(self, data: Dict) -> List[str]:
        recs = []
        if data.get('engagement_rate', 0) < 0.03:
            recs.append("Increase engagement by posting more interactive content")
        if data.get('growth', 0) <= 0:
            recs.append("Run targeted ad campaigns to boost follower growth")
        return recs if recs else ["Current performance is good. Maintain consistency"]
