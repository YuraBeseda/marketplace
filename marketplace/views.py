from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.list import MultipleObjectMixin

from marketplace.forms import ProductSearchForm, ProductForm, PublicationForm, TraderCreationForm, TraderSearchForm
from marketplace.models import Trader, Publication, Product


@login_required
def index(request):
    return HttpResponseRedirect(reverse_lazy("marketplace:trader-detail", args=[request.user.id]))


class TraderCreateView(generic.CreateView):
    model = Trader
    form_class = TraderCreationForm


class TraderListView(LoginRequiredMixin, generic.ListView):
    model = Trader
    paginate_by = 10
    queryset = Trader.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TraderListView, self).get_context_data(**kwargs)

        username = self.request.GET.get("model", "")

        context["search_form"] = TraderSearchForm(initial={"nickname": username})

        return context

    def get_queryset(self):
        form = TraderSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(username__icontains=form.cleaned_data["nickname"])

        return self.queryset


class TraderDetailView(LoginRequiredMixin, generic.DetailView, MultipleObjectMixin):
    model = Trader
    queryset = Trader.objects.all()
    paginate_by = 3

    def get_context_data(self, **kwargs):
        user = self.get_object()
        publication_list = Publication.objects.filter(author=user)
        product_list = Product.objects.filter(author=user)[:6]
        context = super(TraderDetailView, self).get_context_data(object_list=publication_list, **kwargs)
        context["product_list"] = product_list
        return context


class PublicationListView(LoginRequiredMixin, generic.ListView):
    model = Publication
    queryset = Publication.objects.all().select_related("author")
    paginate_by = 5


@login_required
def publication_create_view(request):
    context = {}
    if request.method == "POST":
        form = PublicationForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            text = form.cleaned_data.get("text")
            obj = Publication.objects.create(
                title=title,
                author=request.user,
                text=text,
            )
            obj.save()
        return HttpResponseRedirect(reverse_lazy("blog:index"))
    else:
        form = PublicationForm()
    context['form'] = form
    return render(request, "marketplace/publication_form.html", context)


class PublicationUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Publication
    fields = ["title", "text"]
    success_url = reverse_lazy("blog:index")


class PublicationDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Publication
    success_url = reverse_lazy("blog:index")


class ProductListView(LoginRequiredMixin, generic.ListView):
    model = Product
    paginate_by = 20
    queryset = Product.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")
        author = self.request.GET.get("author", "")

        context["search_form"] = ProductSearchForm(initial={"name": name, "author": author})

        return context

    def get_queryset(self):
        form = ProductSearchForm(self.request.GET)

        if form.is_valid():
            if form.cleaned_data["author"]:
                return self.queryset.filter(
                    name__icontains=form.cleaned_data["name"],
                    author_id=form.cleaned_data["author"]
                )
            else:
                return self.queryset.filter(
                    name__icontains=form.cleaned_data["name"]
                )

        return self.queryset


class ProductDetailView(LoginRequiredMixin, generic.DetailView):
    model = Product


@login_required
def product_create_view(request):
    context = {}
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            img = form.cleaned_data.get("image")
            desc = form.cleaned_data.get("description")
            price = form.cleaned_data.get("price")
            obj = Product.objects.create(
                name=name,
                author=request.user,
                image=img,
                description=desc,
                price=price
            )
            obj.save()
        return HttpResponseRedirect(reverse_lazy("blog:index"))
    else:
        form = ProductForm()
    context['form'] = form
    return render(request, "marketplace/product_form.html", context)


class ProductUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Product
    fields = ["name", "image", "description", "price"]


class ProductDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Product
    success_url = reverse_lazy("blog:index")
