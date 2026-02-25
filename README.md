# Travel-Django

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Django](https://img.shields.io/badge/django-6.0-092e20?logo=django&logoColor=white)
![Python](https://img.shields.io/badge/python-3.14-blue?logo=python&logoColor=white)
[![Pipeline Status](https://gitlab.com/adityashankar1-group/Travel-Django/badges/main/pipeline.svg)](https://gitlab.com/adityashankar1-group/Travel-Django/-/pipelines)


## TravelMaster using PostgreSQL + Django + Bootstrap CSS + Ollama (Phi 3.8)

A professional, production-ready travel itinerary planner for Tamil Nadu, built with high engineering standards.

## Technical Architecture
- **Backend:** Django with **PostgreSQL** for robust, relational data management.
- **Design Principles:** Developed with **SOLID** design principles and **GRASP** patterns to ensure modular, maintainable, and scalable code.
- **Frontend:** Responsive UI developed using **Bootstrap CSS**.

- **AI Engine:** Integrated with Phi3 via Ollama, featuring custom hybrid rule-based guardrails to prevent misuse and optimize token usage.

## Key Features
- **Weather Intelligence:** Real-time weather monitoring for key TN hubs (Chennai, Coimbatore, Madurai, Trichy, Tuticorin) using OpenMeteo API.
- **Interactive Mapping:** Built-in Leaflet.js maps for visualizing circuits relative to regional climate conditions.
- **Quality Assurance:** Comprehensive end-to-end (E2E) and unit testing suite to ensure high reliability.
- **Containerization:** Fully Dockerized for consistent development and deployment environments.

## Data Model (Schema)
The architecture follows a strict hierarchy:
- **Package:** The top-level travel offering.
- **Circuit:** A curated experience within a package, consisting of multiple **Places**.
- **Places:** Geographical destinations linked to circuits via a many-to-many relationship.
- **Hotel:** Multi-tier accommodation (Budget, Standard, Premium, Luxury) linked to specific travel plans.
- **Booking:** Manages user selection of circuits, transport types, and hotel tiers with enforced data integrity.

## Setup
1. Clone the repository: `git clone https://github.com/AdityaShankar1/Travel-Django.git`
2. Build the Docker image: `docker build -t travel-master .`
3. Run the container: `docker run -p 8000:8000 travel-master`

## Output Screenshots:

### Homepage with Ask AI:
<img width="1229" height="823" alt="image" src="https://github.com/user-attachments/assets/34549d56-bdb2-49e4-91db-a52464654f3c" />

## Weather Alerts :
<img width="1118" height="810" alt="image" src="https://github.com/user-attachments/assets/c480e45b-61ee-4f28-8d9c-32dd97f05702" />

## Bookings History Page:
<img width="828" height="353" alt="image" src="https://github.com/user-attachments/assets/1804fe30-4953-4605-b263-6fc5ee7af609" />

## Continuous Integration (CI):
### GitLab:
<img width="1005" height="491" alt="image" src="https://github.com/user-attachments/assets/01b39792-d058-417d-937e-8620f0394bad" />
I've utilized GitLab to develop a successful CI pipeline

---
*Built with professional-grade engineering practices with ❤️ for the travel industry *
