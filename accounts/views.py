from django.core.mail import send_mail
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .token_serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsModerator, IsMember
from django.shortcuts import render, redirect

from rest_framework.views import APIView

from .serializers import UserSerializer, RegisterSerializer
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator as token_generator

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from .tasks import send_verification_code

###################################################################################
class UserListAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        active_users = User.objects.filter(is_active=True)
        return Response(serializer.data)


def showuserpage(request):
    return render(request, 'accounts/users.html')


####################################################################################

class RegisterVieww(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            current_site = get_current_site(request).domain
            verification_link = f"http:/{current_site}/api/accounts/verify-email/{uid}/{token}/"

            # send_mail(
            #     subject="Verify your email",
            #     message=f"Click the link to verify: {verification_link}",
            #     from_email=settings.DEFAULT_FROM_EMAIL,
            #     recipient_list=[user.email],
            #     fail_silently=False,
            # )

            subject = f" :لینک تایید {request.user}"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = user.email

            send_verification_code.delay(subject, verification_link, from_email, [to_email])
            return Response({"message": "Verification email sent."})
        return Response(serializer.errors, status=400)


def register_page(request):
    return render(request, 'accounts/signup.html')


def verify_email_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'accounts/login.html')

    return redirect('accounts/invalid_link.html')


#################################################################################################
def login_page(request):
    return render(request, 'accounts/login.html')


###############################################################################################


def verify_code_page(request):
    return render(request, 'accounts/verify_code.html')


################################################################################################
class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class MemberPageView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsMember]

    def get(self, request):
        return Response({"message": "صفحه عضو انجمن"})


class ModeratorPageView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsModerator]

    def get(self, request):
        return Response({"message": "داشبورد مدیر انجمن"})

#################################################################################

