from django.urls import path, include
from . import views


app_name='home'
bucket_urls=[
    path('', views.BucketHomeView.as_view(), name='bucket'),
    path('delete/<str:key>', views.BucketDeleteView.as_view(), name='bucket_delete'),
    path('download/<str:key>', views.BucketDownloadView.as_view(), name='bucket_download'),
    path('Upload/<str:key>', views.BucketUploadView.as_view(), name='bucket_upload'),

]
urlpatterns=[
    path('', views.HomeView.as_view(),name='home'),
    path('aboutme/', views.AboutMeView.as_view(),name='about_me'),
    path('faq/', views.FAQ.as_view(),name='faq'),
    path('product/',views.ProductView.as_view(), name='product'),
    path('product/detail/<int:product_id>/', views.ProductDetailView.as_view(), name='detail'),
    path('product/comment/<int:product_id>/',views.AddCommentView.as_view(), name='add_comment'),
    path('bucket/', views.BucketHomeView.as_view(), name='bucket'),
    path('bucket/', include(bucket_urls)),
    path('product/category/',views.CategoryView.as_view(),name='category'),
    path('product/category/detail/<slug:slug_id>',views.CategoryDetailView.as_view(),name='category_detail')

    ]