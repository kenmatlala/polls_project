from django.db import models
import datetime
from django.utils import timezone
from django.contrib import admin


# Create your models here.
# The Question class is a model that represents a question. 
# 
# A model is the single, definitive source of information about your data. 
# 
# It contains the essential fields and behaviors of the data you’re storing. 
# 
# Generally, each model maps to a single database table
# The Question class is a subclass of the Model class, which is a subclass of the object class
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return f"{self.question_text} {self.pub_date}"

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        """
        Return True if the question's pub_date is within the last day.
        :return: The return value is a boolean value.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


# The Choice model is a database table that has a foreign key to the Question model. 
# 
# The foreign key is defined with the question attribute of the Choice class. 
# 
# The question attribute is connected to the Question model via a relationship field, and this tells
# Django each Choice is related to a single Question
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


def was_published_recently(self):
    """
    Return True if the pub_date is within the last day
    :return: A boolean value.
    """
    now = timezone.now()
    return now - datetime.timedelta(days=1) <= self.pub_date <= now
