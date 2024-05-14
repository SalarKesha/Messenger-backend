from django.db.models.signals import post_save
from django.dispatch import receiver
from channel.models import Channel, ChannelMember


@receiver(post_save, sender=Channel)
def add_channel_member(sender, instance, created, **kwargs):
    if created:
        ChannelMember.objects.create(
            channel=instance,
            user=instance.creator,
            type=ChannelMember.ADMIN,
        )
