from django.contrib import admin
from gameApp.models import Questions, Answers, UserScores

# changing admin tables views to have more friendy views
# using admin.ModelAdmin

class QuestionsAdmin(admin.ModelAdmin):
    list_display = ['question', 'point']

class AnswersAdmin(admin.ModelAdmin):
    list_display = ['answer', 'question_id', 'is_true']

class UserScoresAdmin(admin.ModelAdmin):
    list_display = ['score', 'user']

# Register your models here.

admin.site.register(Questions, QuestionsAdmin)
admin.site.register(Answers, AnswersAdmin)
admin.site.register(UserScores, UserScoresAdmin)
