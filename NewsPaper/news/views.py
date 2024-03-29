from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group, User
from django.core.cache import cache
from django.db.models import Exists, OuterRef
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .filters import PostFilter
from .forms import NewForm
from .models import Author, Category, Post, Subscription
import logging
from .serializers import PostSerializer
from rest_framework import viewsets

# logger = logging.getLogger('django')
logger = logging.getLogger(__name__)


class NewsList(ListView):
    # logger.info('INFO')
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-creation_date'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        context['is_author'] = self.request.user.groups.filter(name='Authors').exists()
        return context


class NewDetail(DetailView):
    # logger.info('INFO')
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'product-{self.kwargs["pk"]}',
                        None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает
        # значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)

        return obj


class NewCreate(PermissionRequiredMixin, CreateView):
    # logger.info('INFO')
    # Указываем нашу разработанную форму
    permission_required = ('news.add_post',)
    raise_exception = True
    form_class = NewForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'new_edit.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form)


class NewUpdate(PermissionRequiredMixin, UpdateView):
    # logger.info('INFO')
    permission_required = ('news.change_post',)
    form_class = NewForm
    model = Post
    template_name = 'new_edit.html'


class NewDelete(PermissionRequiredMixin, DeleteView):
    # logger.info('INFO')
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'new_delete.html'
    success_url = reverse_lazy('new_list')


@login_required
def upgrade_user(request):
    # logger.info('INFO')
    user = request.user
    group = Group.objects.get(name='Authors')
    print(user)
    print(group)

    if not user.groups.filter(name='Authors').exists():
        group.user_set.add(user)
        Author.objects.create(author_name=User.objects.get(pk=user.id))
    return redirect('/news')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )


class PostNewsViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Post.objects.filter(post_type='N')
    serializer_class = PostSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly]

    # @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    # def highlight(self, request, *args, **kwargs):
    #     snippet = self.get_object()
    #     return Response(snippet.highlighted)
    #
    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class PostArticleViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Post.objects.filter(post_type='A')
    serializer_class = PostSerializer

    # def get_queryset(self):
    #     """
    #     This view should return a list of all the purchases
    #     for the currently authenticated user.
    #     """
    #     user = self.request.user
    #     return Purchase.objects.filter(purchaser=user)
    #