from django.contrib import admin
from .models import LeadRequest, UserProfile

admin.site.register(UserProfile)


@admin.register(LeadRequest)
class LeadRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'phone', 'created_at')
    list_filter = ('source', 'created_at')
    search_fields = ('phone', 'question')
