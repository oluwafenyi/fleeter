
from core.routers import CoreRouter
from .viewsets import AccountsViewSet


router = CoreRouter()
router.register("accounts", AccountsViewSet, basename="accounts")
