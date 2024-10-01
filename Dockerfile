# 1. Python 3.10 slim 버전의 이미지를 사용합니다.
FROM python:3.10-slim

# 2. 컨테이너 안에서 작업 디렉토리를 /app으로 설정합니다.
WORKDIR /app

# 3. 필요한 패키지를 설치하기 위해 requirements.txt 파일을 컨테이너로 복사합니다.
COPY requirements.txt /app/

# 4. 패키지 의존성들을 설치합니다.
RUN pip install --no-cache-dir -r requirements.txt

# 5. 현재 프로젝트의 모든 파일을 컨테이너로 복사합니다.
COPY . /app

# CSV 파일을 포함한 데이터를 복사합니다. (필요한 파일을 여기에 추가)
COPY afternoon_score_id.csv /app/
COPY morning_score_id.csv /app/
COPY night_score_id.csv /app/
COPY music_recommendation_list.csv /app/
COPY music_embeddings.npy /app/
COPY average_embeddings.npy /app/

# 6. uvicorn을 이용해 FastAPI 서버를 실행합니다.
CMD ["uvicorn", "backend.music_recommendation:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
