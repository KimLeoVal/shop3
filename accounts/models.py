from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.


class Profile(models.Model):
    birthday = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    avatar = models.ImageField(upload_to="avatars", null=True, blank=True, verbose_name="Аватар")
    user = models.OneToOneField(get_user_model(),
                                on_delete=models.CASCADE,
                                verbose_name="Пользователь",
                                related_name="profile")
