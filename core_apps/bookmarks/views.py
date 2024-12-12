from rest_framework import generics, permissions
from .models import Bookmark
from .serializers import BookmarkSerializer
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError, NotFound
from core_apps.articles.models import Article
from uuid import UUID

class BookmarkCreateView(generics.CreateAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        article_id = self.kwargs.get('article_id')

        if article_id:
            try:
                article = Article.objects.get(id = article_id)
            except Article.DoesNotExist:
                raise ValidationError("Invalid article_id provided")
        else:
            raise ValidationError("article_id is required!")
        
        try:
            serializer.save(user = self.request.user, article = article)
        except IntegrityError:
            raise ValidationError("You have already bookmarked this article")

class BookmarkDestroyView(generics.DestroyAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self): # gets specific bookmark instance, which the user is trying to delete
        user = self.request.user
        article_id = self.kwargs.get("article_id")

        try: # Validating whether the article ID is a valid UUID version 4
            UUID(str(article_id), version=4) # We are converting our article ID to a string before passing it to the UUID function
        except ValueError:
            raise ValidationError("Invalid article_id provided")
        
        try:
            bookmark = Bookmark.objects.get(user = user, article__id = article_id)
        except Bookmark.DoesNotExist:
            raise NotFound("Bookmark not found or it doesn't belong to you")
        
        return bookmark
    
    def perform_destroy(self, instance):
        user = self.request.user
        if instance.user != user:
            raise ValidationError("YOU CAN NOT DELETE A BOOKMARK THAT IS NOT YOURS")
        
        instance.delete()