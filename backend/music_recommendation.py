from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
from backend.models.main import main_pipeline
import numpy as np

app = FastAPI()

# 장소 정보 모델 (요청/응답 공통)
class Place(BaseModel):
    placeId: str
    placeName: str
    category: str
    duration: int
    order: int
    price: int

# 여행 구간 정보 모델 (요청/응답 공통)
class TravelSegmentDto(BaseModel):
    distance: float

# 하루 일정 정보 (요청)
class DayItineraryRequestDto(BaseModel):
    dayNumber: int
    places: List[Place]  # 하루 동안 방문할 장소 리스트
    travelSegments: List[TravelSegmentDto]  # 하루 동안의 구간 정보

# 추천 후보의 요청 데이터 모델 (요청)
class RecommendationCandidateRequestDto(BaseModel):
    candidates: int  # 후보의 ID 또는 후보 개수 (각각의 추천 후보)
    itinerary: List[DayItineraryRequestDto]  # 여러 날의 일정 포함

# 최종 요청 모델 (요청)
class FinalRecommendationRequestDto(BaseModel):
    recommendations: List[RecommendationCandidateRequestDto]  # 여러 후보
    musicGenres: List[str]
    genreOpenness: int
    musicTags: List[str]
    tagOpenness: int

# 응답 모델에서 하루 일정 정보 (응답)
class PlaceMusicPair(BaseModel):
    placeId: str
    placeName: str
    category: str
    duration: int
    order: int
    price: int
    new_order: Optional[int] = None  # 추가된 필드, None 허용
    timeOfDay: Optional[str] = None  # 추가된 필드, None 허용
    music_bool: Optional[bool] = None  # 추가된 필드, None 허용
    musicId: Optional[str] = None
    musicName: Optional[str] = None
    musicArtist: Optional[str] = None
    spotify_id: Optional[str] = None

# 하루의 응답 데이터 모델 (응답)
class DayItineraryResponseDto(BaseModel):
    dayNumber: int
    places: List[PlaceMusicPair]  # 음악 정보가 포함된 장소 리스트
    travelSegments: List[TravelSegmentDto]  # 구간 정보

# 추천 후보의 응답 데이터 모델 (응답)
class RecommendationCandidateResponseDto(BaseModel):
    candidates: int  # 후보 ID 또는 개수
    itinerary: List[DayItineraryResponseDto]  # 여러 날의 음악 추천 일정

# 최종 응답 모델 (응답)
class FinalRecommendationResponseDto(BaseModel):
    recommendations: List[RecommendationCandidateResponseDto]  # 여러 후보


@app.post("/music_recommend", response_model=FinalRecommendationResponseDto)
async def music_recommend(request: FinalRecommendationRequestDto):

    # Call the main_pipeline function
    result = main_pipeline(request.dict())

    # Process the result to match the response model
    recommendations = []
    for recommendation in result['recommendations']:  # result가 딕셔너리임
        candidates_count = recommendation['candidates']
        itinerary = []

        for day in recommendation['itinerary']:  # 각 day 정보 접근
            day_response = DayItineraryResponseDto(
                dayNumber=day['dayNumber'],
                places=[
                    PlaceMusicPair(
                        placeId=place['placeId'],
                        placeName=place['placeName'],
                        category=place['category'],
                        duration=place['duration'],
                        order=place['order'],
                        new_order=place.get('new_order'),
                        timeOfDay=place.get('timeOfDay'),
                        music_bool=place.get('music_bool'),
                        musicId=place.get('top_musicId'),
                        musicName=place.get('song_title'),
                        musicArtist=place.get('artist_name'),
                        spotify_id=place.get('spotify_id'),
                        price=place['price']
                    ) for place in day['places']  # 'places' 리스트에서 음악 포함된 장소 파싱
                ],
                travelSegments=day['travelSegments']  # 'travelSegments' 정보 파싱
            )
            itinerary.append(day_response)

        day_recommendation = RecommendationCandidateResponseDto(
            candidates=candidates_count,
            itinerary=itinerary
        )
        recommendations.append(day_recommendation)

    response = FinalRecommendationResponseDto(
        recommendations=recommendations
    )

    return response

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)