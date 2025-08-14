# # token_serializers.py
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
#
# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
#         data['username'] = self.user.username
#         return data


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
#         data['username'] = self.user.username
#
#         # تشخیص نقش کاربر
#         role = 'user'  # پیش‌فرض: کاربر عادی
#
#         # اگر نقش به صورت فیلد user.role باشد (مثلاً مدل یوزر را سفارشی کرده‌اید)
#         if hasattr(self.user, 'role'):
#             role = self.user.role
#
#         else:
#             # یا نقش بر اساس گروه‌های Django باشد
#             if self.user.groups.filter(name='moderator').exists():
#                 role = 'moderator'
#             elif self.user.groups.filter(name='member').exists():
#                 role = 'member'
#
#         data['role'] = role
#
#         return data

# token_serializers.py
# token_serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserRole  # مطمئن شو مسیر درست باشه

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username

        try:
            role_obj = UserRole.objects.get(user=self.user)
            data['role'] = role_obj.role  # مثلاً 'moderator', 'member', ...
        except UserRole.DoesNotExist:
            data['role'] = 'user'  # اگر هیچ نقشی ثبت نشده باشد

        return data


