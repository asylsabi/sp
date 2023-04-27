from django.urls import path, re_path


from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('categories/<int:catid>/', categories),
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive),
    path('addpage/',login_required(addpage),name='add_page'),
    re_path(r'^accounts/login/$', LoginView.as_view(), name='login'),
    path('findsp/', login_required(findsp), name='find_sp'),
    path('delete-sp/', delete_sp_view, name='delete_sp'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<int:post_id>/',show_post,name='post'),
    path("category/<int:cat_id>/", show_category, name='category')
]