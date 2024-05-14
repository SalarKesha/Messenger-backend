from django.db.models.signals import post_save
from django.dispatch import receiver
from group.models import GroupChat, GroupMember


@receiver(post_save, sender=GroupChat)
def create_group_member(sender, instance, created, **kwargs):
    if created:
        GroupMember.objects.create(
            group=instance,
            user=instance.creator,
            type=GroupMember.ADMIN
        )
