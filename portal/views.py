from django.db.models import Q
from django.http import HttpResponse

from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Announcement, Event, ScientificIdea, Comment, ChatMessage
from .serializers import AnnouncementSerializer, EventSerializer, ScientificIdeaSerializer, CommentSerializer
from django.shortcuts import get_object_or_404, render


from accounts.permissions import IsUser, IsMember, IsModerator, IsUserOrModerator
from rest_framework import permissions
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser


from .tasks import send_welcome_to_event
from django.contrib.auth.models import User

class AnnouncementListCreateView(APIView):
    # permission_classes = [IsAuthenticated, IsUserOrModerator]

    def get(self, request):
        announcements = Announcement.objects.all()
        serializer = AnnouncementSerializer(announcements, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AnnouncementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if pk is None:
            return Response({"detail": "شناسه مشخص نشده."}, status=400)
        try:
            announcement = Announcement.objects.get(pk=pk)
            announcement.delete()
            return Response(status=204)
        except Announcement.DoesNotExist:
            return Response({"detail": "اطلاعیه پیدا نشد."}, status=404)

    def put(self, request, pk=None):
        if pk is None:
            return Response({"detail": "شناسه مشخص نشده."}, status=400)
        try:
            announcement = Announcement.objects.get(pk=pk)
        except Announcement.DoesNotExist:
            return Response({"detail": "اطلاعیه پیدا نشد."}, status=404)

        serializer = AnnouncementSerializer(announcement, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class AnnouncementDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer


###################################################################
class IdeaCreateView(generics.CreateAPIView):
    queryset = ScientificIdea.objects.all()
    serializer_class = ScientificIdeaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(submitted_by=self.request.user)


class IdeaListForModerators(generics.ListAPIView):
    queryset = ScientificIdea.objects.filter(is_approved=False)
    serializer_class = ScientificIdeaSerializer
    # permission_classes = [permissions.IsAdminUser]


class ApproveIdeaView(APIView):

    def post(self, request, pk):
        try:
            idea = ScientificIdea.objects.get(pk=pk)
            idea.is_approved = True
            idea.approved_by = request.user
            idea.save()
            return Response({'message': 'Idea approved'}, status=status.HTTP_200_OK)
        except ScientificIdea.DoesNotExist:
            return Response({'error': 'Idea not found'}, status=status.HTTP_404_NOT_FOUND)


class ApprovedIdeaListView(generics.ListAPIView):
    serializer_class = ScientificIdeaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ScientificIdea.objects.filter(is_approved=True).order_by('-submitted_at')


class RejectIdeaView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            idea = ScientificIdea.objects.get(pk=pk)
            idea.delete()
            return Response({'message': 'ایده حذف شد'}, status=status.HTTP_200_OK)
        except ScientificIdea.DoesNotExist:
            return Response({'error': 'ایده پیدا نشد'}, status=status.HTTP_404_NOT_FOUND)


# important
# class EventListCreateView(generics.ListCreateAPIView):
#         queryset = Event.objects.all()
#         serializer_class = EventSerializer
#         permission_classes = [permissions.IsAuthenticated]
#
#         def perform_create(self, serializer):
#             serializer.save(created_by=self.request.user)

class EventListCreateView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        لیست همه رویدادها
        """
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        ایجاد رویداد جدید
        """
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            # اضافه کردن کاربر ایجادکننده قبل از ذخیره
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]


class EventCommentCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'error': 'رویداد یافت نشد'}, status=404)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(event=event, user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ScientificIdeaListCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        ideas = ScientificIdea.objects.all()
        serializer = ScientificIdeaSerializer(ideas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ScientificIdeaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(submitted_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventCommentListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, event_id):
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({'detail': 'رویداد پیدا نشد'}, status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter(event=event).order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


#


# views.py
class EventRegisterAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)

        # بررسی ظرفیت
        if event.remaining_capacity <= 0:
            return Response({'detail': 'ظرفیت این رویداد تکمیل شده است.'}, status=status.HTTP_400_BAD_REQUEST)

        # بررسی ثبت‌نام قبلی
        if request.user in event.participants.all():
            return Response({'detail': 'قبلاً در این رویداد ثبت‌نام کرده‌اید.'}, status=status.HTTP_400_BAD_REQUEST)

        # اضافه کردن کاربر به لیست شرکت‌کنندگان
        event.participants.add(request.user)

        # آماده‌سازی ایمیل
        subject = f"تأیید ثبت‌نام در رویداد: {event.title}"
        message = f"""
سلام {request.user.get_full_name() or request.user.username} عزیز،

ثبت‌نام شما در رویداد "{event.title}" با موفقیت انجام شد.
تاریخ رویداد: {event.date}

با احترام،
تیم پشتیبانی
        """
        from_email = settings.EMAIL_HOST_USER
        to_email = request.user.email

        # ارسال ایمیل با Celery
        send_welcome_to_event.delay(subject, message, from_email, [to_email])

        return Response({'detail': 'ثبت‌نام با موفقیت انجام شد و ایمیل تأیید در حال ارسال است.'}, status=status.HTTP_200_OK)


def showEventRegister(request):
    event_id = request.GET.get('event_id')
    if not event_id:
        return HttpResponse("رویدادی انتخاب نشده.", status=400)

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return HttpResponse("رویداد پیدا نشد.", status=404)

    return render(request, 'portal/register-event-page.html', {'event': event})


class EventParticipantsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'detail': 'رویداد یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)

        participants = event.participants.all()
        data = [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
            for user in participants
        ]
        return Response(data, status=status.HTTP_200_OK)


def showUserDashboardView(request):
    announcements = Announcement.objects.all().order_by('-created_at')

    return render(request, 'portal/dashboard.html', {'announcements': announcements})


class AnnouncementDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsModerator, IsUser]

    def get(self, request, pk):
        announcement = get_object_or_404(Announcement, pk=pk)
        serializer = AnnouncementSerializer(announcement)
        return Response(serializer.data)

    def put(self, request, pk):
        announcement = get_object_or_404(Announcement, pk=pk)
        serializer = AnnouncementSerializer(announcement, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        announcement = get_object_or_404(Announcement, pk=pk)
        announcement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def showAnnouncementDetail(request):
    announcements = Announcement.objects.all()

    return render(request, 'portal/dashboard.html', {'announcements': announcements})


class ApproveScientificIdeaAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsModerator]

    def post(self, request, pk):
        idea = get_object_or_404(ScientificIdea, pk=pk)
        if idea.is_approved:
            return Response({"detail": "این ایده قبلاً تأیید شده است."}, status=status.HTTP_400_BAD_REQUEST)

        idea.is_approved = True
        idea.approved_by = request.user
        idea.save()
        serializer = ScientificIdeaSerializer(idea)
        return Response(serializer.data)


class MemberDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsMember]

    def get(self, request):
        return Response({
            "role": "member",
            "message": "داشبورد عضو انجمن",
            "available_actions": [
                "ایجاد اطلاعیه",
                "ویرایش یا حذف اطلاعیه",
                "ثبت رویداد جدید",
                "مدیریت نظرات"
            ]
        })


def showMemberDashboardView(request):
    title = Announcement.objects.all()

    return render(request, 'portal/member_dashboard.html', {'title': title})


# داشبورد مدیر انجم
class ModeratorDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsModerator, IsUser]

    def get(self, request):
        return Response({
            "role": "moderator",
            "message": "داشبورد مدیر انجمن",
            "available_actions": [
                "تمام دسترسی‌های عضو انجمن",
                "تأیید و انتشار مقالات علمی",
                "حذف کاربران",
                "مدیریت کامل محتوا"
            ]
        })


def showModeratorDashboardView(request):
    annoucments = Announcement.objects.all()
    event = Event.objects.all()
    scientificIdea = ScientificIdea.objects.all()

    return render(request, 'portal/dashboard_moderator.html', {'title': annoucments, 'event': event,
                                                         'scientificidea': scientificIdea})


