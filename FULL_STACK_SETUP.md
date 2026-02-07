# Full Stack AI Detection System

Complete setup for both backend (FastAPI + Python) and frontend (React + TypeScript).

## 📊 Project Architecture

```
├── app/                          # Backend (FastAPI)
│   ├── main.py                  # App entry point
│   ├── api/routes.py            # API endpoints
│   ├── core/config.py           # Configuration
│   ├── services/inference.py    # YOLO inference
│   └── models/                  # Pre-trained models
│
├── frontend/                     # Frontend (React + TypeScript)
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── App.tsx              # Main component
│   │   └── main.tsx             # Entry point
│   └── package.json
│
├── Dockerfile                    # Backend Docker
├── docker-compose.yml           # Full stack orchestration
└── requirements.txt             # Python dependencies
```

## 🚀 Quick Start (Local Development)

### Prerequisites

- Python 3.9+
- Node.js 18+ & npm
- Docker & Docker Compose (optional)

### Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run the backend
uvicorn app.main:app --reload --port 8000
```

Backend will be available at: `http://localhost:8000`

### Frontend Setup

```bash
# Install dependencies
cd frontend
npm install

# Run development server
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## 🐳 Docker Compose (Full Stack)

```bash
# Start both services
docker-compose up --build

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

## 📋 API Endpoints

### Detection

- **POST** `/detect/` - Run detection on an image
  - Parameters: modelname, project, imageKey, imageUrl, categoryName, routeId, visitDate
  - Response: detection results with bounding boxes and confidence scores

### Health Check

- **GET** `/` - Health check endpoint

## 🎨 Frontend Features

- **Model Selection**: Choose from available YOLO models
- **Image Input**: Provide image URL for detection
- **Form Configuration**: Set project, route, category details
- **Results Display**: View detected objects with confidence scores
- **Responsive Design**: Mobile-friendly interface

## 🛠️ Technologies

### Backend

- FastAPI 0.115.6
- PyTorch 2.2.2
- YOLOv8 (Ultralytics)
- OpenCV 4.10.0
- Uvicorn server

### Frontend

- React 19.0.0
- TypeScript 5.5.3
- Vite 5.4.2
- Axios 1.7.7

## 📦 Installation Details

### Backend Dependencies

```
fastapi==0.115.6
uvicorn==0.33.0
ultralytics==8.2.103
torch==2.2.2
torchvision==0.17.2
opencv-python==4.10.0.84
```

### Frontend Dependencies

```
react@^19.0.0
react-dom@^19.0.0
typescript@^5.5.3
vite@^5.4.2
axios@^1.7.7
```

## 🔧 Configuration

### Backend Config

Edit `app/core/config.py`:

```python
DOWNLOAD_DIR = "download"
LOG_DIR = "logs"
DATABASE_DIR = "database"
```

### Frontend Config

Edit `frontend/vite.config.ts`:

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    }
  }
}
```

## 📊 Supported Models

- `nestle_chiller.pt` - Nestle Chiller detection
- `nestle_coffee.pt` - Nestle Coffee detection
- `nestle_dairy_liquid.pt` - Nestle Dairy Liquid detection
- `nestle_juices.pt` - Nestle Juices detection
- `zyn.pt` - Zyn product detection

## 🚀 Production Deployment

### Build Frontend

```bash
cd frontend
npm run build
```

### Docker Production Build

```bash
docker build -t ai-detection-backend:latest .
cd frontend && docker build -t ai-detection-frontend:latest .
```

### Kubernetes Deployment

Create deployment manifests in `k8s/` directory for scalable deployment.

## 📝 Environment Variables

### Backend

```env
DOWNLOAD_DIR=./download
LOG_DIR=./logs
DATABASE_DIR=./database
```

### Frontend

```env
VITE_API_URL=http://localhost:8000
VITE_API_TIMEOUT=30000
```

## 🐛 Troubleshooting

### Backend Issues

1. **Port 8000 already in use**: `lsof -i :8000` then kill process
2. **CUDA not available**: CPU mode will be used automatically
3. **Models not loading**: Check `app/models/` directory

### Frontend Issues

1. **CORS errors**: Ensure backend has CORS enabled
2. **API not connecting**: Check proxy in `vite.config.ts`
3. **Port 3000 in use**: `npm run dev -- --port 3001`

## 📚 Documentation

- [FastAPI Docs](http://localhost:8000/docs) - Swagger UI (when running)
- [React Docs](https://react.dev)
- [TypeScript Docs](https://www.typescriptlang.org/docs)

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/name`
2. Commit changes: `git commit -am 'Add feature'`
3. Push to branch: `git push origin feature/name`
4. Submit pull request

## 📄 License

MIT License - see LICENSE file for details

## 📞 Support

For issues and questions, please open an issue on the repository.
