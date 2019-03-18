from django.db import models
from django.contrib.auth.models import User
from django_auto_one_to_one import AutoOneToOneModel

# Create your models here.
class Questions(models.Model):
    question = models.CharField(max_length=264, unique=True)
    point = models.PositiveIntegerField()

    def questionanswers(self):
        return self.question_answers.all()

    def __str__(self):
        return self.question

class Answers(models.Model):
    question_id = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='question_answers')
    answer = models.CharField(max_length=20)
    is_true = models.BooleanField()

    def __str__(self):
        return self.answer

# installed AutoOneToOneModel(Parent) which allows to create record
# in this model when parent model record is created
# in this case when new user is registered then created new record in
# UserScores whith default score equal to 0

class UserScores(AutoOneToOneModel(User,  related_name='user_id')):
    score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.score)
