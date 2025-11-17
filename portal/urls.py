from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("items/", views.ItemListView.as_view(), name="item_list"),
    path("item/<int:pk>/", views.ItemDetailView.as_view(), name="item_detail"),
    path("item/<int:pk>/comment/", views.CommentCreateView.as_view(), name="add_comment"),
    path("report/", views.ItemReportCreateView.as_view(), name="report_item"),
    path("report/success/", views.ReportSuccessView.as_view(), name="report_success"),
]