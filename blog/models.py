from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()


# ------------> Models <------------

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):

    class Status (models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        REJECTED = 'RJ', 'Rejected'



    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    category = models.ForeignKey(
        Category,
        on_delete= models.CASCADE,
        related_name= "posts"
    )

    tags = models.ManyToManyField(
        Tag,
        related_name= 'posts',
        blank= True
    )

    author = models.ForeignKey(
        User,
        on_delete= models.CASCADE,
        related_name= 'posts'        
    )

    content = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=2, choices= Status.choices, default= Status.DRAFT) 

    class Meta:
        ordering = ['-published_at']
        indexes = [
            models.Index(fields= ['published_at']),
            models.Index(fields= ['status']),
            models.Index(fields=['status', 'published_at']),
        ]


    def __str__(self):
        return self.title