import logging
import aiohttp
import asyncio
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.openapi.utils import get_openapi

from model import User, Event, EventsRequest


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
USERS = {
    "user1": {
        "username": "user1",
        "password": "password1",
    },
    "user2": {
        "username": "user2",
        "password": "password2",
    }
}


async def fetch_user(username: str):
    return USERS.get(username)

async def authenticate_user(username: str, password: str):
    user = await fetch_user(username)
    if password == user['password']:
        return User(**user)
    else:
        return False

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException (
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": user.username, "token_type": "bearer"}

 
async def fetch_data(session, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.post("/events", response_model=list[Event], tags=["challenge"])
async def polling_events(request: EventsRequest, token: str = Depends(oauth2_scheme)):
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

        events = [] 
        
        for scoreboard_event in scoreboard_data:  
            # Parse event date from timestamp and convert to datetime.date object
            event_date = datetime.strptime(scoreboard_event["timestamp"].split("T")[0], '%Y-%m-%d').date()
            if request.startDate < event_date < request.endDate:
                home_team_id = scoreboard_event["home"]["id"]
                away_team_id = scoreboard_event["away"]["id"]
                home_team_rank = next((team["rank"] for team in team_rankings_data if team["teamId"] == home_team_id), None)
                away_team_rank = next((team["rank"] for team in team_rankings_data if team["teamId"] == away_team_id), None)
                # Construct event object and append to events list
                event = {
                    "eventId": scoreboard_event["id"],
                    "eventDate": event_date.strftime('%Y-%m-%d'),
                    "eventTime": scoreboard_event["timestamp"].split("T")[1][:-1],
                    "homeTeamNickName": scoreboard_event["home"]["nickName"],
                    "homeTeamCity": scoreboard_event["home"]["city"],
                    "homeTeamRank": home_team_rank,
                    "awayTeamId": away_team_id,
                    "awayTeamNickName": scoreboard_event["away"]["nickName"],
                    "awayTeamRank": away_team_rank,
                }
                events.append(event)

        return events


