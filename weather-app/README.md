# Weather AI Application

A minimalist, glassmorphic weather application that uses an AI Agent to provide detailed weather reports and forecasts for any city. Built with **React** and **FastAPI**.

## Features

-   **Natural Language Queries**: Ask "How's the weather in Tokyo?" or "Will it rain in London?".
-   **AI-Powered Responses**: Uses LangChain + OpenRouter (Gemini/LLaMA) to generate human-like summaries.
-   **Rich Weather Data**: Real-time stats (Temp, Wind, Humidity) + 5-Day Forecast.
-   **Glassmorphism UI**: Premium, modern design with smooth animations.

## Tech Stack

-   **Frontend**: React, Vite, Vanilla CSS (Glassmorphism).
-   **Backend**: Python, FastAPI, LangChain.
-   **AI Provider**: OpenRouter (Google Gemini Flash / LLaMA, etc.).
-   **Weather Data**: Open-Meteo API (No key required).

## Prerequisites

-   **Node.js** (v16+)
-   **Python** (v3.9+)
-   **OpenRouter API Key** (Get one at [openrouter.ai](https://openrouter.ai/))

---

## Setup & and Installation

### 1. Backend Setup

1.  Navigate to the backend folder:
    ```bash
    cd backend
    ```
2.  Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Configure Environment Variables:
    -   Rename `env.example` to `.env` (or create a new `.env` file).
    -   Add your API key:
        ```ini
        OPENROUTER_API_KEY=sk-or-v1-your-key-here
        ```
4.  Run the Backend Server:
    ```bash
    python -m uvicorn main:app --reload
    ```
    *The server will start at `http://localhost:8000`*

### 2. Frontend Setup

1.  Open a new terminal and navigate to the frontend folder:
    ```bash
    cd frontend
    ```
2.  Install Node dependencies:
    ```bash
    npm install
    ```
3.  Run the Development Server:
    ```bash
    npm run dev
    ```
    *The app will start at `http://localhost:5173`*

---

## How to Run

Once both servers are running:
1.  Open your browser and go to [http://localhost:5173](http://localhost:5173).
2.  Enter a city name or a question (e.g., "Paris weather").
3.  Click **Send**.

## Troubleshooting

-   **429 Error (Rate Limit)**: If the AI returns a "Rate Limit" error, it means the free model on OpenRouter is busy. You can wait a minute or switch the model in `backend/agent.py`.
-   **Network Error**: Ensure the backend is running on port 8000.
