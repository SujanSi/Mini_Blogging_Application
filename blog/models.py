from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=250,default=1)
    email= models.EmailField()
    address=models.CharField(max_length=20,default=1)
    message=models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.author