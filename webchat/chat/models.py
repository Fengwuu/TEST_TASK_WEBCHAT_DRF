from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User


class Thread(models.Model):

    """Thread model. 
    Here Here I was forced to slightly deviate from the initially indicated only two fields,
    since I considered this solution the best for further use of the model. 
    This view simplifies interaction with objects in the future."""

    creater = models.ForeignKey(
        User, verbose_name="Creater", on_delete=models.CASCADE)
    participant = models.ManyToManyField(
        User, verbose_name="Participant", related_name="participant_user")
    created = models.DateTimeField("Created", auto_now_add=True)
    updated = models.DateTimeField(
        auto_now=True, verbose_name='Updated', blank=True)

    # Override save method to check participants count

    def save(self, *args, **kwargs):
        if self.participant.count() > 2:
            raise ValidationError("Chat can have only two participants.")
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Thread"
        verbose_name_plural = "Threads"


class Message(models.Model):
    """Message model."""
    thread = models.ForeignKey(
        Thread, verbose_name="Thread", on_delete=models.CASCADE)
    sender = models.ForeignKey(
        User, verbose_name="Sender", on_delete=models.CASCADE)
    text = models.TextField("Text of the message", max_length=500)
    created = models.DateTimeField("Sent", auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
