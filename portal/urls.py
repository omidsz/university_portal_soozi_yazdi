from django.urls import path
from .views import (
    AnnouncementListCreateView,
    ScientificIdeaListCreateView, MemberDashboardView, ModeratorDashboardView,
    showUserDashboardView, AnnouncementDetailAPIView, ApproveScientificIdeaAPIView, showModeratorDashboardView,
    showMemberDashboardView, AnnouncementDetailView, IdeaCreateView, IdeaListForModerators, ApproveIdeaView,
    ApprovedIdeaListView, RejectIdeaView, EventListCreateView, EventRetrieveUpdateDestroyAPIView,
    EventCommentCreateView, EventCommentListView, EventRegisterAPIView,  EventParticipantsAPIView,
    showEventRegister,
)

urlpatterns = [
    path('announcements/', AnnouncementListCreateView.as_view(), name='announcement-list-create'),
    path('announcements/<int:pk>/', AnnouncementDetailView.as_view()),
    path('events/', EventListCreateView.as_view(), name='event-list-create'),

    path('dashboard/showuser/', showUserDashboardView, name='show-dashboard-user'),

    path('dashboard/member/', MemberDashboardView.as_view(), name='dashboard-member'),
    path('dashboard/showmember/', showMemberDashboardView, name='show-member-moderator'),

    path('dashboard/moderator/', ModeratorDashboardView.as_view(), name='dashboard-moderator'),
    path('dashboard/showmoderator/', showModeratorDashboardView, name='show-dashboard-moderator'),

    path('ideas/', ScientificIdeaListCreateView.as_view(), name='idea-list-create'),
    path('ideas/', IdeaCreateView.as_view(), name='idea-create'),
    path('ideas/moderator/', IdeaListForModerators.as_view(), name='idea-list'),
    path('ideas/<int:pk>/approve/', ApproveIdeaView.as_view(), name='idea-approve'),
    path('ideas/approved/', ApprovedIdeaListView.as_view(), name='approved-ideas'),
    path('ideas/<int:pk>/reject/', RejectIdeaView.as_view(), name='reject-idea'),
    path('events/<int:pk>/', EventRetrieveUpdateDestroyAPIView.as_view(), name='event-approve'),
    path('events/<int:event_id>/comments/', EventCommentCreateView.as_view(), name='event-comments'),
    path('events/<int:event_id>/comments/list/', EventCommentListView.as_view()),
    path('events/<int:event_id>/register/', EventRegisterAPIView.as_view(), name='event-register'),
    path('events/showregister/', showEventRegister, name='event-register'),
    path('events/<int:event_id>/registrations/', EventParticipantsAPIView.as_view(), name='event-registrations'),





]
