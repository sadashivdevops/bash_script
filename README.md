# Git Branch Manager

A modern web interface for managing multiple git release branches, built with React, Vite, and Tailwind CSS.

## Features

- **Interactive Web UI**: Clean, responsive interface built with React and Tailwind CSS
- **Branch Management**: Visual representation of release branches
- **Execution Simulation**: Interactive demonstration of the git script functionality
- **Dockerized**: Fully containerized application for easy deployment

## Screenshots

### Initial Interface
![Initial Interface](https://github.com/user-attachments/assets/dbdd9630-a2f0-45d2-bbdf-9342921a70e0)

### Script Execution
![Script Execution](https://github.com/user-attachments/assets/1d96fc0f-9cbd-4e0d-bc7f-99ac122be49c)

## Project Structure

```
├── frontend/                 # React application
│   ├── src/                 # Source code
│   ├── package.json         # Dependencies
│   └── vite.config.js       # Vite configuration
├── new_git_script.sh        # Original bash script
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
├── nginx.conf               # Nginx configuration
└── README.md                # This file
```

## Quick Start

### Using Docker (Recommended)

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   Open your browser and go to `http://localhost:3000`

### Development Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

3. **Access the application:**
   Open your browser and go to `http://localhost:5173`

### Production Build

1. **Build the application:**
   ```bash
   cd frontend
   npm run build
   ```

2. **Serve the built files:**
   The built files will be in the `frontend/dist` directory

## Original Bash Script

The original `new_git_script.sh` performs the following operations:

- Loops through release branches: `release-1.0`, `release-2.0`, `release-3.0`, `release-4.0`, `release-5.0`
- Checks out each branch
- Creates a file named after the branch (e.g., `release-1.0.txt`)
- Stages and commits the file
- Pushes changes to the remote origin

## Web Interface Functionality

The React web interface provides:

- **Visual Branch List**: Shows all release branches with their status
- **Interactive Execution**: Click "Execute Git Script" to simulate the bash script
- **Real-time Logs**: Watch the execution progress in a terminal-like interface
- **Responsive Design**: Works on desktop and mobile devices

## Docker Configuration

### Dockerfile
- Multi-stage build using Node.js and Nginx
- Optimized for production with static file serving
- Lightweight Alpine Linux base images

### Docker Compose
- Simple single-service setup
- Configurable port mapping
- Ready for extension with backend services

## Technologies Used

- **Frontend**: React 18, Vite, Tailwind CSS
- **Build Tool**: Vite for fast development and optimized builds
- **Styling**: Tailwind CSS for utility-first styling
- **Containerization**: Docker with Nginx for production serving
- **Web Server**: Nginx with optimized configuration

## Development

To contribute or modify the application:

1. **Clone the repository**
2. **Install dependencies**: `cd frontend && npm install`
3. **Start development server**: `npm run dev`
4. **Make your changes**
5. **Test the build**: `npm run build`
6. **Test with Docker**: `docker-compose up --build`

## License

This project is open source and available under the [MIT License](LICENSE).