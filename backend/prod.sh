set -e

echo "=== [PROD START] Проверка и запуск миграций ==="
uv run alembic upgrade head

echo "=== [PROD START] Запуск FastAPI приложения ==="
uv run python entrypoints/run.py