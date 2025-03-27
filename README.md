# Flask-Vue Application

A modern web application skeleton with Flask backend and Vue 3 frontend.

Generated by sonnect 3.7 and fixed something by myself

## Project Overview

This project provides a structured skeleton for building web applications with the following components:

1. **API Services for Backend Operations**: RESTful endpoints for core services
2. **API Services for Frontend Interfaces**: Dedicated endpoints optimized for frontend needs
3. **Batch Script System**: Automated background tasks with email alerting capabilities

## Technology Stack

- **Backend**: Python 3.13, Flask
- **Frontend**: Vue 3, Vite, Pinia, Vue Router
- **Database**: MySQL
- **Environment Management**: dotenv for environment-specific configurations

## Project Structure

```
flask_vue/
├── app/                        # Backend Flask application
│   ├── api/                    # API modules
│   │   ├── frontend/           # API endpoints for frontend
│   │   └── services/           # Core service API endpoints
│   ├── batch/                  # Batch processing scripts
│   ├── config/                 # Configuration files
│   ├── logs/                   # Application logs
│   ├── models/                 # Database models
│   ├── static/                 # Static files
│   └── templates/              # Flask templates (if needed)
├── frontend/                   # Vue.js frontend
│   ├── public/                 # Static public assets
│   └── src/                    # Vue source files
│       ├── assets/             # Frontend assets
│       ├── components/         # Vue components
│       ├── router/             # Vue Router configuration
│       ├── stores/             # Pinia stores
│       └── views/              # Page views
├── .env.example                # Example environment variables
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
└── run.py                      # Application entry point
```

## Setup Instructions

### Prerequisites

- Python 3.13+
- Node.js 16+
- MySQL

### Backend Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env file with your specific configuration
   ```

4. Create the database:
   ```bash
   mysql -u root -p
   > CREATE DATABASE flask_vue_dev;
   > exit
   ```

5. Initialize the database:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. Run the Flask application:
   ```bash
   python run.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

## Environment Configuration

The application supports three environments:

- **Development**: Local development settings
- **Staging**: Pre-production testing
- **Production**: Live production environment

Configuration is managed through environment variables defined in the `.env` file.

## Logging

The application implements a robust logging system:

- **Application Logs**: Main application logs
- **Batch Logs**: Separate logs for batch processes
- **Log Rotation**: Prevents logs from consuming too much disk space

## Batch Processing

The batch system includes:

- **Scheduler**: Runs tasks at specified intervals
- **Email Alerts**: Automated notifications
- **Logging**: Detailed job execution logs

To run batch jobs:

```bash
python -m app.batch.scheduler
```

## API Documentation

### Service API Endpoints

- `GET /api/services/health` - Health check endpoint
- `GET /api/services/example` - Example service endpoint

### Frontend API Endpoints

- `GET /api/frontend/user` - Get user information
- `GET /api/frontend/dashboard` - Get dashboard data

## License

[MIT](LICENSE) 


![image](https://github.com/user-attachments/assets/c0cd99ff-3ee6-4a6c-849e-c23a5a2c4400)
