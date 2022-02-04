from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import CreateProductForm, UpdateProductForm
from .models import Category, Product
from .permissions import IsAdminCheckMixin
from cart.cart import Cart


class SearchListView(ListView):
    model = Product
    # Product.objects.all()
    template_name = 'search.html'
    context_object_name = 'results'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchListView, self).get_context_data()
        context['search_word'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        queryset = super(SearchListView, self).get_queryset()
        search_word = self.request.GET.get('q')
        if not search_word:
            queryset = Product.objects.none()
        else:
            if len(search_word) < 3:
                queryset = Product.objects.none()
            else:
                queryset = queryset.filter(name__icontains=search_word)
        return queryset

class CategoryListView(ListView):
    model = Category
    # Category.objects.all()
    template_name = 'index.html'
    context_object_name = 'categories'


class ProductListView(ListView):
    model = Product
    # Product.objects.all()
    template_name = 'list.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset() # all
        slug = self.kwargs.get('slug')
        filter_word = self.request.GET.get('filter')
        if filter_word:
            queryset = queryset.filter(category__slug=slug,
                                       status=filter_word)
        else:
            queryset = queryset.filter(category__slug=slug)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        context['slug'] = self.kwargs.get('slug')
        return context


class ProductDetailView(DetailView):
    model = Product
    # Product.objects.get()
    template_name = 'detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'


class ProductCreateView(IsAdminCheckMixin, CreateView):
    model = Product
    # Product.objects.create()
    template_name = 'create_product.html'
    form_class = CreateProductForm

    # def get_success_url(self):
    #     return reverse('detail',
    #                    kwargs={'product_id': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['product_form'] = self.get_form()
        return context


class ProductUpdateView(IsAdminCheckMixin, UpdateView):
    model = Product
    template_name = 'update_product.html'
    form_class = UpdateProductForm
    pk_url_kwarg = 'product_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['product_form'] = self.get_form()
        return context


class ProductDeleteView(IsAdminCheckMixin, DeleteView):
    model = Product
    # Product.objects.get().delete()
    template_name = 'delete_product.html'
    pk_url_kwarg = 'product_id'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        slug = self.object.category.slug
        self.object.delete()
        return redirect('list', slug)



