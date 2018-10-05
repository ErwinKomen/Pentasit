from django.contrib import admin
from pentabank.ptxref.models import *
# from pentabank.ptxref.forms import *

class BookAdmin(admin.ModelAdmin):
    """Present a book"""

    list_display = ['number', 'abbr', 'english']
    list_filter = ['abbr']

# PtxRef models
admin.site.register(Book, BookAdmin)
admin.site.register(Selection)
admin.site.register(VerseItem)
admin.site.register(Reference)
