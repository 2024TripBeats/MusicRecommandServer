# global_data.py

import pandas as pd
import numpy as np

# CSV 경로 정의
csv_paths = {
    '아침': './morning_score_id.csv',
    '오후': './afternoon_score_id.csv',
    '밤': './night_score_id.csv'
}

# CSV 파일 및 데이터 로드
dfs = {time: pd.read_csv(path, index_col=0) for time, path in csv_paths.items()}
music_embeddings = np.load('./music_embeddings.npy')
user_preferences_embeddings = np.load('./average_embeddings.npy', allow_pickle=True)
music_hashtags_data = pd.read_csv('./music_recommendation_list.csv')
