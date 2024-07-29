# massive_ingest

## Project Overview

`massive_ingest` is a project designed to demonstrate how to load massive amounts of data, including JSON files and images, into a database using a microservices architecture. The project leverages Docker Compose to orchestrate the services required for data ingestion.

## Architecture

The project consists of the following services:

- **backend**: A FastAPI backend that serves as the entry point for data ingestion.
- **mongodb**: A MongoDB database for storing JSON data.
- **postgres**: A PostgreSQL database for structured data storage.
- **rabbitmq**: A RabbitMQ message broker for handling task queues.
- **ingest_data_worker**: A worker service for ingesting JSON data.
- **ingest_image_worker**: A worker service for ingesting image data.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

### Clone the Repository

```sh
git clone https://github.com/puiggrosd/massive_ingest.git
cd massive_ingest
```
Build and Start the Services
```
docker-compose up --build
```
This command will build the necessary Docker images and start all the services defined in the docker-compose.yml file.
Accessing the Services

    Backend API: The FastAPI backend will be available at http://localhost:8000.
    MongoDB: Accessible at mongodb://localhost:27017.
    PostgreSQL: Accessible at postgresql://user:password@localhost:5432/mydatabase.
    RabbitMQ Management Console: Available at http://localhost:15672 (default credentials: guest / guest).

Environment Variables

The following environment variables are configured in the docker-compose.yml file:

    - MONGODB_URL: URL for connecting to MongoDB.
    - POSTGRES_HOST: Hostname for PostgreSQL.
    - POSTGRES_USER: PostgreSQL user.
    - POSTGRES_PASSWORD: PostgreSQL password.
    - POSTGRES_DB: PostgreSQL database name.
    - RABBITMQ_HOST: Hostname for RabbitMQ.
    - BACKEND: Service name for the backend.

## How works
JSON Data

The ingest_data_worker service is responsible for ingesting JSON data. To load JSON data, place your files in the appropriate directory and ensure the ingest_data_worker.py script is set up to process them.
Image Data

The ingest_image_worker service handles image data ingestion. Place your images in the ./image_data directory. The ingest_image_worker.py script will process these images.

## Usage
```
docker compose up --scale ingest_data_worker=8
docker exec -it massive_ingest-base-1 bash
and in the console of docker container bash test_siege.sh
you can also run test_siege.sh in your console

```
