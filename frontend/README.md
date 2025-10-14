# Excel Data Analyzer - React Frontend

A modern React frontend for the AI-powered Excel data analyzer.

## Features

- 📊 **Excel File Upload** - Drag & drop or click to select files
- 🔍 **Parse Excel** - Convert Excel files to structured JSON
- 🤖 **AI Analysis** - Get AI-powered insights and recommendations
- 📈 **Real-time Health Check** - Monitor system status
- 📱 **Responsive Design** - Works on desktop and mobile
- 🎨 **Modern UI** - Clean, professional interface

## Setup

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn
- Backend server running on http://localhost:8000

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Environment Variables

Create a `.env` file in the frontend directory (optional):
```
REACT_APP_API_URL=http://localhost:8000
```

## Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm eject` - Eject from Create React App

## API Endpoints

The frontend connects to these backend endpoints:
- `GET /health` - System health check
- `POST /upload` - Parse Excel file
- `POST /analyze` - AI analysis of Excel file

## Usage

1. **Upload File**: Select an Excel file (.xlsx or .xls)
2. **Parse Excel**: Convert the file to JSON format
3. **AI Analysis**: Get comprehensive AI insights
4. **View Results**: See formatted JSON results
5. **Clear**: Reset the interface

## Technologies Used

- React 18
- Axios for API calls
- CSS3 for styling
- Create React App for tooling
