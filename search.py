import elastic_connect
from elasticsearch import Elasticsearch
from datetime import datetime
import streamlit as st

def search(selected_library,tag_version,search_text):
    # Elasticsearch 호스트 및 포트 설정
    es_host = "smw-whiteeye.es.us-west-2.aws.found.io"
    es_port = 9243
    es_scheme = "https"  

    # 사용자 이름과 비밀번호
    username = st.secrets['ELASTIC_ID']
    password = st.secrets['ELASTIC_PW']

    # Elasticsearch에 연결을 시도합니다.

    # Elasticsearch에 HTTP Basic Authentication을 사용하여 연결합니다.
    es = Elasticsearch(
        [{'host': es_host, 'port': es_port, 'scheme': es_scheme}],
        basic_auth=(username, password)
    )

    # Elasticsearch에 쿼리를 실행합니다.
    query = {
            "query": {
                "function_score": {
                    "query": {
                        "bool": {
                            "must": [
                                {"match": {"stack": selected_library}},
                            ],
                            "should": [
                                {
                                "match": {
                                    "issue": {
                                    "query": search_text,
                                    }
                                }
                                }
                            ]
                        }
                    },
                    "functions": [
                        {
                        "filter": { "match": { "version": tag_version } },
                        "weight": 1
                        },
                        {
                        "filter": { "exists": { "field": "lastModifiedDate" } },
                        "weight": 1.5
                        },
                        {
                        "filter": { "exists": { "field": "createdDate" } },
                        "weight": 1.5
                        }
                    ],
                    "score_mode": "sum",
                    "boost_mode": "multiply"
                }
            }
        }

    # Elasticsearch에 쿼리를 실행하고 결과를 출력합니다.
    result = es.search(index="questions", body=query)
    print("쿼리문:",query)
    print("쿼리 결과:", result)
    # 검색 결과에서 hits.total.value 값을 가져옴
    total_hits = result['hits']['total']['value']

    # 데이터 변수 초기화
    data = {
        "issue": [],
        "stack": [],
        "version": [],
        "createdDate": [],
        "lastModifiedDate": [],
        "questioner": [],
        "solve": [],
        "ts": []
        
    }

    # 쿼리 결과를 파싱하여 data 딕셔너리에 데이터 추가
    for hit in result["hits"]["hits"]:
        data["issue"].append(hit["_source"]["issue"])
        data["createdDate"].append(datetime.strptime(hit["_source"]["createdDate"], "%Y%m%dT%H%M%S.%fZ").strftime("%Y/%m/%d %H:%M:%S"))
        data["lastModifiedDate"].append(datetime.strptime(hit["_source"]["lastModifiedDate"], "%Y%m%dT%H%M%S.%fZ").strftime("%Y/%m/%d %H:%M:%S"))
        data["questioner"].append(hit["_source"]["questioner"])
        data["solve"].append(hit["_source"]["solve"])
        data["stack"].append(hit["_source"]["stack"])
        data["ts"].append(hit["_source"]["ts"])
        data["version"].append(hit["_source"]["version"])


    # total_hits가 0이면 False를 반환, 그 외에는 True를 반환
    if total_hits == 0:
        return False,None
    else:
        return True,data
