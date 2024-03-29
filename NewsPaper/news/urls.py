from django.urls import path, include

# Импортируем созданное нами представление
from .views import NewCreate, NewDelete, NewDetail, NewsList, NewUpdate, subscriptions, upgrade_user


urlpatterns = [
    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым,
    # чуть позже станет ясно почему.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('', NewsList.as_view(), name='new_list'),
    path('<int:pk>', (NewDetail.as_view()), name='new_detail'),
    path('create/', NewCreate.as_view(), name='new_create'),
    path('upgrade/', upgrade_user, name='account_upgrade'),
    path('<int:pk>/update/', NewUpdate.as_view(), name='new_update'),
    path('<int:pk>/delete/', NewDelete.as_view(), name='new_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('i18n/', include('django.conf.urls.i18n')),
]
