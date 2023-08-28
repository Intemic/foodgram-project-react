from django.urls import include, path

urlpatterns = [
    path('', include('foods.urls')),
    path('', include('users.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
