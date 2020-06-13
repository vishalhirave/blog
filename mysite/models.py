from django.db import models
from django.utils import timezone
from django.shortcuts import reverse


# we are using auth.user model of django,so no need to create extra model for users
# post model for saving blog data
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('mysite:PostDetail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{author}{title}{text}{created_date}'.format(author=self.author, title=self.title, text=self.text,
                                                            created_date=self.created_date)
