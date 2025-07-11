from rest_framework.viewsets import ModelViewSet
from posts.models import Post
from posts.api.serializer import PostSerializer
from posts.api.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


class PostApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(published=True)
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['slug','category','category__slug']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)