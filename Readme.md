# Project Documentation: Medida Challenge API

## Table of Contents

1. [Introduction](#introduction)
2. [Project Overview](#project-overview)
3. [Architecture Design](#architecture-design)
   - [Component Overview](#component-overview)
   - [API Endpoints](#api-endpoints)
   - [Data Flow](#data-flow)
   - [Authentication](#authentication)
   - [Error Handling](#error-handling)
4. [Development Workflow](#development-workflow)
   - [Requirements Gathering](#requirements-gathering)
   - [API Specification](#api-specification)
   - [Model Definition](#model-definition)
   - [Main Application Logic](#main-application-logic)
   - [Unit Testing](#testing)
   - [Integration Testing](#integration-testing)
   - [Dockerization](#dockerization)
5. [Running Method](#running-method)
6. [Conclusion](#conclusion)

## Introduction <a name="introduction"></a>

```
This document outlines the architecture, design, and development workflow for the implementation of the Medida Challenge API. The purpose of this API is to provide a RESTful interface for retrieving NFL events data from a remote API and exposing it in a standardized JSON format. The project includes designing and implementing the API, as well as unit and integration testing, and Docker containerization.
```

## Project Overview <a name="project-overview"></a>

### Objective:

The objective of the project is to develop a RESTful API that retrieves NFL events data from a remote API, formats it according to specifications, and exposes it through designated endpoints.

### Key Features:

- Integration with a remote API to fetch live NFL events data.
- Exposing standardized JSON endpoints for retrieving events data.
- Authentication mechanism for accessing API endpoints.
- Error handling for providing meaningful error responses.

## Architecture Design <a name="architecture-design"></a>

### Component Overview <a name="component-overview"></a>

The architecture consists of the following components:

- **FastAPI Application:** The core application built using FastAPI, responsible for handling incoming requests and serving responses.
- **OAuth2 Authentication:** Implements OAuth2 password bearer scheme for user authentication.
- **HTTP Client:** Asynchronous HTTP client for fetching data from the remote API.
- **Mock Remote API:** A mock implementation of the remote API for testing purposes.
- **Unit and Integration Tests:** Ensure the correctness and reliability of the application.

### API Endpoints <a name="api-endpoints"></a>

- `POST /token`: Endpoint for user authentication and token generation.
- `POST /events`: Endpoint for retrieving NFL events data between specified dates.

### Data Flow <a name="data-flow"></a>

1. User sends a request to authenticate and obtain an access token.
2. Authenticated user sends a request to retrieve NFL events data within a specified date range.
3. FastAPI application fetches data from the remote API using an HTTP client.
4. Data is formatted according to specifications and returned to the user.

### Authentication <a name="authentication"></a>

- OAuth2 password bearer scheme is used for user authentication.
- Users must provide a valid username and password to obtain an access token.
- Access token is included in the Authorization header for subsequent requests.

### Error Handling <a name="error-handling"></a>

- Custom error responses are provided for various scenarios, including authentication failure, bad requests, and internal server errors.
- Errors are returned with appropriate HTTP status codes and error messages.

## Development Workflow <a name="development-workflow"></a>

### Requirements Gathering <a name="requirements-gathering"></a>

- Understand the project requirements and objectives.
- Identify key features and endpoints to be implemented.
- Determine the data format and structure for requests and responses.

### API Specification <a name="api-specification"></a>

- Design the API specification using OpenAPI.
- Define endpoints, request and response schemas, and security requirements.
- Specify data validation rules and error responses.

### Model Definition <a name="model-definition"></a>

- Define Pydantic models to represent request and response data structures.
- Include validation logic for ensuring data integrity.

### Main Application Logic <a name="main-application-logic"></a>

- Implement the core application logic using FastAPI.
- Handle incoming requests, authenticate users, and fetch data from the remote API.
- Format data according to specifications and return responses.

### Testing <a name="testing"></a>

- Write unit tests to validate the functionality of individual components.
- Test model validation, authentication, and data retrieval logic.
- Ensure edge cases and error scenarios are handled correctly.

### Dockerization <a name="dockerization"></a>

- Dockerize the application for easy deployment and scalability.
- Use Docker Compose to orchestrate multiple containers, including the main application and mock remote API.
- Ensure proper configuration of volumes, ports, and dependencies.

## Running Method <a name="running-method"></a>

### Environment Setup

#### 1. Install Docker Engine

> `sudo apt-get update`

> `sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin`

#### 2. Install Docker Compose V2

> `mkdir -p ~/.docker/cli-plugins/`

> `curl -SL https://github.com/docker/compose/releases/download/v2.3.3/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose`

### Building and executing Docker Container

> `sudo docker compose build`

> `sudo docker compose up -d`

After that, the mock remote API is deployed on http://localhost:9000, as well as API endpoints on http://localhost:8000.

You can use `pytest` to check out all the units are working well.

And also you can checkout APIs navigating to http://localhost:8000/docs for SwaggerUI or use API simulation tool such as Postman and Microcks.

## Conclusion <a name="conclusion"></a>

The Medida Challenge API provides a robust solution for retrieving NFL events data and exposing it through standardized endpoints. By following a structured development workflow and adhering to best practices in architecture design, the project ensures scalability, reliability, and maintainability. The use of FastAPI, OAuth2 authentication, and Dockerization contributes to the efficiency and effectiveness of the solution. Overall, the project demonstrates proficiency in API development and engineering practices.
