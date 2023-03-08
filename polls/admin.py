from django.contrib import admin
from .models import Question, Choice

#
# # Register your models here.
# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None, {'fields': ['question_text']}),
#         ('Date information', {'fields': ['pub_date']}),
#     ]
#
#     list_display = ('question_text', 'pub_date', 'was_published_recently')
#     list_filter = ['pub_date']
#
#
# class ChoiceInline(admin.StackedInline):
#     search_fields = ['question_text']
#     model = Choice
#     extra = 3

# Registering the Question and Choice models with the admin site.
admin.site.register(Question)
admin.site.register(Choice)
