from rest_framework import mixins, viewsets, permissions
from .models import Manager, Client
from .serializers import ManagerSerializer, ClientSerializer, ClientCreateSerializer
from django.views.decorators.csrf import csrf_exempt


class ManagerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    permission_classes = [permissions.IsAdminUser]


@csrf_exempt
class ClientViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    queryset = Client.objects.select_related('manager', 'package')
    serializer_class = ClientSerializer
    filterset_fields = ['status', 'country']
    search_fields = ['full_name', 'phone']

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_serializer_class(self):
        return ClientCreateSerializer if self.action == 'create' else ClientSerializer
        