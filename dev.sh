# Остановить выполнение при возникновении ошибки
set -e

# Перейти в директорию скрипта
cd "$(dirname "$0")"

VENV_DIR=".venv"

# Активация виртуального окружения
if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
else
    echo "Warning: Virtual environment not found. Using system environment."
fi

# Вывод информации о запуске
echo "Starting FastAPI server..."
echo "Swagger docs: http://127.0.0.1:8000/docs"
echo "------------------------------------------------------------"

# Запуск сервера
uvicorn entrypoints.run:app --reload --host 0.0.0.0 --port 8000