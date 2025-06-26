<div align="center">

# BookReview — интеллектуальная платформа для книголюбов 📚✨

[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

</div>

---

## 🔍 О проекте

BookReview — это современная веб-платформа для любителей литературы, сочетающая:
- Систему рецензирования книг
- Персонализированные рекомендации на основе ML

**Главная особенность**: интеллектуальный анализ отзывов с помощью NLP для точных рекомендаций, а не просто фильтрация по жанрам.

<div align="center">
  <img src="https://via.placeholder.com/800x400?text=BookCritic+Screenshot" alt="Интерфейс BookReview" width="70%">
</div>

---

## 🚀 Возможности

### 📝 Для читателей
- Публикация развернутых рецензий с оценками
- Персональная лента рекомендаций
- Поиск книг по темам, настроению, стилю
- Ведение виртуальной книжной полки

### 🤖 Интеллектуальные функции
- Анализ тональности отзывов (NLP)
- Рекомендации на основе Word2Vec и TF-IDF
- Выявление скрытых тематических паттернов
- Гибридная система рекомендаций (контент + коллаборативная)

### ⚙️ Технические особенности
- JWT-аутентификация с подтверждением email
- Адаптивный интерфейс на React

---

## 🛠 Технологический стек

**Backend**:
- Python 3.9+
- FastAPI (ASGI)
- SQLAlchemy 2.0 (ORM)
- PostgreSQL (DB)

**Frontend**:
- React 18
- Swiper
- Axios

**ML/NLP**:
- Gensim (Word2Vec)
- Scikit-learn (TF-IDF, SVD)

**Docker**
---

## 🏗️ Архитектура

```mermaid
graph TD
    A[Клиент] --> B[React SPA]
    B --> C[FastAPI]
    C --> D[(PostgreSQL)]
    C --> E[Redis]
    C --> F[ML Service]
    C --> G[SMTP]
