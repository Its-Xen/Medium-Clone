from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django_elasticsearch_dsl.registries import registry

from core_apps.articles.models import Article


@receiver(post_save, sender=Article)
def update_document(sender, instance=None, created=False, **kwargs):
    registry.update(instance)


@receiver(post_delete, sender=Article)
def delete_document(sender, instance=None, **kwargs):
    registry.delete(instance)
