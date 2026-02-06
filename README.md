
Backend для сервиса проверки файлов (фото/видео) на подлинность.

## Структура проекта
```
app/
  api/        # роуты FastAPI
  models/     # Pydantic схемы
  services/   # бизнес-логика
  storage/    # временное/постоянное хранение
frontend/     # скелет будущего фронтенда
```

## Запуск
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Базовые эндпоинты
- `GET /health` — проверка состояния сервиса.
- `POST /analyze` — загрузка файла для проверки.
- `GET /analyze/{job_id}` — статус и результат проверки.

## Пример использования
```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/file.jpg"
```

```bash
curl "http://127.0.0.1:8000/analyze/<job_id>"
```

## Важное
Текущая реализация возвращает заглушку результата (fake_probability = 0.5).
Нужно подключить ML-модель и хранилище для реальной проверки.
