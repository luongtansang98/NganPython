from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ModelBase(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
        ordering = ['-id']  # sắp giảm theo id

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Course(ModelBase):
    subject = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    image = models.ImageField(upload_to='courses/%Y/%m/', null=True, blank=True)


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Lesson(ModelBase):
    subject = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', related_query_name='my_lesson')
    tags = models.ManyToManyField('Tag', blank=True, related_name='lessons')

    image = models.ImageField(upload_to='lessons/%Y/%m/', null=True, blank=True)


class Comment(ModelBase):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

class Rating(ModelBase):
    rating = models.DecimalField(max_digits=5, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)






