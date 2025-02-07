from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('vpn/', include('vpn.urls'))
]

#handler404="main.views.handle_not_found"