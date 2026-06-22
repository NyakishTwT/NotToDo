# NotToDo

Небольшое приложение на базе Archtool 

### Стек
`FastAPI`  `Archtool`  `SQLAlchemy`  `Pydantic`  `Uvicorn`  `uv`  `Alembic` `Web_fractal`

---
Интерактивная документация API (Swagger): http://127.0.0.1:8000/docs

## Быстрый запуск

```bash
git clone https://github.com/NyakishTwT/NotToDo.git
cd NotToDo
uv sync
cd backend
./dev.sh  # или ./prod.sh


## Структура проекта:
NotToDo
 ┣ backend
 ┃ ┣ alembic/                  # Управление миграциями базы данных
 ┃ ┃ ┗ env.py                  # Конфигурация среды Alembic
 ┃ ┣ app/                      # Основной код приложения
 ┃ ┃ ┣ archtool_conf/          # Настройка слоев и автоматического DI
 ┃ ┃ ┣ core_integrations/      # Ручная регистрация системных зависимостей
 ┃ ┃ ┣ todos/                  # Модуль управления задачами
 ┃ ┃ ┗ users/                  # Модуль управления пользователями
 ┃ ┃   ┣ controllers.py        # API эндпоинты
 ┃ ┃   ┣ dms.py                # Описание интерфейсов данных (Data Mappers)
 ┃ ┃   ┣ dtos.py               # Валидация входных/выходных данных (Pydantic DTO)
 ┃ ┃   ┣ interfaces.py         # Абстрактные контракты компонентов (ABC)
 ┃ ┃   ┣ models.py             # ORM-модели базы данных (SQLAlchemy)
 ┃ ┃   ┣ repos.py              # Слой доступа к данным (Repository)
 ┃ ┃   ┗ services.py           # Слой чистой бизнес-логики (Service)
 ┃ ┣ entrypoints/
 ┃ ┃ ┗ run.py                  # Главная точка входа для запуска приложения
 ┃ ┣ dev.sh / prod.sh          # Скрипты автоматического запуска окружения
 ┃ ┗ alembic.ini               # Конфигурационный файл Alembic
 ┣ pyproject.toml              # Конфигурация проекта и менеджер зависимостей (uv)
 ┗ uv.lock                     # Зафиксированные версии пакетов


