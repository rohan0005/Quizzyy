from django.db import models

# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=100,)
    description = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.category



class QuizzAdd(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    question = models.CharField(max_length=100)
    optionA = models.CharField(max_length=100)
    optionB = models.CharField(max_length=100)
    optionC = models.CharField(max_length=100, blank=True) 
    optionD = models.CharField(max_length=100, blank=True)
    correctAnswer =  models.CharField(max_length=100)
    
