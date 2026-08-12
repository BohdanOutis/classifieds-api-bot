from aiogram import Router

from . import(
    main, 
    advert_creation,
    profile,
    admin,
    adverts,
    payments,
    for_others,
)

def get_routers() -> list[Router]:
    return [
        admin.router,
        main.router,
        advert_creation.router,
        profile.router,
        adverts.router,
        payments.router,
        for_others.router
    ]