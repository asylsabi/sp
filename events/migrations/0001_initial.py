# Generated by Django 4.1.7 on 2023-04-27 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя контакта')),
                ('email', models.EmailField(max_length=254, verbose_name='Email контакта')),
                ('message', models.TextField(verbose_name='Сообщение')),
                ('role', models.CharField(choices=[('sponsor', 'Спонсор'), ('organizer', 'Организатор')], max_length=20, verbose_name='Роль')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('date', models.DateTimeField(verbose_name='Дата мероприятия')),
                ('location', models.CharField(max_length=100, verbose_name='Локация')),
                ('budget', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Бюджет')),
                ('photo', models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('is_published', models.BooleanField(default=True, verbose_name='Публикация')),
                ('description', models.TextField(default='', max_length=1500, verbose_name='Описание мероприятия')),
                ('attachment', models.FileField(upload_to='attachments/', verbose_name='Прикрепите коммерческое предложение ')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Номер телефона')),
                ('email', models.EmailField(max_length=254, verbose_name='Почта')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.category', verbose_name='Категория')),
            ],
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100, verbose_name='Название компании')),
                ('contact_name', models.CharField(max_length=100, verbose_name='ФИО представителя')),
                ('about', models.TextField(max_length=500, verbose_name='О компании')),
                ('description', models.TextField(max_length=1500, verbose_name='Условия спонсора')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Номер телефона')),
                ('email', models.EmailField(max_length=254, verbose_name='Почта')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sponsorship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
                ('sponsor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.sponsor')),
            ],
        ),
    ]
