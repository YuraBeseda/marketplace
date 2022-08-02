from django.urls import path

from marketplace import views

urlpatterns = [
    path("", views.index, name="index"),

    path("traders/", views.TraderListView.as_view(), name="trader-list"),
    path("traders/create", views.TraderCreateView.as_view(), name="trader-create"),
    path("traders/<int:pk>/", views.TraderDetailView.as_view(), name="trader-detail"),

    path("publications/", views.PublicationListView.as_view(), name="publication-list"),
    path("publications/create", views.publication_create_view, name="publication-create"),
    path("publications/<int:pk>/update/", views.PublicationUpdateView.as_view(), name="publication-update"),
    path("publications/<int:pk>/delete/", views.PublicationDeleteView.as_view(), name="publication-delete"),

    path("products/", views.ProductListView.as_view(), name="product-list"),
    path("products/<int:pk>", views.ProductDetailView.as_view(), name="product-detail"),
    path("products/create/", views.product_create_view, name="product-create"),
    path("products/<int:pk>/update/", views.ProductUpdateView.as_view(), name="product-update"),
    path("products/<int:pk>/delete/", views.ProductDeleteView.as_view(), name="product-delete"),
]

app_name = "marketplace"
