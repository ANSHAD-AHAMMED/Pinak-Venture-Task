from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_test_user(sender, **kwargs):
    User = get_user_model()

    if not User.objects.filter(username="testuser").exists():
        User.objects.create_user(username="testuser", password="testpass")
        print("✅ Test user created: testuser / testpass")
