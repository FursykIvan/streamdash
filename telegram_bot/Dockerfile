FROM python:3.11-slim

WORKDIR /app

# Копіюємо requirements тільки для telegram_bot
COPY telegram_bot/requirements.txt ./

# Встановлюємо лише ці залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо код бота та producer, якщо потрібно
COPY telegram_bot/ ./
COPY producer/ ./producer/

# Встановлюємо змінну середовища PYTHONPATH, щоб імпорти працювали
ENV PYTHONPATH=/app

CMD ["python", "-u", "bot.py"]