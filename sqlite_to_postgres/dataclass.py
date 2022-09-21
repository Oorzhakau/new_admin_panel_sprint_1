import uuid
from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal


@dataclass
class MixinId:
    id: uuid.UUID


@dataclass
class MixinDate:
    updated_at: datetime
    created_at: datetime


@dataclass
class Genre(MixinId, MixinDate):
    name: str
    description: str


@dataclass
class Filmwork(MixinId, MixinDate):
    title: str
    description: str
    creation_date: date
    file_path: str
    rating: float
    type: Literal["movie", "tv_show"]


@dataclass
class Person(MixinId, MixinDate):
    full_name: str


@dataclass
class GenreFilmwork(MixinId):
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created_at: datetime


@dataclass
class PersonFilmwork(MixinId):
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: Literal["director", "writer", "actor"]
    created_at: datetime
