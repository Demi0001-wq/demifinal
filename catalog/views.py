from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.core.exceptions import PermissionDenied
from django.core.cache import cache
from catalog.models import Product, Contact
from catalog.forms import ProductForm
from catalog.services import get_products_by_category
from config.settings import CACHE_ENABLED


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        if CACHE_ENABLED:
            key = 'products_list'
            products = cache.get(key)
            if products is None:
                products = super().get_queryset()
                if not self.request.user.groups.filter(name='Product Moderator').exists() and not self.request.user.is_superuser:
                    products = products.filter(is_published=True)
                cache.set(key, list(products))
            return products

        queryset = super().get_queryset()
        if not self.request.user.groups.filter(name='Product Moderator').exists() and not self.request.user.is_superuser:
            queryset = queryset.filter(is_published=True)
        return queryset


class CategoryProductListView(ListView):
    template_name = 'catalog/category_product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return get_products_by_category(self.kwargs.get('pk'))


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        if CACHE_ENABLED:
            key = f'product_{self.kwargs.get("pk")}'
            product = cache.get(key)
            if product is None:
                product = super().get_object(queryset)
                cache.set(key, product)
            return product
        return super().get_object(queryset)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('home')
    template_name = 'catalog/product_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('home')
    template_name = 'catalog/product_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        user = self.request.user
        obj = self.get_object()
        return user == obj.owner or user.groups.filter(name='Product Moderator').exists() or user.has_perm('catalog.can_unpublish_product')


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('home')
    template_name = 'catalog/product_confirm_delete.html'

    def test_func(self):
        user = self.request.user
        obj = self.get_object()
        return user == obj.owner or user.groups.filter(name='Product Moderator').exists() or user.has_perm('catalog.delete_product')


class ContactTemplateView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = Contact.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"New contact message:\nName: {name}\nPhone: {phone}\nMessage: {message}")
        return self.get(request, *args, **kwargs)
