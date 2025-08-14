from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from board.views import accept_response, delete_response
from accounts.views import ProfileUpdateView, ProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('allauth.urls')),
    path('account/profile/', ProfileView.as_view(), name='profile'),
    path('', include('board.urls')),
    path('responses/accept/<int:pk>/', accept_response, name='accept_response'),
    path('accounts/profile/', ProfileView.as_view(), name='profile'),
    path('accounts/profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('responses/accept/<int:pk>/', accept_response, name='accept_response'),
    path('responses/delete/<int:pk>/', delete_response, name='delete_response'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)