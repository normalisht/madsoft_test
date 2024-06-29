# madsoft_test

* [Задание](https://docs.google.com/forms/d/e/1FAIpQLSeFG6LOI0i165oLR4mwHglMt_NaVcqak-Zz51hK8mnZ4SRJTQ/viewform)

Веб-приложение на FastAPI,
которое предоставляет API для работы с коллекцией мемов.
Приложение состоит из двух FastAPI сервисов:
сервис с публичным API с бизнес-логикой
и сервис для работы с медиа-файлами.
Так же используются сервис с бд PostgreSQL и S3 хранилищем MinIO.
Дополнительно был реализован сервис для автоматического применения миграций.

## Инструкция по запуску
[Установить docker](https://docs.docker.com/engine/install/)

Клонировать репозиторий
```bash
git clone https://github.com/normalisht/madsoft_test.git
```

Создать .env файлы на основе .env.example в следующих директориях:
- infra
- private_api
- public_api

Перейти в директорию с конфигурацией проекта
```bash
cd infra
```

Запустить проект
```bash
docker compose up --build -d
```

Вариант для разработки (инфраструктура без fastapi сервисов)
```bash
docker compose -f dev-docker-compose.yml up --build -d
```

## Функционал

* Получить список всех мемов
```http request
GET /memes?page=1&size=1
```
```json
{
    "total": 2,
    "page": 1,
    "size": 1,
    "results": [
        {
            "filename": "filename.jpg",
            "image_url": "http://127.0.0.1:9000/memes/filename.jpg",
            "description": "desc",
            "expires_at": "2024-06-29T16:49:17.533461",
            "id": "8d75b10b-47f5-127f-84d3-fa4a72068c67"
        }
    ]
}
```

* Получить конкретный мем по ID
```http request
GET /memes/{id}
```
```json
{
  "filename": "filename.jpg",
  "image_url": "http://127.0.0.1:9000/memes/filename.jpg",
  "description": "desc",
  "expires_at": "2024-06-29T16:49:17.533461",
  "id": "{id}"
}
```

* Добавить новый мем (с картинкой и текстом).
```http request
POST /memes
```
form-data
```json
{
  "image": "some_file.jpg(binary)",
  "description": "desc"
}
```

```json
{
  "filename": "filename.jpg",
  "image_url": "http://127.0.0.1:9000/memes/filename.jpg",
  "description": "desc",
  "expires_at": "2024-06-29T16:49:17.533461",
  "id": "8d75b10b-47f5-127f-84d3-fa4a72068c67"
}
```

* Обновить существующий мем
```http request
PUT /memes/{id}
```

* Удалить мем
```http request
DELETE /memes/{id}
```
