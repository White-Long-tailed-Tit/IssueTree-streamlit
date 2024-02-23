#ElasticSearch document와 연결 

import streamlit as st
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError


def connect():
    # Elasticsearch 호스트 및 포트 설정
    es_host = "smw-whiteeye.es.us-west-2.aws.found.io"
    es_port = 9243
    es_scheme = "https"  

    # 사용자 이름과 비밀번호
    username = st.secrets['ELASTIC_ID']
    password = st.secrets['ELASTIC_PW']

    # Elasticsearch에 연결을 시도합니다.
    try:
        # Elasticsearch에 HTTP Basic Authentication을 사용하여 연결합니다.
        es = Elasticsearch(
            [{'host': es_host, 'port': es_port, 'scheme': es_scheme}],
            basic_auth=(username, password)
        )
        
        # Elasticsearch에 핑을 보내서 응답을 확인합니다.
        if es.ping():
            print("Elasticsearch에 성공적으로 연결되었습니다.")
        else:
            print("Elasticsearch에 연결할 수 없습니다: 핑 실패")
        
    except ConnectionError as e:
        # Elasticsearch에 연결되지 않은 경우, 오류 메시지를 출력합니다.
        print("Elasticsearch에 연결할 수 없습니다:", e)

    # Elasticsearch에서 문서 가져오기
    index_name = "questions"  # Elasticsearch 인덱스 이름
    query = {"query": {"match_all": {}}}  # 모든 문서를 가져오는 쿼리
    docs = es.search(index=index_name, body=query)["hits"]["hits"]

    # 데이터 변수 초기화
    data = {
        "issue": [],
        "createdDate": [],
        "lastModifiedDate": [],
        "questioner": [],
        "solve": [],
        "stack": [],
        "ts": [],
        "version": []
    }

    # 문서를 반복하면서 데이터 변수에 값 할당
    for doc in docs:
        source = doc["_source"]
        data["issue"].append(source.get("issue", ""))
        data["createdDate"].append(source.get("createdDate", ""))
        data["lastModifiedDate"].append(source.get("lastModifiedDate", ""))
        data["questioner"].append(source.get("questioner", ""))
        data["solve"].append(source.get("solve", ""))
        data["stack"].append(source.get("stack", ""))
        data["ts"].append(source.get("ts", ""))
        data["version"].append(source.get("version", ""))

    return data 