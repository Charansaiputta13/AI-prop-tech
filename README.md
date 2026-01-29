# AI-First Property Management System (AI-PMS)

An intelligent, agentic platform for autonomous property management.

## 🚀 Overview

AI-PMS is a modern, full-stack application leveraging AI agents to automate the property lifecycle. From tenant onboarding and maintenance coordination to financial reporting, our agents handle the heavy lifting.

### Key Features
- **Intelligent Orchestration**: A central agent that routes requests to specialized sub-agents.
- **Maintenance Agent**: Automates maintenance request intake, priority assessment, and vendor assignment.
- **Finance Agent**: Handles rent tracking and invoice generation.
- **Modern UI**: A responsive, premium dashboard built with Next.js and Tailwind CSS.

---

## 🏗️ Architecture

The system follows a microservices-inspired architecture:

- **Frontend**: Next.js (App Router) + Tailwind CSS + Framer Motion.
- **Backend**: FastAPI + LangChain + SQLAlchemy.
- **AI Engine**: LangChain-powered agents (defaulting to GPT-3.5-Turbo).

---

## 🛠️ Getting Started

### Prerequisites
- [Docker & Docker Compose](https://docs.docker.com/get-docker/)
- OpenAI API Key (Optional, fallbacks to "Echo Mode" if missing)

### Running with Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ai-prop-tech
   ```

2. Start the services:
   ```bash
   docker compose up --build
   ```

3. Access the application:
    - **Frontend**: http://localhost:3000
    - **Backend API**: http://localhost:8000

---

## 📄 Development

### Manual Setup

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 🔒 License
Proprietary. All rights reserved.
