# Travel-Django

A professional, production-ready travel itinerary planner for Tamil Nadu, built with high engineering standards.

## Technical Architecture
- **Backend:** Django with **PostgreSQL** for robust, relational data management.
- **Design Principles:** Developed with **SOLID** design principles and **GRASP** patterns to ensure modular, maintainable, and scalable code.
- **AI Engine:** Integrated with Phi3 via Ollama, featuring custom hybrid rule-based guardrails to prevent misuse and optimize token usage.

## Key Features
- **Weather Intelligence:** Real-time weather monitoring for key TN hubs (Chennai, Coimbatore, Madurai, Trichy, Tuticorin) using OpenMeteo API.
- **Interactive Mapping:** Built-in Leaflet.js maps for visualizing circuits relative to regional climate conditions.
- **Quality Assurance:** Comprehensive end-to-end (E2E) and unit testing suite to ensure high reliability.
- **Containerization:** Fully Dockerized for consistent development and deployment environments.

## Setup
1. Clone the repository: `git clone https://github.com/AdityaShankar1/Travel-Django.git`
2. Build the Docker image: `docker build -t travel-master .`
3. Run the container: `docker run -p 8000:8000 travel-master`

---
*Built with professional-grade engineering practices for scalable travel solutions.*
