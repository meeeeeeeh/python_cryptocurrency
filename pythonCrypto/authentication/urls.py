from django.urls import path, reverse_lazy
from .views import signup, login_view, wallet
from django.contrib.auth import views as authViews

app_name = 'authentication'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', authViews.LogoutView.as_view(next_page=reverse_lazy('authentication:login')), name='logout'),
    path('wallet/', wallet, name='wallet')

]
