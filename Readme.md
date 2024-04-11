## INTRODUCTION

> The Medida Challenge API is a RESTful API developed to provide dynamic NFL event data. It retrieves data from a remote API, formats it according to specified requirements, and returns it in JSON format.

## API DOCUMENTATION

### AUTHENTICATION

- `POST /token`
  - Endpoint for user login to obtain access token.
  - Requires username and password in the request body.
  - Returns an access token upon successful authentication.

### ENDPOINTS

- `POST /events`
  - **Summary**: Retrieves a list of NFL events.
  - **Description**: Returns a list of NFL events including event ID, date, time, home team details (ID, nickname, city, rank, and rank points), and away team details (ID, nickname, city, rank, and rank points).
  - **Parameters**:
    - `startDate` (string): Start date for filtering events (format: YYYY-MM-DD).
    - `endDate` (string): End date for filtering events (format: YYYY-MM-DD).
  - **Responses**:
    - `200 OK`: Successful response with a list of event objects.
    - `400 Bad Request`: Invalid request format.
    - `401 Unauthorized`: Unauthorized access, invalid credentials.
    - `500 Internal Server Error`: Server error occurred.

### DATA MODELS

- **EventsRequest**
  - Request model for /events endpoint.
  - **Attributes**:
    - `league` (string): The league (currently supports only "NFL").
    - `startDate` (string): Start date for filtering events.
    - `endDate` (string): End date for filtering events.
- **EventsResponse**
  - Response model for /events endpoint.
  - Array of Event objects.
- **Event**
  - Data model for an event.
  - **Attributes**:
    - `eventId` (string): Unique identifier for the event.
    - `eventDate` (string): Date of the event (format: YYYY-MM-DD).
    - `eventTime` (string): Time of the event (format: HH:MM:SS).
    - `homeTeamId` (string): Unique identifier for the home team.
    - `homeTeamNickName` (string): Nickname of the home team.
    - `homeTeamCity` (string): City of the home team.
    - `homeTeamRank` (integer): Rank of the home team.
    - `homeTeamRankPoints` (float): Rank points of the home team.
    - `awayTeamId` (string): Unique identifier for the away team.
    - `awayTeamNickName` (string): Nickname of the away team.
    - `awayTeamCity` (string): City of the away team.
    - `awayTeamRank` (integer): Rank of the away team.
    - `awayTeamRankPoints` (float): Rank points of the away team.

### ERROR HANDLING

- The API handles various error scenarios such as invalid requests, unauthorized access, and server errors.
- Error responses include appropriate status codes and error messages.

### SECURITY

- Authentication is implemented using OAuth2 with password flow.
- Users must authenticate to obtain an access token for accessing protected endpoints.

### LOGGING

- Utilizes Python logging module for logging execution information, including errors and debug details.

### TESTING

- Unit and Integration Testing have been implemented to ensure the correctness and robustness of the code using pytest and Testcontainers.
- Tests cover authentication, endpoint functionality, error handling, and data retrieval.

### CONSIDERATIONS

- Data fetching from the remote API is asynchronous to improve performance.
- Caching mechanism (LRU cache) is applied to reduce redundant data fetching.

