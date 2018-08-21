import os

from rest_framework.routers import DefaultRouter

from . views import BookViewSet


inventories = DefaultRouter()
inventories.register(r'books', BookViewSet)

cwd = os.path.abspath(os.path.dirname(__file__)).split('/')[-1]
app_name = cwd  # current working directory
urlpatterns = [
]

urlpatterns += inventories.urls
