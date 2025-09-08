# 🤖 ML-прогноз инфаркта 🫀

[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)](https://t.me/heartcorbot)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-green?logo=fastapi)](https://makemlbehappy.ru/model-api/docs)
[![Docker](https://img.shields.io/badge/Docker-Container-blue?logo=docker)](https://www.docker.com/)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-yellow?logo=python)](https://www.python.org/)
[![Nginx](https://img.shields.io/badge/Nginx-Reverse%20Proxy-green?logo=nginx)](https://nginx.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Телеграм-бот для скрининга риска инфаркта миокарда с использованием машинного обучения. Пользователи проходят опрос о состоянии здоровья, а модель CatBoost предсказывает вероятность сердечного приступа.

**Готовый бот:** [@heartcorbot](https://t.me/heartcorbot) в Telegram.

**Готовый API:** [Протестировать в Postman](https://www.postman.com/aidievjabrail-1402364/workspace/github/request/47712792-7c843c1e-6840-4b8b-ba32-cc807dbdcbb8?action=share&source=copy-link&creator=47712792)

**Документация к API:** [Документация](https://makemlbehappy.ru/model-api/docs)

## 🚀 Возможности

* **🤖 Опросник в Telegram**: Интуитивный диалог с пользователем на основе библиотеки aiogram
* **🌐 Webhook-интеграция**: Стабильная и быстрая связь с ботом через HTTPS
* **🧠 ML-модель CatBoost**: Mодель, обученная на датасете BRFSS
* **🚀 REST API на FastAPI**: Высокопроизводительное API для предсказаний с автоматической документацией
* **💾 База данных SQLite3**: Логирование анонимизированных результатов опросов
* **🐳 Docker-контейнеризация**: Полная изоляция сервисов и простое развертывание
* **🔒 Nginx с HTTPS**: Обеспечение безопасного шифрования трафика
* **📊 Мониторинг логов**: Все события приложения логируются для отладки
* **📝 Автодокументация API**: Документация доступна по пути `/docs`

## 📊 Модель машинного обучения

* **Алгоритм**: CatBoostClassifier
* **Датасет**: [BRFSS (Behavioral Risk Factor Surveillance System)](https://www.kaggle.com/datasets/cdc/behavioral-risk-factor-surveillance-system) на Kaggle
* **Основные метрики**:
  * **Accuracy**: `0.80`
  * **ROC-AUC**: `0.80`
  * **Precision (мажорный класс)**: `0.99`
  * **Recall (мажорный класс)**: `0.80`
  * **Precision (минорный класс)**: `0.21`
  * **Recall (минорный класс)**: `0.81`

* **Ключевые признаки**: Возраст, пол, сердечные заболевания, общее состояние здоровья, артериальное давление, курение, уровень холестерина, диабет, рост, вес и др.

* **Jupyter Notebook**: [Анализ и обучение модели](https://www.kaggle.com/code/jabr1one/ml-rus)

## 📁 Структура проекта

```text
.
├── ModelApi
│   ├── catboost.cbm
│   ├── init_db.py
│   ├── logger.db
│   └── model_api.py
├── Nginx
│   ├── ssl
│   │   └── .gitkeep
│   ├── templates
│   │   └── app.conf.template
│   ├── Dockerfile
│   └── nginx.conf
├── TelegramBot
│   └── telegram_bot.py
├── docker-compose.yml
├── Dockerfile
├── .dockerignore
├── .gitignore
├── README.md
└── requirements.txt
```

## ⚡ Быстрый старт (Развертывание)

### 1. Клонирование репозитория

```bash
git clone https://github.com/AidievJabrail/InfarctPrediction.git
cd InfarctPrediction
```

### 2. Установка Docker и Docker Compose

Установите docker и docker compose.

```bash
sudo apt install docker.io
sudo apt install docker-compose-v2
```

Проверьте установлен ли docker

```bash
docker --version
docker compose --version
```

### 3. Заполнение `.env` файла

Введите ваши данные env.example, далее:

```bash
cp .env.example .env
```

Или создайте и заполните:

```bash
nano .env
```

### 3. Получение SSL сертификатов

Получите SSL сертификаты (например, от Let's Encrypt с помощью Certbot) и добавьте в папку Nginx/ssl.

#### Пример для Certbot

Установите certbot

```bash
sudo snap install letsencrypt
```

Запустите

```bash
sudo certbot certonly --standalone
```

Скопируйте ваши сертификаты в папку Nginx/ssl как fullchain.pem и privkey.pem

```bash
cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ./Nginx/ssl/fullchain.pem
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ./Nginx/ssl/privkey.pem
```

### 4. Запуск приложений

Запустите все сервисы (FastAPI, Bot, Nginx) с помощью Docker Compose:

```bash
docker-compose up -d
```

Для остановки:

```bash
docker-compose down
```

### 5. Проверка работы FastApi

<https://yourdomain.ru/model-api/predict> - путь для предсказания модели. Отправляется POST запрос с json файлом в теле. Ответ приходит в поле predict.

```text
1 - Высокий риск инфаркта
2 - Низкий риск инфаркта
```

<https://yourdomain.ru/model-api/docs> - автоматическая документация API.

### 6. Проверка работы Телеграм-бота

```text
Найдите вашего бота в Telegram.
Начните диалог командой /start.
Для начало опроса /survey.
Для отмены опроса /cancel.
```

### 🛠 Технологический стек

* **Backend**: Python 3.10, FastAPI, Uvicorn
* **Machine Learning**: CatBoost, Scikit-learn, Pandas, NumPy
* **Telegram Bot**: Aiogram, Asyncio
* **Database**: SQLite3
* **Web Server**: Nginx
* **Containerization**: Docker, Docker Compose
* **Security**: SSL, HTTPS

### ⚠️ Важное примечание

Этот проект создан в учебных и демонстрационных целях. Прогнозы модели не являются медицинским диагнозом и не должны использоваться для принятия реальных медицинских решений. Всегда консультируйтесь с квалифицированными врачами по вопросам здоровья.

### 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл LICENSE для подробностей.

### 📞 Контакты

**Джабраил Айдиев**: <dzabrail.aidiev@mail.ru>

**Ссылка на проект**: <https://github.com/AidievJabrail/InfarctPrediction>