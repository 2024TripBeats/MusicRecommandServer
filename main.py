from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Place(BaseModel):
    placeId: str
    placeName: str
    duration: int

class PlaceMusicPair(BaseModel):
    placeId: str
    placeName: str
    musicId: str
    musicName: str
    musicArtist: str
    duration: int

class TravelSegmentDto(BaseModel):
    distance: float

class RecommendationCandidateRequestDto(BaseModel):
    itinerary: List[Place]
    travelSegments: List[TravelSegmentDto]

class RecommendationCandidateResponseDto(BaseModel):
    itinerary: List[PlaceMusicPair]
    travelSegments: List[TravelSegmentDto]

class DayRecommendationRequestDto(BaseModel):
    dayNumber: int
    candidates: List[RecommendationCandidateRequestDto]

class DayRecommendationResponseDto(BaseModel):
    dayNumber: int
    candidates: List[RecommendationCandidateResponseDto]

class FinalRecommendationRequestDto(BaseModel):
    recommendations: List[DayRecommendationRequestDto]
    musicGenres: List[str]
    genreOpenness: int
    musicTags: List[str]
    tagOpenness: int

class FinalRecommendationResponseDto(BaseModel):
    recommendations: List[DayRecommendationResponseDto]

@app.post("/music_recommend", response_model=FinalRecommendationResponseDto)
async def music_recommend(request: FinalRecommendationRequestDto):
    # 로그에 요청 데이터를 출력합니다.
    print("Received request:")
    print(request)

    # 샘플 응답 데이터
    sample_response = FinalRecommendationResponseDto(
        recommendations=[
            DayRecommendationResponseDto(
                dayNumber=1,
                candidates=[
                    RecommendationCandidateResponseDto(
                        itinerary=[
                            PlaceMusicPair(
                                placeId="1",
                                placeName="Central Park",
                                musicId="101",
                                musicName="Relaxing Vibes",
                                musicArtist="Maroon 5",
                                duration=120
                            ),
                            PlaceMusicPair(
                                placeId="2",
                                placeName="Statue of Liberty",
                                musicId="102",
                                musicName="Freedom Symphony",
                                musicArtist="John Williams",
                                duration=180
                            )
                        ],
                        travelSegments=[
                            TravelSegmentDto(
                                distance=5
                            )
                        ]
                    ),
                    RecommendationCandidateResponseDto(
                        itinerary=[
                            PlaceMusicPair(
                                placeId="3",
                                placeName="Empire State Building",
                                musicId="103",
                                musicName="City Lights",
                                musicArtist="The Weeknd",
                                duration=90
                            ),
                            PlaceMusicPair(
                                placeId="4",
                                placeName="Times Square",
                                musicId="104",
                                musicName="Neon Nights",
                                musicArtist="Daft Punk",
                                duration=60
                            )
                        ],
                        travelSegments=[
                            TravelSegmentDto(
                                distance=2
                            )
                        ]
                    )
                ]
            ),
            DayRecommendationResponseDto(
                dayNumber=2,
                candidates=[
                    RecommendationCandidateResponseDto(
                        itinerary=[
                            PlaceMusicPair(
                                placeId="5",
                                placeName="Brooklyn Bridge",
                                musicId="105",
                                musicName="Bridge to Tranquility",
                                musicArtist="Norah Jones",
                                duration=110
                            ),
                            PlaceMusicPair(
                                placeId="6",
                                placeName="Fifth Avenue",
                                musicId="106",
                                musicName="Shopping Spree",
                                musicArtist="Madonna",
                                duration=75
                            )
                        ],
                        travelSegments=[
                            TravelSegmentDto(
                                distance=3.5
                            )
                        ]
                    ),
                    RecommendationCandidateResponseDto(
                        itinerary=[
                            PlaceMusicPair(
                                placeId="7",
                                placeName="Broadway",
                                musicId="107",
                                musicName="Broadway Classics",
                                musicArtist="Andrew Lloyd Webber",
                                duration=100
                            ),
                            PlaceMusicPair(
                                placeId="8",
                                placeName="Wall Street",
                                musicId="108",
                                musicName="Wall Street Blues",
                                musicArtist="Eric Clapton",
                                duration=130
                            )
                        ],
                        travelSegments=[
                            TravelSegmentDto(
                                distance=4
                            )
                        ]
                    )
                ]
            )
        ]
    )
    return sample_response

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
