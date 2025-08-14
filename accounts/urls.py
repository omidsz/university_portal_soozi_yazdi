from django.urls import path
from django.views.generic import TemplateView


from .views import (CustomTokenView,
                    MemberPageView, ModeratorPageView,
                    UserListAPI, login_page,
                    showuserpage, verify_email_view, RegisterVieww, register_page, )
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path('token/', CustomTokenView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # مشاهده کاربران ثبت شده
    path('api/users/', UserListAPI.as_view(), name='user-list-api'),
    path('show-users/', showuserpage, name='show-users'),
    #
    path('register/', RegisterVieww.as_view(), name='register'),
    path('registerpage/', register_page, name='register'),
    path('verify-email/<uidb64>/<token>/', verify_email_view, name='verify-email'),
    #
    path('login-page/', login_page, name='login_page'),
    #
    path('member/', MemberPageView.as_view(), name='member_page'),
    path('moderator/', ModeratorPageView.as_view(), name='moderator_page'),

]
