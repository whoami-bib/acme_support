from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, DepartmentViewSet, TicketViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'tickets', TicketViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
