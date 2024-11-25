from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    #profile urls
    path('',views.ProductView.as_view(),name = 'home'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('product_detail/<int:pk>',views.ProductDetailView.as_view(),name='product_detail'),
    path('address/', views.address,name='address'),
    path('orders/',views.order,name='orders'),
    path('checkout/',views.checkout,name='checkout'),
    path('paymentdone/',views.payment_done,name='paymentdone'),
    path('search/',views.search,name='search'),

        # product urls
    path('bottomwears/', views.bottomwears,name='bottomwears'),
    path('bottomwears/<slug:data>',views.bottomwears,name='bottomwearsdata'),
    path('topwears/',views.topwears,name='topwears'),
    path('topwears/<slug:data>',views.topwears,name='topwearsdata'),
    path('sleepwears/',views.sleepwears,name='sleepwears'),
    path('sleepwears/<slug:data>',views.sleepwears,name='sleepwearsdata'),
    path('shoes/',views.shoes,name='shoes'),
    path('shoes/<slug:data>',views.shoes,name='shoesdata'),
    path('jackets/',views.jackets,name='jackets'),
    path('jackets/<slug:data>',views.jackets,name='jacketsdata'),
    path('blazzers/',views.blazzers,name='blazzers'),
    path('blazzers/<slug:data>',views.blazzers,name='blazzersdata'),
    path('shirts/',views.shirts,name='shirts'),
    path('shirts/<slug:data>',views.shirts,name='shirtsdata'),
    path('jeans/',views.jeans,name='jeans'),
    path('jeans/<slug:data>',views.jeans,name='jeansdata'),
    
    # CART-URLS
    path('add_to_cart/',views.add_to_cart , name='add_to_cart'),
    path('cart/',views.show_cart,name='cart'),
    path('pluscart/',views.plus_cart,name='pluscart'),
    path('minuscart/',views.minus_cart,name='minuscart'),
    path('removecart/',views.remove_cart,name='removecart'),
    



] +static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)

