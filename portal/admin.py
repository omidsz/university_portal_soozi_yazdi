from django.contrib import admin
from .models import Announcement, Event, ScientificIdea, Comment


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')
    search_fields = ('title', 'content', 'created_by__username')
    list_filter = ('created_at',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'capacity', 'created_by', 'date', 'created_at',)
    search_fields = ('title', 'description', 'created_by__username')
    list_filter = ('date', 'created_at')
    filter_horizontal = ('participants',)  # بهتر برای ManyToMany

    def show_participants(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    show_participants.short_description = "شرکت‌کنندگان"



@admin.register(ScientificIdea)
class ScientificIdeaAdmin(admin.ModelAdmin):
    list_display = ('title', 'submitted_by', 'is_approved', 'approved_by', 'submitted_at')
    list_filter = ('is_approved', 'submitted_at')
    search_fields = ('title', 'content', 'submitted_by__username', 'approved_by__username')



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at', 'announcement', 'event')
    list_filter = ('created_at',)
    search_fields = ('content', 'user__username')






