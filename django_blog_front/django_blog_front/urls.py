from django.conf.urls import handler403, handler400, handler404, handler500
from django.urls import path, include

handler400 = 'blog.views.custom_400'
handler403 = 'blog.views.custom_403'
handler404 = 'blog.views.custom_404'
# handler500 = 'blog.views.custom_500'


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('projects/', include('projects.urls'))
]
