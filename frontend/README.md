# Frontend - AI Detection System

A modern React + TypeScript + Vite frontend for the AI Detection backend service.

## 🚀 Quick Start

### Install Dependencies

```bash
cd frontend
npm install
```

### Development Server

```bash
npm run dev
```

The app will run on `http://localhost:3000` and proxy API requests to `http://localhost:8000`.

### Build for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## 📋 Features

- ✨ Real-time AI object detection interface
- 🎨 Professional, responsive UI with a clean card layout
- 🖼️ View original and processed images side-by-side
- 🗂️ Persisted gallery of processed images (stored in browser localStorage)
- 📊 Display SKU summary and detected coordinates in a table
- 🔄 Form-based configuration for detection parameters
- ⚡ Built with React 19, TypeScript, and Vite
- 🚀 Hot Module Replacement (HMR) for instant updates

## 🛠️ Technologies

- **React 19** - UI Framework
- **TypeScript** - Type safety
- **Vite** - Build tool & dev server
- **CSS 3** - Modern styling

## 📁 Project Structure

```
src/
├── components/
│   ├── DetectionForm.tsx      # Form for detection input
│   └── ResultsDisplay.tsx     # Results visualization
├── App.tsx                    # Main app component
├── App.css                    # App styles
├── main.tsx                   # Entry point
└── index.css                  # Global styles
```

## 🔌 API Integration

The frontend communicates with the backend API at `http://localhost:8000`:

### Detection Endpoint

**POST** `/detect/`

**Parameters:**

- `modelname` - YOLO model to use (nestle_chiller, nestle_coffee, etc.)
- `project` - Project name
- `imageKey` - Image identifier
- `imageUrl` - URL to the image
- `categoryName` - Category name
- `routeId` - Route ID
- `visitDate` - Visit date (optional)

**Response:**

```json
{
  "success": true,
  "data": {
    "detection_count": 5,
    "detections": [
      {
        "class": "product",
        "confidence": 0.95,
        "x": 100,
        "y": 150
      }
    ],
    "filename": "image_001.jpg"
  }
}
```

## 🔐 Environment Variables

Create a `.env` file (if needed):

```env
VITE_API_URL=http://localhost:8000
```

## 🐳 Docker Support

```bash
# Build Docker image
docker build -t ai-detection-frontend .

# Run container
docker run -p 3000:80 ai-detection-frontend
```

## 📦 Dependencies

- react: ^19.0.0
- react-dom: ^19.0.0
- axios: ^1.7.7 (for HTTP requests)

## 🎯 Development Tips

- Use `npm run dev` for development with HMR
- TypeScript errors will show in the browser console
- CSS modules can be added if needed
- Component-based architecture for easy scaling

## 📝 License

MIT
{
files: ['**/*.{ts,tsx}'],
extends: [
// Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },

},
])

````

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
````
