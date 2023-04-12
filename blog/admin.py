from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Car, Comment


@admin.register(Car)
class CarAdmin(SummernoteModelAdmin):
    """ Car Admin model """

    list_display = ('make', 'model', 'year')
    list_filter = ('created_date', 'year')
    summernote_fields = ('specifications', 'rundown')
    prepopulated_fields = {'slug': ('site_user', 'make', 'model', 'year')}
    search_fields = ['make', 'model', 'year']


@admin.register(Comment)
class CommentAdmin(SummernoteModelAdmin):
    """ Comment Admin Model """

    list_display = ('author', 'created_date')
    summernote_fields = ('text',)
