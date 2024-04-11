import logging
import aiohttp
import asyncio
from datetime import datetime
from functools import lru_cache

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.openapi.utils import get_openapi

from model import User, Event, EventsRequest


"""
Creating a logger object
"""
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""
Initializing FastAPI application
"""
app = FastAPI(
    title="Medida Challenge API",
    description="This is the API that must be implemented as your output deliverable of this challenge",
    version="0.1.0",
    contact={
        "name": "Medida",
        "email": "challenges@medida.com",
        "url": "https://www.medida.com/"
    }
)

"""
Creating OAuth2 password bearer scheme
"""

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

"""
Creating a mock user database with dummy user data
"""

USERS = {
    "user1": {
        "username": "user1",
        "password": "password1",
        "role": "admin"
    },
    "user2": {
        "username": "user2",
        "password": "password2",
        "role": "user"
    }
}


async def fetch_user(username: str):
    return USERS.get(username)

async def authenticate_user(username: str, password: str):
    """
    Function for authenticating users.
    Returning authenticated user objects or False
    """
    user = await fetch_user(username)
    if not user:
        return False
    if password != user["password"]:
        return False
    return User(**user)

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint for user login to obtain access token.
    In case of success, create and return JWT Token
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException (
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": user.username, "token_type": "bearer"}

# Cache up to 128 recent calls
@lru_cache(maxsize=128)  
async def fetch_data(session, url):
    """
    Function to fetch data from a remote API.
    """
    logger.info(f"Fetching data from {url}")
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()
    except aiohttp.ClientError as e:
        logger.error(f"Error fetching data from {url}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error fetching data: {str(e)}")
    except ValueError as e:
        logger.error(f"Invalid response from {url}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid response from mock API: {str(e)}")


@app.post("/events", response_model=list[Event], tags=["challenge"])
async def polling_events(request: EventsRequest, token: str = Depends(oauth2_scheme)):
    """
    Endpoint to retrieve a list of NFL events between the specified start and end dates.
    """
    async with aiohttp.ClientSession() as session:
        scoreboard_url = "http://localhost:9000/NFL/scoreboard"
        team_rankings_url = "http://localhost:9000/NFL/team-rankings"

        try:
            # Fetch data from remote APIs concurrently
            scoreboard_data, team_rankings_data = await asyncio.gather(
                fetch_data(session, scoreboard_url),
                fetch_data(session, team_rankings_url)
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Unknown error occurred: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Unknown error occurred: {str(e)}")

        events = [] 
        
        for scoreboard_event in scoreboard_data:  
            # Parse event date from timestamp and convert to datetime.date object
            event_date = datetime.strptime(scoreboard_event["timestamp"].split("T")[0], '%Y-%m-%d').date()
            # Filter events based on the specified start and end dates
            if request.startDate <= event_date <= request.endDate:
                home_team_id = scoreboard_event["home"]["id"]
                away_team_id = scoreboard_event["away"]["id"]
                home_team_rank = next((team["rank"] for team in team_rankings_data if team["teamId"] == home_team_id), None)
                home_team_rank_points = next((team["rankPoints"] for team in team_rankings_data if team["teamId"] == home_team_id), None)
                away_team_rank = next((team["rank"] for team in team_rankings_data if team["teamId"] == away_team_id), None)
                away_team_rank_points = next((team["rankPoints"] for team in team_rankings_data if team["teamId"] == away_team_id), None)
                # Construct event object and append to events list
                event = {
                    "eventId": scoreboard_event["id"],
                    "eventDate": event_date.strftime('%Y-%m-%d'),  # Format event date as string
                    "eventTime": scoreboard_event["timestamp"].split("T")[1][:-1],
                    "homeTeamId": home_team_id,
                    "homeTeamNickName": scoreboard_event["home"]["nickName"],
                    "homeTeamCity": scoreboard_event["home"]["city"],
                    "homeTeamRank": home_team_rank,
                    "homeTeamRankPoints": home_team_rank_points,
                    "awayTeamId": away_team_id,
                    "awayTeamNickName": scoreboard_event["away"]["nickName"],
                    "awayTeamCity": scoreboard_event["away"]["city"],
                    "awayTeamRank": away_team_rank,
                    "awayTeamRankPoints": away_team_rank_points,
                }
                events.append(event)

        return events

"""
Customized OpenAPI schema
"""

custom_openapi_schema = get_openapi(
    title="Medida Challenge API",
    version="0.1.0",
    description="This is the API that must be implemented as your output deliverable of this challenge",
    routes=app.routes,
)


@app.get("/openapi.json", include_in_schema=False)
async def get_custom_openapi_schema():
    """
    Serve the customized OpenAPI schema at /openapi.json
    """
    return custom_openapi_schema
