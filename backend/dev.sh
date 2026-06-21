
set -e

cd "$(dirname "$0")"
export ARCHTOOL_VERBOSE=1
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Вывод информации о запуске
echo "Starting FastAPI server via UV..."
echo "Swagger docs: http://127.0.0.1:8000/docs"
echo "------------------------------------------------------------"


uv run uvicorn entrypoints.run:app --reload --host 0.0.0.0 --port 8000