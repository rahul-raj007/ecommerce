from django.db import models

# Create your models here.


class ContactMessage(models.Model):
    full_name = models.CharField(max_length=225)
    email = models.CharField(max_length=225)
    contact_message = models.TextField()
    creations_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
