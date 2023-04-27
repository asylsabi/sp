
from django.forms import ModelForm
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=100,verbose_name="Заголовок")
    date = models.DateTimeField(verbose_name="Дата мероприятия")
    location = models.CharField(max_length=100,verbose_name="Локация")
    budget = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Бюджет")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/",verbose_name="Фото")
    time_create=models.DateTimeField(auto_now_add=True,verbose_name="Время создания")
    time_update=models.DateTimeField(auto_now=True,verbose_name="Время изменения")
    is_published=models.BooleanField(default=True,verbose_name="Публикация")
    description = models.TextField(max_length=1500, default='',verbose_name="Описание мероприятия")
    attachment = models.FileField(upload_to='attachments/',verbose_name="Прикрепите коммерческое предложение ")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT,verbose_name="Категория")
    phone_number = PhoneNumberField(verbose_name="Номер телефона")
    email = models.EmailField(max_length = 254,verbose_name="Почта")


def __str__(self):
    return self.title

class Meta:
    verbose_name = 'Event'
    verbose_name_plural = 'Events'
    ordering = ['time_create', 'title']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

class Sponsor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, verbose_name="Название компании")
    contact_name = models.CharField(max_length=100,verbose_name="ФИО представителя")
    about = models.TextField(max_length=500,verbose_name="О компании")
    description = models.TextField(max_length=1500, verbose_name="Условия спонсора")
    phone_number = PhoneNumberField(verbose_name="Номер телефона")
    email = models.EmailField(max_length = 254,verbose_name="Почта")


class Sponsorship(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class SponsorForm(ModelForm):
    class Meta:
        model = Sponsor
        fields = ['company_name', 'contact_name', 'email']

class SponsorshipForm(ModelForm):
    class Meta:
        model = Sponsorship
        fields = ['event', 'sponsor', 'amount']

from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class Contact(models.Model):
        # Определяем поля модели
    name = models.CharField(max_length=100, verbose_name="Имя контакта")  #
    email = models.EmailField(verbose_name="Email контакта")  #
    message = models.TextField(verbose_name="Сообщение")  #
    role = models.CharField(max_length=20, choices=[('sponsor', 'Спонсор'), ('organizer', 'Организатор')],
                                verbose_name="Роль")

        # Определяем строковое представление модели
def __str__(self):
    return self.name

