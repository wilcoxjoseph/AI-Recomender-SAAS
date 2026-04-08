# AI-Powered Recommender System SaaS

A production-ready full-stack application with AI-powered recommendations, user authentication, and persistent storage.

## Features

- 🤖 AI-powered recommendations using sentence transformers and FAISS
- 🔐 Google OAuth authentication via Supabase
- 💾 PostgreSQL database for user interactions
- 📱 Responsive React frontend with Next.js
- 🐳 Docker containerization for easy deployment

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Supabase account (free tier)

### Setup

1. Clone the repository
2. Create a Supabase project and enable Google Auth
3. Copy `.env.example` to `.env` in both backend and frontend
4. Run `docker-compose up --build`

### Environment Variables

Backend:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anon key
- `DATABASE_URL`: PostgreSQL connection string

Frontend:
- `NEXT_PUBLIC_SUPABASE_URL`: Your Supabase project URL
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`: Your Supabase anon key
- `NEXT_PUBLIC_API_URL`: Backend API URL

## API Endpoints

- `GET /api/recommendations` - Get personalized recommendations
- `POST /api/interactions` - Rate an item
- `GET /api/saved` - Get saved items
- `POST /api/saved/{item_id}` - Save an item

## Deployment

### Deploy to Render

1. Push code to GitHub
2. Create a new Web Service on Render
3. Connect your repository
4. Set environment variables
5. Deploy!

### Live Demo

[Add your deployed URL here]

## Tech Stack

- Backend: FastAPI, SQLAlchemy, Sentence Transformers, FAISS
- Frontend: Next.js, Tailwind CSS, Supabase Auth
- Database: PostgreSQL
- ML: Sentence-BERT embeddings, FAISS similarity search

## License

MIT
