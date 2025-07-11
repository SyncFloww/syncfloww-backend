from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Brand
from .serializers import BrandSerializer

class BrandListCreateView(generics.ListCreateAPIView):
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Brand.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BrandDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Brand.objects.filter(user=self.request.user)
