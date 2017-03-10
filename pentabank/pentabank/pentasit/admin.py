from django.contrib import admin
from pentabank.pentasit.models import *
from pentabank.pentasit.forms import *
from django.forms import Textarea

class WordInline(admin.TabularInline):
    model = Word
    form = WordForm
    extra = 0


class NpTypeInline(admin.TabularInline):
    model = NpType
    form = NpTypeForm
    extra = 0


class NodeAdmin(admin.ModelAdmin):
    # filter_horizontal = ('word', 'npType',)
    fieldsets = ( (None, {'fields': ('relation', 'pos', 'word', 'npType', 'other',)}),
                )
    inlines = [WordInline, NpTypeInline]
    list_display = ['relation', 'pos', 'wordlist', 'nptypelist']


class NodeInline(admin.TabularInline):
    model = Node
    form = NodeForm
    extra = 0


class ExampleInline(admin.TabularInline):
    model = Example
    form = ExampleForm
    extra = 0


class AntecedentInline(admin.TabularInline):
    model = Node
    form = NodeForm
    extra = 0


class SituationAdmin(admin.ModelAdmin):
    save_on_top = True      # Also allow the save buttons on top
    # filter_horizontal = ('nodes', 'example',)
    fieldsets = ( (None, {'fields': ('name', 'preposition', 'npType', 'penta', 'antecedent', 'action', )}),
                )
    inlines = [NodeInline, ExampleInline]

    #fieldsets = ( (None, {'fields': ('name', 'preposition', 'npType', 'penta', 'action', )}),
    #            )
    #inlines = [AntecedentInline, NodeInline, ExampleInline]

    list_display = ['name', 'preposition', 'npType', 'penta', 'antecedent', 'action' ]
    list_filter = ['penta']


class ExampleAdmin(admin.ModelAdmin):
    list_display = ['sentence', 'textId', 'sentId']
    list_filter = ['textId']
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(
                attrs={'rows':1}
            )
            },
    }


class FieldChoiceAdmin(admin.ModelAdmin):
    readonly_fields=['machine_value']
    list_display = ['english_name','dutch_name','machine_value','field']
    list_filter = ['field']

    def save_model(self, request, obj, form, change):

        if obj.machine_value == None:
            # Check out the query-set and make sure that it exists
            qs = FieldChoice.objects.filter(field=obj.field)
            if len(qs) == 0:
                # The field does not yet occur within FieldChoice
                # Future: ask user if that is what he wants (don't know how...)
                # For now: assume user wants to add a new field (e.g: wordClass)
                # NOTE: start with '0'
                obj.machine_value = 0
            else:
                # Calculate highest currently occurring value
                highest_machine_value = max([field_choice.machine_value for field_choice in qs])
                # The automatic machine value we calculate is 1 higher
                obj.machine_value= highest_machine_value+1

        obj.save()



# Models that serve others
admin.site.register(FieldChoice, FieldChoiceAdmin)
admin.site.register(HelpChoice)

# Models supporting situation
admin.site.register(Word)
admin.site.register(NpType)
admin.site.register(Relation)
admin.site.register(Node, NodeAdmin)
admin.site.register(Example, ExampleAdmin)

# The actual situation model
admin.site.register(Situation, SituationAdmin)