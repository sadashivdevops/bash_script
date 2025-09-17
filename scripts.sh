#!/bin/bash

# Git Branch Manager - Development Helper Script

set -e

case "$1" in
    "dev")
        echo "🚀 Starting development server..."
        cd frontend && npm run dev
        ;;
    "build")
        echo "🔨 Building application..."
        cd frontend && npm run build
        echo "✅ Build completed! Files are in frontend/dist/"
        ;;
    "docker-build")
        echo "🐳 Building Docker image..."
        docker build -t git-branch-manager .
        echo "✅ Docker image built successfully!"
        ;;
    "docker-run")
        echo "🐳 Running Docker container..."
        docker run -d -p 3000:80 --name git-branch-manager git-branch-manager
        echo "✅ Container started! Access at http://localhost:3000"
        ;;
    "docker-stop")
        echo "🛑 Stopping Docker container..."
        docker stop git-branch-manager || true
        docker rm git-branch-manager || true
        echo "✅ Container stopped!"
        ;;
    "compose-up")
        echo "🐳 Starting with Docker Compose..."
        docker-compose up --build -d
        echo "✅ Application started! Access at http://localhost:3000"
        ;;
    "compose-down")
        echo "🛑 Stopping Docker Compose..."
        docker-compose down
        echo "✅ Application stopped!"
        ;;
    "install")
        echo "📦 Installing dependencies..."
        cd frontend && npm install
        echo "✅ Dependencies installed!"
        ;;
    *)
        echo "Git Branch Manager - Development Helper"
        echo "Usage: $0 {dev|build|docker-build|docker-run|docker-stop|compose-up|compose-down|install}"
        echo ""
        echo "Commands:"
        echo "  dev          - Start development server"
        echo "  build        - Build production application"
        echo "  docker-build - Build Docker image"
        echo "  docker-run   - Run Docker container"
        echo "  docker-stop  - Stop Docker container"
        echo "  compose-up   - Start with Docker Compose"
        echo "  compose-down - Stop Docker Compose"
        echo "  install      - Install dependencies"
        exit 1
        ;;
esac