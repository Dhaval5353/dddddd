# from django.db import models
# from django.contrib.auth.models import User

# # Create your models here.
# class Chat(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     message = models.TextField()
#     response = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.user.username}: {self.message}'

from django.db import models
from django.contrib.auth.models import User
from django.db import IntegrityError

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message}'

    @classmethod
    def create_chat_entry(cls, user, message, response):
        """
        Method to securely create a new chat entry.
        """
        try:
            chat_entry = cls(user=user, message=message, response=response)
            chat_entry.save()
            return chat_entry
        except IntegrityError as e:
            # Handle integrity errors (e.g., duplicate entry) appropriately
            raise e
