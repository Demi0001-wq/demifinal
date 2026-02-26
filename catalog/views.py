from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.core.exceptions import PermissionDenied
from catalog.models import Product, Contact


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductTemplateView(TemplateView):
    template_name = 'catalog/contacts.html'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ('name', 'description', 'image', 'category', 'price', 'is_published')
    success_url = reverse_lazy('catalog:list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ('name', 'description', 'image', 'category', 'price', 'is_published')
    success_url = reverse_lazy('catalog:list')

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        if user == product.owner or user.is_superuser or user.groups.filter(name='Product Moderator').exists():
            return True
        return False

    def handle_no_permission(self):
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:list')

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        if user == product.owner or user.is_superuser:
            return True
        return False

    def handle_no_permission(self):
        raise PermissionDenied


class ContactCreateView(CreateView):
    model = Contact
    fields = ('name', 'email', 'message')
    success_url = reverse_lazy('catalog:contacts')
    template_name = 'catalog/contacts.md'
