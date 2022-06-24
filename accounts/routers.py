
from core.routers import CoreRouter
from .viewsets import AccountsViewSet


router = CoreRouter()
router.register("account", AccountsViewSet, basename="accounts")
