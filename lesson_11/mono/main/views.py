from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Card
from .serializer.card_serializer import CardSerializer
from .permissions import IsCardOwner

class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated, IsCardOwner]

    def get_queryset(self):
        return Card.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['patch'])
    def freeze(self, request, pk=None):
        card = self.get_object()
        card.is_frozen = True
        card.save()
        return Response({'message': 'Card frozen successfully.'})

    @action(detail=True, methods=['patch'])
    def unfreeze(self, request, pk=None):
        card = self.get_object()
        card.is_frozen = False
        card.save()
        return Response({'message': 'Card unfrozen successfully.'})