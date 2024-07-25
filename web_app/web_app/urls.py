from django.contrib import admin
from django.urls import path, include
from user import views as user_view
from django.contrib.auth import views as auth_views # type: ignore
from django.conf import settings
from django.conf.urls.static import static
from ganache_blockchain import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("api.urls")),
    path("register/", user_view.register, name="user-register"),
    path("", auth_views.LoginView.as_view(template_name="user/login.html"), name= "user-login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="user/logout.html"), name= "user-logout"),
    path("perfil/", user_view.perfil, name="user-perfil"),
    path("perfil/update", user_view.perfil_update, name="user-perfil-update"),
    path('blockchain/', include('blockchain.urls')),
    path('contract/', views.my_contract_view, name='my_contract_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
