from django.urls import include, path

urlpatterns = [
    # path('', include(router_v1.urls)),
    path('', include('foods.urls')),
    path('', include('users.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
