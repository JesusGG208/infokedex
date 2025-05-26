from django.urls import path
from compare import views

app_name = 'compare'
urlpatterns = [
    path('', views.PokemonCompareView.as_view(), name='compare'),
]