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


class NoteAdmin(admin.ModelAdmin):
    """
    This is just a way to view the history of changes.
    We disable editing of entries.
    """
    list_display = ('timestamp', 'user', 'elu_link', 'note')
    list_display_links = None
    readonly_fields = ('timestamp', 'user', 'elu', 'note')
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'
    list_filter = ('user',)

    def elu_link(self, obj):
        return obj.elu.link()
    elu_link.allow_tags = True

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Elu, EluAdmin)
admin.site.register(Note, NoteAdmin)
