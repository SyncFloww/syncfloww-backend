from celery import shared_task
from django.conf import settings
from .models import AgentTask, AIAgent
import importlib
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def execute_agent_task(self, task_id):
    try:
        task = AgentTask.objects.get(id=task_id)
        task.status = 'processing'
        task.save()

        agent = task.agent
        provider_module = agent.model.provider.provider_class
        model_id = agent.model.model_id

        try:
            # Dynamic import of provider module
            module_path, class_name = provider_module.rsplit('.', 1)
            module = importlib.import_module(module_path)
            provider_class = getattr(module, class_name)
            
            # Initialize provider with config
            provider = provider_class(
                api_key=agent.model.provider.api_key,
                base_url=agent.model.provider.base_url
            )
            
            # Execute task
            result = provider.execute(
                model_id=model_id,
                input_data=task.input_data,
                agent_config=agent.config
            )
            
            task.output_data = result
            task.status = 'completed'
            task.completed_at = timezone.now()
            task.save()
            
            return result
            
        except Exception as e:
            logger.error(f"Error executing task {task_id}: {str(e)}")
            task.status = 'failed'
            task.output_data = {'error': str(e)}
            task.save()
            raise self.retry(exc=e)
            
    except AgentTask.DoesNotExist:
        logger.error(f"Task {task_id} not found")
        raise
