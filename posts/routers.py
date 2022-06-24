
from core.routers import CoreRouter
from .viewsets import PostsViewSet

router = CoreRouter()
router.register("post", PostsViewSet, basename="posts")
