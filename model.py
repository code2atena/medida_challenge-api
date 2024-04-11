from datetime import datetime
from pydantic import BaseModel, Field, validator


class User(BaseModel):
    """
    User model
    """
    username: str
    role: str


class Event(BaseModel):
    """
    Response model for events endpoint
    """
    eventId: str
    eventDate: str
    eventTime: str
    homeTeamId: str
    homeTeamNickName: str
    homeTeamCity: str
    homeTeamRank: int
    homeTeamRankPoints: float
    awayTeamId: str
    awayTeamNickName: str
    awayTeamCity: str
    awayTeamRank: int
    awayTeamRankPoints: float


class EventsRequest(BaseModel):
    """
    Request model for events endpoint
    """
    startDate: str = Field(..., pattern=r'\d{4}-\d{2}-\d{2}')
    endDate: str = Field(..., pattern=r'\d{4}-\d{2}-\d{2}')

    @validator('startDate', 'endDate')
    def parse_date(cls, value):
        try:
            return datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError('Dates must be in the format YYYY-MM-DD')

    @validator('endDate')
    def end_date_after_start_date(cls, value, values):
        if 'startDate' in values and value < values['startDate']:
            raise ValueError('End date must be after start date')
        return value
