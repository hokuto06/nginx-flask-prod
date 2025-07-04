from rest_framework.permissions import BasePermission
from comments.models import Comment

class IsOwnerOrReadAndCreateOnly(BasePermission):
    # def has_permission(self, request, view):
    #     if request.method == 'GET'  or request.method == 'POST':
    #         return True
    #     else:
    #         id_comment = view.kwargs['pk']
    #         comment = Comment.objects.get(pk=id_comment)

    #         id_user = request.user.pk
    #         id_user_comment = comment.user_id

    #         if id_user == id_user_comment:
    #             return True
            
    #         return False
    def has_permission(self, request, view):
        if request.method in ['GET', 'POST']:
            return True
        
        id_comment = view.kwargs.get('pk')
        if id_comment is None:
            return False  # o True si querés permitir sin pk

        try:
            comment = Comment.objects.get(pk=id_comment)
        except Comment.DoesNotExist:
            return False

        return request.user.pk == comment.user_id

