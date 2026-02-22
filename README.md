# Travel-Django

A production-ready, AI-powered travel itinerary planner focused on Tamil Nadu tourism. 

## Features
- **Smart AI Assistant:** Integrated with Phi3 via Ollama, featuring custom hybrid rule-based guardrails to prevent misuse and optimize token usage.
- **Weather Intelligence:** Real-time weather monitoring for key TN hubs (Chennai, Coimbatore, Madurai, Trichy, Tuticorin) using OpenMeteo API.
- **Interactive Mapping:** Built-in Leaflet.js maps for visualizing circuits relative to regional climate conditions.
- **Production-Ready:** Containerized with Docker for seamless deployment.

## Tech Stack
- **Backend:** Django
- **AI Engine:** Ollama (Phi3)
- **External APIs:** OpenMeteo (Weather), Leaflet.js (Mapping)
- **Deployment:** Docker

## Setup
1. Clone the repository: `git clone https://github.com/AdityaShankar1/Travel-Django.git`
2. Build the Docker image: `docker build -t travel-master .`
3. Run the container: `docker run -p 8000:8000 travel-master`

---
*Built with professional-grade engineering practices for scalable travel solutions.*
