from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Car, Comment


@admin.register(Car)
class CarAdmin(SummernoteModelAdmin):
    """ Car Admin model """

    list_display = ('make', 'model', 'year')
    summernote_fields = ('specifications', 'rundown')


@admin.register(Comment)
class CommentAdmin(SummernoteModelAdmin):
    """ Comment Admin Model """

    list_display = ('author', 'created_date')
    summernote_fields = ('text',)
