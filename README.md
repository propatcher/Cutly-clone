# Cutly Clone - A Simple Link Shortener

A clean and functional URL shortener service built with **FastAPI**. This pet project demonstrates core backend development skills using a modern Python stack.

## ✨ Features

- **Shorten URLs**: Create short, easy-to-share links from long URLs
- **Basic Click Analytics**: Track total clicks and view click history over time for each link
- **User Accounts**: Sign up to create and manage your own links
- **RESTful API**: All features are available through a simple API
- **Automatic Docs**: Interactive API documentation (Swagger UI) provided by FastAPI

## 🛠️ Tech Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **Task Queue**: Celery
- **Message Broker & Cache**: Redis
- **Containerization**: Docker & Docker Compose

## 🚀 How It Works (Simplified)

1. You submit a long URL
2. The FastAPI app saves it to PostgreSQL and gives you a short code
3. When someone clicks your short link:
   - FastAPI finds the original URL and redirects them instantly
   - It creates a background task to log the click
   - A Celery worker (using Redis) processes this task in the background
4. You can see the total clicks and a simple chart on your dashboard
