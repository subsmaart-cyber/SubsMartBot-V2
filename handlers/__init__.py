from .start import router as start_router
from .profile import router as profile_router
from .wallet import router as wallet_router
from .products import router as products_router
from .deposit import router as deposit_router
from .purchase import router as purchase_router
from .history import router as history_router
from .referral import router as referral_router
from .reviews import router as reviews_router
from .support import router as support_router
from .admin import router as admin_router
from .broadcast import router as broadcast_router
from .stats import router as stats_router
from .force_join import router as force_join_router
from .maintenance import router as maintenance_router
from .settings import router as settings_router
from .stock import router as stock_router


def register_handlers(dp):
    dp.include_router(start_router)
    dp.include_router(profile_router)
    dp.include_router(wallet_router)
    dp.include_router(products_router)
    dp.include_router(deposit_router)
    dp.include_router(purchase_router)
    dp.include_router(history_router)
    dp.include_router(referral_router)
    dp.include_router(reviews_router)
    dp.include_router(support_router)
    dp.include_router(admin_router)
    dp.include_router(broadcast_router)
    dp.include_router(stats_router)
    dp.include_router(force_join_router)
    dp.include_router(maintenance_router)
    dp.include_router(settings_router)
    dp.include_router(stock_router)
