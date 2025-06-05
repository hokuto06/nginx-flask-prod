from rest_framework import serializers
from posts.models import Post
from categories.models import Category
from posts.api.s3 import get_presigned_url
from users.api.serializer import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(read_only=True)
    user = UserSerializer(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    miniature_url = serializers.SerializerMethodField()

    def get_miniature_url(self, obj):
        if obj.miniature:
            return get_presigned_url(obj.miniature.name)
        return None

    class Meta:
        model = Post
        fields = [
            'title', 'content', 'slug', 'description',
            'miniature_url', 'miniature',
            'published', 'created_at',
            'user', 'category'
        ]
