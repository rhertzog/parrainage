from django.contrib import admin
from parrainage.app.models import Elu, Note


class NoteInline(admin.StackedInline):
    model = Note
    fields = (('timestamp', 'user'), 'note')
    readonly_fields = ('timestamp',)
    ordering = ('timestamp',)
    extra = 1


class EluAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'gender', 'nuance_politique',
                    'status')
    list_filter = ('gender', 'nuance_politique', 'status')
    inlines = [
        NoteInline
    ]


admin.site.register(Elu, EluAdmin)
