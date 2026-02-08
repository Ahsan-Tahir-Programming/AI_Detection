# AI Detection System 🤖

A full-stack real-time object detection system using YOLO models with React frontend and FastAPI backend.

**Live Demo:** Coming soon (deploy on Vercel + Render)

---

## Features ✨

- **Real-time YOLO Detection**: Process images and get instant bounding box predictions
- **Multi-Model Support**: Support for multiple YOLO models (Zyn, Nestle products, etc.)
- **Modern UI**: React 18 with TypeScript, light/dark theme toggle
- **Type-Safe API**: FastAPI with Pydantic models and auto-generated OpenAPI docs
- **Gallery Management**: View, download, and delete detection results
- **Pagination**: Server-backed gallery with configurable page sizes
- **Responsive Design**: Works on desktop and mobile devices

---

## Tech Stack 🛠️

### Frontend

- **React 18** + **TypeScript**
- **Vite** (fast build tool)
- **CSS3** with CSS variables for theming
- **Fetch API** for backend communication

### Backend

- **FastAPI** (modern Python web framework)
- **Pydantic** (data validation and serialization)
- **SQLite** (database)
- **Ultralytics YOLO** (object detection)
- **SQLAlchemy** (ORM)

### DevOps

- **Docker** & **Docker Compose** for containerization
- **GitHub** for version control
- **Vercel** for frontend hosting (free)
- **Render** for backend hosting (free)

---

## Quick Start 🚀

### Prerequisites

- Node.js 16+ and npm
- Python 3.11+
- Git

### Local Development

#### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Ai_Detection.git
cd Ai_Detection
```

#### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn app.main:app --reload
```

Backend runs on: `http://localhost:8000`
API docs: `http://localhost:8000/docs`

#### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

Frontend runs on: `http://localhost:5173`

#### 4. Use Application

- Open `http://localhost:5173` in browser
- Enter test data in the form
- Click "Run Detection"
- View results in gallery

---

## Project Structure 📁

```
Ai_Detection/
├── app/                          # Backend (FastAPI)
│   ├── main.py                  # App entry point
│   ├── api/
│   │   └── routes.py            # API endpoints
│   ├── services/
│   │   ├── inference.py         # YOLO detection logic
│   │   ├── db.py                # Database operations
│   │   └── service2.py
│   ├── core/
│   │   ├── config.py            # Configuration & class mappings
│   │   └── logger.py            # Logging setup
│   ├── database/
│   │   └── detections.db        # SQLite database
│   ├── models/
│   │   ├── nestle_chiller.pt
│   │   ├── nestle_coffee.pt
│   │   ├── zyn.pt
│   │   └── ...                  # YOLO model files
│   ├── assets/
│   │   ├── ARIALBD.TTF          # Font for bounding boxes
│   │   └── classes.txt          # Class name mappings
│   └── download/                # Processed images (output)
│
├── frontend/                    # Frontend (React + Vite)
│   ├── src/
│   │   ├── App.tsx             # Main component
│   │   ├── App.css             # Global styles
│   │   ├── main.tsx            # Entry point
│   │   └── components/
│   │       ├── DetectionForm.tsx    # Input form
│   │       ├── ResultsDisplay.tsx   # Results view
│   │       ├── Gallery.tsx          # Saved detections
│   │       └── ErrorBoundary.tsx    # Error handling
│   ├── vite.config.ts          # Vite configuration
│   ├── package.json            # Dependencies
│   └── dist/                   # Production build
│
├── docker-compose.yml          # Docker services
├── Dockerfile                  # Backend container
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
├── DEPLOYMENT_GUIDE.md        # Deployment instructions
├── PYDANTIC_INTEGRATION.md    # API schema docs
└── CLASS_CONFIGURATION.md     # Class management docs
```

---

## API Documentation 📚

### Endpoints

#### `POST /detect/`

Process image and run detection

**Request:**

```json
{
  "modelname": "zyn",
  "project": "ai",
  "routeId": "route_001",
  "imageKey": "img_123",
  "imageUrl": "https://example.com/image.jpg",
  "categoryName": "product",
  "visitDate": "2026-02-08"
}
```

**Response:**

```json
{
  "requestId": "abc-123",
  "project": "ai",
  "routeId": "route_001",
  "imageSize": [1920, 1080],
  "originalImageUrl": "https://...",
  "processedImageUrl": "http://localhost:8000/download/...",
  "detectedSKU": {...},
  "detections": [...]
}
```

#### `GET /detections/`

Get paginated detection results

**Query Parameters:**

- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 12)

#### `DELETE /detections/{request_id}`

Delete a detection record

#### `GET /download-image/{filename}`

Download processed image

#### `GET /health`

Health check endpoint

**Full API docs:** Visit `/docs` endpoint after starting backend

---

## Configuration 🔧

### Class Names

Edit `app/assets/classes.txt` to add/modify detection classes:

```
YOLO_CLASS_NAME|MAPPED_CLASS_NAME|R|G|B
Backlit Not Functional|backlit_not_functional|255|0|0
```

### Environment Variables

See `.env.example` and create `.env` file:

```bash
DEBUG=False
DOCKER_ENV=False
```

---

## Docker Deployment 🐳

### Build & Run Locally

```bash
docker-compose up --build
```

### Environment

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

---

## Production Deployment 🌐

### 📘 See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for:

- ✅ Step-by-step deployment on Vercel + Render (FREE)
- ✅ Database setup for production
- ✅ Image storage solutions
- ✅ Environment configuration
- ✅ Troubleshooting guide

**Recommended:** Vercel (Frontend) + Render (Backend) = **$0/month** 🎉

---

## Development Notes 📝

### Adding New Models

1. Place `.pt` file in `app/models/`
2. Add class mapping to `app/assets/classes.txt`
3. Restart backend

### Database

- SQLite database at `app/database/detections.db`
- To reset: Delete `.db` file, backend auto-creates new one

### Frontend Theming

- Light/dark theme stored in localStorage
- CSS variables in `App.css` control colors
- Toggle button in header

### API Testing

Visit `http://localhost:8000/docs` for interactive Swagger UI

---

## Troubleshooting 🔧

### Backend won't start

```bash
# Verify Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend build fails

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Images aren't loading

- Check `VITE_API_URL` environment variable
- Verify backend CORS settings
- Check browser console for errors

### Database issues

- Delete `app/database/detections.db`
- Restart backend to auto-create new database

---

## Contributing 🤝

1. Fork repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push: `git push origin feature/your-feature`
5. Open Pull Request

---

## Performance Optimization 💨

- **Frontend**: Vite for fast builds (~2-3s)
- **Backend**: Threadpool for CPU-intensive YOLO inference
- **Images**: Lazy-loaded gallery for smooth scrolling
- **API**: Pydantic response models for efficient serialization

---

## Security Notes 🔒

- ✅ CORS configured for specific origins
- ✅ Input validation via Pydantic
- ✅ File path validation for downloads
- ✅ No hardcoded credentials
- ⚠️ Remember to:
  - Set `DEBUG=False` in production
  - Use HTTPS in production
  - Configure proper CORS origins
  - Validate all user inputs

---

## License 📄

MIT License - Feel free to use this project

---

## Support & Feedback 💬

- 📧 Email: your.email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/YOUR_USERNAME/Ai_Detection/issues)
- 💡 Discussions: [GitHub Discussions](https://github.com/YOUR_USERNAME/Ai_Detection/discussions)

---

## Roadmap 🗺️

- [ ] Multi-file batch processing
- [ ] User authentication
- [ ] Advanced filtering in gallery
- [ ] Export results (CSV/PDF)
- [ ] Real-time WebSocket updates
- [ ] Model training interface
- [ ] Mobile app version

---

## Author 👨‍💻

Created by: **Ahsan**

---

## Changelog 📋

### v1.0.0 (Feb 8, 2026)

- ✅ Initial release
- ✅ Pydantic models integration
- ✅ Dark theme support
- ✅ Image download functionality
- ✅ Pagination system
- ✅ Class configuration externalization

---

**Happy Detecting! 🎯**
