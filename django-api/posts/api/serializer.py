from rest_framework import serializers
from posts.models import Post
from users.api.serializer import UserSerializer
from categories.api.serializers import CategorySerializer


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    category = CategorySerializer()
    miniature = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['title','content','slug','miniature','created_at','description','published','user','category']
    def get_miniature(self, obj):
        return obj.miniature.url  # => /media/posts/img/portada_ldin.png
        