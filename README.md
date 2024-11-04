# Тестовое задание для компании "Аболъ"

### Установка

Установка проекта обёрнутого в докер

```bash
git clone git@github.com:Leraner/test_task_abol.git
```

### Запуск базы и брокера

```bash
docker-compose up --build
```

### Применяем миграции
```bash
cd auth
make migrate
```


### Запуск микросервисов

```bash
cd gateway
python3 main.py
cd ..
cd image_processor
python3 main.py
cd ..
cd auth
python3 main.py
```

### Запуск тестов
```bash
cd image_processor
pytest tests/images_tests.py
```