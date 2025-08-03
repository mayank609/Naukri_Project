# Social Media Analytics & Content Ideation Platform

A comprehensive MVP for social media post performance analytics and AI-powered content ideation.

## Features

### 1. Social Media Analytics Dashboard
- **Performance Insights**: Day-wise and week-on-week performance tracking
- **Competitive Analysis**: Compare your performance with competitors
- **Top/Bottom Analysis**: Identify what worked and what didn't (top 5, bottom 5)
- **Data Export**: Download raw data as CSV
- **Visual Analytics**: Interactive charts and graphs

### 2. AI Content Ideation
- **Image Suggestions**: AI-generated image ideas tailored to your brand
- **Caption Generation**: Engaging captions optimized for engagement
- **Video Concepts**: Creative video ideas and strategies
- **Brand Customization**: All outputs tailored to your brand guidelines

## Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework
- **SQLAlchemy**: Database ORM
- **OpenAI API**: AI content generation
- **StarAPI**: Instagram data integration
- **Pandas**: Data manipulation and analysis

### Frontend
- **React**: Modern UI framework
- **Chart.js**: Interactive charts
- **Tailwind CSS**: Styling
- **Axios**: HTTP client

## Setup Instructions

1. **Clone the repository**
```bash
git clone <repository-url>
cd Analytics-Naukri
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. **Install frontend dependencies**
```bash
cd frontend
npm install
```

5. **Run the application**
```bash
# Backend
uvicorn main:app --reload

# Frontend (in another terminal)
cd frontend
npm start
```

## API Keys Required

- **OpenAI API Key**: For AI content generation
- **StarAPI Key**: For Instagram data (RapidAPI)

## Environment Variables

Create a `.env` file with:
```
OPENAI_API_KEY=your_openai_key
STARAPI_KEY=your_starapi_key
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## API Endpoints

### Analytics
- `GET /api/analytics/performance` - Get performance data
- `GET /api/analytics/competitor` - Get competitor data
- `GET /api/analytics/export` - Export data as CSV

### Content Ideation
- `POST /api/content/generate` - Generate content ideas
- `POST /api/content/optimize` - Optimize existing content

## License

MIT License 