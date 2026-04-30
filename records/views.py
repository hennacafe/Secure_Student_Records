from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import BasePermission, IsAuthenticated, IsAdminUser
from .models import StudentRecord
from .serializers import StudentRecordSerializer


class IsAdminOrFaculty(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=['Admin', 'Faculty']).exists() #[cite: 1]

class StudentRecordViewSet(ModelViewSet):
    serializer_class = StudentRecordSerializer

    def get_queryset(self):
    
        user = self.request.user
        if user.groups.filter(name__in=['Admin', 'Faculty']).exists():
            return StudentRecord.objects.all()
        return StudentRecord.objects.filter(owner=user)

    def perform_create(self, serializer):
        
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAdminUser] 
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAdminOrFaculty] 
        else:
            permission_classes = [IsAuthenticated] 
        return [permission() for permission in permission_classes]