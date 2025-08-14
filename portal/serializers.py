import jdatetime
from rest_framework import serializers
from .models import Announcement, Event, ScientificIdea, Comment


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'created_at']


class EventSerializer(serializers.ModelSerializer):
    persian_date = serializers.SerializerMethodField()
    remaining_capacity = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'persian_date', 'date', 'created_at', 'participants', 'capacity',
                  'remaining_capacity']
        read_only_fields = ['remaining_capacity', 'created_by']


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

    def get_persian_date(self, obj):
        jd = jdatetime.datetime.fromgregorian(datetime=obj.date)
        return jd.strftime("%Y/%m/%d %H:%M")


class ScientificIdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScientificIdea
        fields = ['id', 'title', 'content', 'submitted_by', 'is_approved', 'approved_by', 'submitted_at', 'file']
        read_only_fields = ['submitted_by', 'is_approved', 'approved_by', 'submitted_at']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'event', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']


