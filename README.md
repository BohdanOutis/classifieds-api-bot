# Enterprise Classifieds Bot & Admin Dashboard

Комплексний асинхронний бекенд-сервіс та Telegram-бот для управління системою оголошень, підписок та автоматизованої обробки даних, побудований на сучасних стандартах розробки.

## Основні можливості

- **RESTful API**: Швидкий та безпечний бекенд на FastAPI з валідацією через Pydantic v2.
- **Telegram Bot**: Інтерактивний бот на aiogram 3.x для користувачів з підтримкою платежів та управління оголошеннями.
- **Автоматизація (APScheduler)**: Форові задачі для моніторингу та автоматичного оновлення статусу VIP-підписок.
- **Структуроване логування**: Повна інтеграція `structlog` із контекстними подіями у форматі `snake_case`.
- **Безпека**: Хешування паролів через `pwdlib[argon2]`, захист маршрутів за допомогою API-ключів та JWT.
- **База даних**: Надійна робота з PostgreSQL через SQLAlchemy 2.0 (Async) та міграції за допомогою Alembic.
- **Фронтенд**: Зручна веб-панель керування на React, TypeScript та Tailwind CSS.

## Архітектура проєкту

```
ClassifiedsBot/
├── frontend/             # Веб-інтерфейс (React + TS + Tailwind)
├── src/
│   ├── api/              # FastAPI бекенд
│   │   ├── v1/
│   │   │   ├── endpoints/# Роутери (users, ads, payments, stats)
│   │   │   ├── schemas/  # Pydantic моделі валідації
│   │   │   └── services/ # Бізнес-логіка бекенду
│   │   ├── dependencies.py
│   │   └── main.py       # Головна точка входу API
│   ├── bot/              # Telegram бот (aiogram 3.x)
│   │   ├── handlers/     # Обробники повідомлень та команд
│   │   ├── keyboards/    # Клавіатури
│   │   ├── middlewares/  # Мідлварі бота
│   │   └── tasks/        # Форові задачі
│   ├── core/             # Системні налаштування
│   │   ├── config.py     # Конфігурація середовища
│   │   ├── database.py   # Підключення до БД (AsyncSession)
│   │   └── security.py   # Безпека та верифікація
│   └── models/           # SQLAlchemy ORM моделі
├── .env.example          # Зразки змінних середовища
├── compose.yaml          # Конфігурація Docker Compose
├── Dockerfile            # Інструкція з конфігурації контейнера
└── pyproject.toml        # Залежності та конфігурація проєкту (uv)
```

## Встановлення та запуск

### 1. Системні вимоги

- Python 3.11+
- PostgreSQL
- uv
- React
- ReduxToolkit

### 2. Клонування та налаштування середовища

Клонуйте репозиторій та створіть файл `.env` на основі `.env.example`:
```bash
cp .env.example .env
```
Заповніть необхідні параметри (дані підключення до БД, токен Telegram-бота тощо).

### 3. Встановлення залежностей Python

Проєкт використовує uv для керування залежностями:
```bash
uv sync
```

### 4. Запуск міграцій бази даних

Створіть структуру таблиць у PostgreSQL через Alembic:
```bash
alembic upgrade head
```
## Використання

Запуск API-сервера
```bash
fastapi dev src/api/main.py
```
Документація Swagger буде доступна за адресою: http://127.0.0.1:8000/docs

Запуск Telegram-бота
```bash
python -m src.bot
```
Запуск Frontend-частини
Перейдіть у папку frontend та запустіть сервер розробки:
```bash
cd frontend
npm install
npm run dev
```
## Структура бази даних

Основні таблиці в PostgreSQL:
- `users` — Користувачі системи та їхні Telegram ID
- `advertisements` — Оголошення користувачів
- `advertisement_photo` — Зображення до оголошень
- `payments` — Транзакції та платежі
- `news_sources` — Джерела новин
- `processed_news` — Кеш оброблених новин

## Логування
Логи пишуться через structlog у структурованому форматі, що спрощує моніторинг помилок і подій системи в реальному часі. Рівні логування включають стандартні INFO, WARNING, ERROR.

## Безпека
API захищене за допомогою API-ключа(API__SERVER_SECRET_KEY в .env), що виключає несанкціонований доступ до системних ендпоінтів.
=======
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