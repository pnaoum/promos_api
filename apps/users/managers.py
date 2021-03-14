from django.contrib.auth.models import UserManager


# from apps.users.constants import ADMIN_USER, NORMAL_USER


class CustomUserManager(UserManager):
    pass
    # def get_admin_users(self, *args, **kwargs):
    #     return self.filter(role=ADMIN_USER)
    #
    # def get_normal_users(self, *args, **kwargs):
    #     return self.filter(role=NORMAL_USER)
