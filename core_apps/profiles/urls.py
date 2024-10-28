from django.urls import path
from .views import *

urlpatterns = [
    path("all/", ProfileListApiView.as_view(), name = "all-profiles"),
    path("me/", ProfileDetailApiView.as_view(), name = "my-profile"),
    path("me/update/", UpdateProfileApiView.as_view(), name = "update-profile"),
    path("me/followers/", FollowerListView.as_view(), name = "followers"),
    path("<uuid:user_id>/follow/", FollowApiView.as_view(), name = "follow"),
    path("<uuid:user_id>/unfollow/", UnfollowApiView.as_view(), name = "unfollow")

]