from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

from .forms import AddEventForm, LoginUserForm, AddSpForm, ContactForm
from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить мероприятие", 'url_name': 'add_page'},
        {'title': "Спонсоры", 'url_name': 'find_sp'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        ]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.all()
        # Если пользователь авторизован, появдяется возможность добавить мероприятие
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context


def index(request):
    paginate_by = 3
    contact_list = Event.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    posts = Event.objects.all()
    cats = Category.objects.all()

    context = {
        'posts': posts,
        'cats': cats,
        'menu': menu,
        'title': 'Главная страница',
        'cat_selected': 0,
    }

    return render(request, 'events/index.html', context=context)


def about(request):
    return render(request, 'events/about.html', {'menu': menu, 'title': 'О сайте'})

from django.core.mail import send_mail

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()

            # Собрать список адресов для рассылки
            recipients = []
            if form.cleaned_data['role'] == 'sponsor':
                recipients = [contact.email for contact in Contact.objects.filter(role='sponsor')]
                message = 'Уважаемый спонсор,\n \n Мы рады, что вы подписались на рассылку. Если у Вас возникнут какие-либо вопросы или комментарии, пожалуйста, не стесняйтесь связаться с нами. \n \n С наилучшими пожеланиями, \n \n SPONSORSHIP! '
            elif form.cleaned_data['role'] == 'organizer':
                recipients = [contact.email for contact in Contact.objects.filter(role='organizer')]
                message = 'Уважаемый организатор, \n \n Мы рады, что вы подписались на рассылку. Мы предоставляем участникам-организаторам мероприятий возможность связаться с потенциальными спонсорами и получить необходимую поддержку для их мероприятий. \n \n На нашей платформе Вы можете легко связаться с потенциальными спонсорами и предоставить им коммерческое предложение. Мы гарантируем безопасность и защиту конфиденциальности наших пользователей, и мы проверяем всех потенциальных спонсоров, прежде чем размещать их на нашем сайте. \n \n Если у Вас есть какие-либо вопросы или комментарии, не стесняйтесь связаться с нами. \n \n С наилучшими пожеланиями, \n \n SPONSORSHIP!'

            # Отправить письма
            send_mail(
                'SPONSORSHIP.CLICK HERE',
                message,
                'sponsor.quest@mail.ru',
                recipients,
                fail_silently=False,
            )

            return redirect('home')
    else:
        form = ContactForm()

    return render(request, 'events/contact.html', {'form': form, 'menu': menu, 'title': 'Обратная связь'})


def categories(request, catid):
    if (request.GET):
        print(request.GET)
    return HttpResponse(f"<h1>Мероприятия по категориям</h1><p> {catid} </p>")


def archive(request, year):
    if int(year) > 2023:
        return redirect('home', permanent=False)

    return HttpResponse(f"<h1>Архив по годам</h1><p> {year} </p>")


@login_required
def addpage(request):
    if request.method == 'POST':
        form = AddEventForm(request.POST, request.FILES)
        if form.is_valid():
            # Собрать список адресов спонсоров для рассылки
            recipients = [contact.email for contact in Contact.objects.filter(role='sponsor')]
            # Сформировать сообщение с информацией о новом мероприятии
            message = f'Уважаемый спонсор,\n\nМы рады сообщить Вам, что на нашей платформе появилось новое мероприятие, которое может заинтересовать Вас. Вот краткая информация о нем:\n\nНазвание: {form.cleaned_data["title"]}\nОписание: {form.cleaned_data["description"]}\nДата: {form.cleaned_data["date"]}\nМесто: {form.cleaned_data["location"]}\nБюджет: {form.cleaned_data["budget"]}\n\nЕсли Вы хотите стать спонсором этого мероприятия или узнать больше деталей, пожалуйста, свяжитесь с нами по адресу sponsor.quest@mail.ru либо напрямую с организатором по адресу {form.cleaned_data["email"]} или по номеру {form.cleaned_data["phone_number"]}.\n\nС наилучшими пожеланиями,\n\nSPONSORSHIP!'
            # Отправить письма
            send_mail(
                'SPONSORSHIP.CLICK HERE',
                message,
                'sponsor.quest@mail.ru',
                recipients,
                fail_silently=False,
            )
            # Сохранить мероприятие в базе данных
            Event.objects.create(**form.cleaned_data)
            return redirect('home')
        else:
            form.add_error(None, 'Ошибка добавления мероприятия')
    else:
        form = AddEventForm()
    return render(request, 'events/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление мероприятия'})


def findsp(request):
    if request.method == 'POST':
        forms = AddSpForm(request.POST)
        if forms.is_valid():
            # Собрать список адресов организаторов для рассылки
            recipients = [contact.email for contact in Contact.objects.filter(role='organizer')]
            # Сформировать сообщение с информацией о новой анкете спонсора
            message = f'Уважаемый организатор,\n\nМы рады сообщить Вам, что на нашей платформе появилась новая анкета спонсора, которая может быть интересна Вам. Вот краткая информация о ней:\n\nИмя: {forms.cleaned_data["user"]}\nEmail: {forms.cleaned_data["email"]}\nО компании: {forms.cleaned_data["about"]}\nУсловия спонсора: {forms.cleaned_data["description"]}\n\nЕсли Вы хотите связаться с этим спонсором или узнать больше деталей, пожалуйста, напишите ему на указанный адрес электронной почты.\n\nС наилучшими пожеланиями,\n\nSPONSORSHIP!'
            # Отправить письма
            send_mail(
                'SPONSORSHIP.CLICK HERE',
                message,
                'sponsor.quest@mail.ru',
                recipients,
                fail_silently=False,
            )
            # Сохранить анкету спонсора в базе данных
            forms.save()
            return redirect('home')
    else:
        anketa = Sponsor.objects.all()
        forms = AddSpForm()
        return render(request, 'events/findsp.html',
                      {'menu': menu, 'anketa': anketa, 'form': forms, 'title': 'Спонсоры'})


@login_required
def delete_sp_view(request):
    if request.method == 'POST':
        sponsor = request.user.sponsor
        sponsor.delete()
        return redirect('home')
    return render(request, 'events/delete_sp.html')


# def login(request):
#     return HttpResponse("Авторизация")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def show_post(request, post_id):
    post = get_object_or_404(Event, pk=post_id)

    context = {
        'post': post,
        'menu': menu,
        'title': post.title,
        'cat_selected': post.cat_id,
    }
    return render(request, 'events/post.html', context=context)


def show_category(request, cat_id):
    posts = Event.objects.filter(cat_id=cat_id)
    cats = Category.objects.all()

    context = {
        'posts': posts,
        'cats': cats,
        'menu': menu,
        'title': 'Отображение по рубрикам',
        'cat_selected': cat_id,
    }
    return render(request, 'events/index.html', context=context)


class RegisterUser(DataMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'events/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'events/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('add_page')


def logout_user(request):
    logout(request)
    return redirect('login')
