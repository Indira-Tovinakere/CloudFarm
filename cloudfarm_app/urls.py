from django.urls import path
from . import views
from .views import crop_fertilizer_prediction
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login, name='login'),
    path("predict/", crop_fertilizer_prediction, name="predict"),
    path('fertilizers/', views.fertilizer_list, name='fertilizer_list'),
    path('fertilizers/<int:pk>/', views.fertilizer_detail, name='fertilizer_detail'),
    
    path('home/', views.home, name='home'),  # Home page
    path('fertilizer_list/', views.fertilizer_list, name='fertilizer_list'),  # Fertilizer list page
    path('aboutus/', views.about_us, name='Aboutus'), 
    path('logout/', views.logout_view, name='logout'),
    path('buy-products/', views.buy_products, name='buy_products'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<str:product_name>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

