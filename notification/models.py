from django.db import models

from course.models import CourseInstance
from exercise.models import Submission
from userprofile.models import UserProfile


class NotificationSet(object):
    """
    A result set of notifications.

    """
    @classmethod
    def get_unread(cls, user):
        return NotificationSet(
            user.userprofile.received_notifications.filter(
                seen=False))

    @classmethod
    def get_course(cls, course_instance, user, per_page=30, page=1):
        skip = max(0, page - 1) * per_page
        qs = user.userprofile.received_notifications.filter(
            course_instance=course_instance)[skip:(skip + per_page)]
        return NotificationSet(qs)

    @classmethod
    def get_course_new_count(cls, course_instance, user):
        return user.userprofile.received_notifications.filter(
            course_instance=course_instance, seen=False).count()

    def __init__(self, queryset):
        self.notifications = list(queryset)

    @property
    def count(self):
        return len(self.notifications)

    def count_and_mark_unseen(self):
        """
        Marks notifications seen in data base but keeps the set instances
        in unseen state.
        """
        count = 0
        for notification in self.notifications:
            if not notification.seen:
                count += 1
                notification.seen = True
                notification.save(update_fields=["seen"])

                # Return the instance to previous state without saving.
                notification.seen = False
        return count


class Notification(models.Model):
    """
    A user notification of some event, for example manual assessment.
    """

    @classmethod
    def send(cls, sender, recipient, submission):
        notification = Notification(
            sender=sender,
            recipient=recipient,
            course_instance=submission.exercise.course_instance,
            submission=submission,
        )
        notification.save()

    @classmethod
    def remove(cls, recipients, submission):
        Notification.objects.filter(
            submission=submission,
            recipient__in=recipients
        ).delete()

    subject = models.CharField(max_length=255, blank=True)
    notification = models.TextField(blank=True)
    sender = models.ForeignKey(UserProfile, related_name="sent_notifications",
        blank=True, null=True)
    recipient = models.ForeignKey(UserProfile, related_name="received_notifications")
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    course_instance = models.ForeignKey(CourseInstance)
    submission = models.ForeignKey(Submission, blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return "To:" + self.recipient.user.username + ", " + self.subject + ", " + self.notification[:100]
