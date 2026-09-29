# Classifieds API & Admin Dashboard

Full-stack веб-додаток для управління оголошеннями та Telegram-ботом.

## Технологічний стек

- **Backend & API:** Python 3.11+, FastAPI (AsyncIO), Async SQLAlchemy 2.0, PostgreSQL, Alembic, Pydantic v2
- **Telegram Bot:** Aiogram 3
- **Frontend Admin Panel:** React 19, TypeScript, Vite, Redux Toolkit, Tailwind CSS v4, Axios
- **DevOps & Infrastructure:** Docker, Docker Compose

## Основні можливості

- **REST API:** Повністю асинхронна архітектура з валідацією через Pydantic v2.
- **Авторизація:** Захист за допомогою заголовочного `X-API-Key` та CORS middleware.
- **Admin Dashboard:** Адмін-панель для перегляду статистики, фільтрації за статусами/Telegram ID та створення оголошень з live-preview.
- **База даних:** Асинхронні міграції через Alembic та робота з PostgreSQL.
