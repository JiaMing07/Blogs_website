from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    path('', views.home, name='home'),
    path('detail/<pk>/', views.blog_detail, name="blog_detail"),
    path('submit/<pk>', views.submit_comment, name="submit_comment"),
    path('delete/<pk>/<comment_id>', views.delete_comment, name="delete_comment"),
    path('list/', views.show_list, name="show_list"),
    path('category/', views.category, name="category"),
    path('category/<tag>', views.show_category, name="show_category"),
    path('search/', views.search, name="search"),
    path('search/<keyword>/<choice>/<options>', views.go_to_search, name="go_to_search")
]