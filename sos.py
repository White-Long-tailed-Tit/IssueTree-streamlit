'''
SOS 버튼 (요청) 누르면 -> 해당 에러 메시지를 파싱 

- IF 파일 경로를 파싱할 수 있는 에러 메시지의 경우 
    1. 파일 경로 및 패키지명 파싱 
    2. 파싱된 파일 경로(With 라인)를 해당 깃허브 레포지토리와 매칭 -> 마지막 커밋 내역을 확인 (git blame 내역)
    3. 마지막 커밋 내역의 사용자 (깃허브 id, email) 정보 추출 
    4. 서버 측으로 [요청자이름+패키지이름+에러 메시지 전문+에러 발생한 곳 담당한 유저 정보+
    추가 설명 코멘트+스택+버전] API 요청

- IF 파일 경로 파싱이 불가능한 에러 메시지의 경우 
    1. 바로 서버측으로 [요청자 이름+에러 메시지 전문+ 추가설명 코멘트+스택+버전] API 보냄
        - 패키지 이름, 에러 발생한 곳 담당 유저 정보 default 처리 필요 
'''

import streamlit as st
import requests
import re

# GitHub 저장소 정보
'''
owner = 'White-Long-tailed-Tit'
repo = 'IssueTree-demo'
branch = 'main'
base_file_path='com/example/demo/'
'''

#test용 
owner = 'White-Long-tailed-Tit'
repo = 'IssueTree-Spring'
branch = 'main'
base_file_path='com\wltt\issuetree'

packages=['question','Member']
sub_packages=['controller','domain','repository','service']


def parsing(search_text):
    isrepo=False
    isfile=False
    isLine=False #라인 넘버 추출가능한 에러인가? 
    line=None

    # 레포지토리명 존재 판단 
    if repo in search_text:
        isrepo=True
    
    
    # 파일 위치 구조명 존재 판단 
    if base_file_path in search_text:
        isfile=True

    # # controller or domain 등등 하위 폴더 구조명이 발견되는지 판단 
    # for sub in sub_packages:
    #     if sub in search_text:
    #         issub=True
    #         sub_path=sub

    # 패키지명과 검색 문자열이 모두 존재하는지 확인하고 패키지명 반환
    if isrepo and isfile: #모두 True이면 
        for package in packages:
            if package in search_text:
                pre_file_path=base_file_path+"\\"+package+"\\" #com\wltt\issuetree\question\controller
                print(pre_file_path)
                

                if pre_file_path in search_text:
                    index = search_text.find(pre_file_path)
                    if index != -1:
                        target_index = index + len(pre_file_path)
                        file_name_index = search_text.find(".", target_index)
                        if file_name_index != -1:
                            end_index = file_name_index
                            if ':' in search_text[file_name_index:]:
                                colon_index = search_text.find(':', file_name_index)
                                if colon_index + 1 < len(search_text):
                                    # 숫자가 나오는 부분까지만 추출
                                    end_num_index = colon_index + 1
                                    while end_num_index < len(search_text) and search_text[end_num_index].isdigit():
                                        end_num_index += 1
                                    if colon_index + 1 != end_num_index:  # 숫자가 없는 경우 처리
                                        line = int(search_text[colon_index + 1:end_num_index])
                                    else:
                                        line = None
                                    end_index = colon_index
                                    isLine = True
                                else:
                                    isLine = False
                                    line = None
                            else:
                                isLine = False
                                line = None
                            print(search_text[target_index:end_index])
                            print("isLine:", isLine)


                            file_name=search_text[target_index:file_name_index]
                            print(search_text[target_index:file_name_index]) #controller\MemberController 파싱 
                
                # for example file_structure: src/main/java/com/wltt/issuetree/question/controller
                file_path="src\\main\\java\\"+pre_file_path+file_name+".java"
                package="com.wltt.issuetree."+package
                file_path=file_path.replace("\\", "/")
                print(file_path)
                return package, file_path, isLine,line 
    
    return None, None, isLine, None


# parsing 테스트 
error_message_example = """
org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'questionController' defined in file [C:\\github\\IssueTree-Spring\\out\\production\\classes\\com\\wltt\\issuetree\\question\\controller\\QuestionController.class]: Unsatisfied dependency expressed through constructor parameter 0; nested exception is org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'questionService' defined in file [C:\\github\\IssueTree-Spring\\out\\production\\classes\\com\\wltt\\issuetree\\question\\service\\QuestionService.class]: Unsatisfied dependency expressed through constructor parameter 0; nested exception is org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'questionRepository' defined in com.wltt.issuetree.question.domain.repository.QuestionRepository defined in @EnableElasticsearchRepositories declared on ElasticsearchRepositoriesRegistrar.EnableElasticsearchRepositoriesConfiguration: Invocation of init method failed; nested exception is org.springframework.beans.BeanInstantiationException: Failed to instantiate [org.springframework.data.elasticsearch.repository.support.SimpleElasticsearchRepository]: Constructor threw exception; nested exception is org.springframework.data.elasticsearch.UncategorizedElasticsearchException: java.util.concurrent.ExecutionException: java.net.ConnectException: Timeout connecting to [682fb71161354b0d812e6c2d5f5fc8ca.us-west-2.aws.found.io/52.26.59.44:443]; nested exception is ElasticsearchException[java.util.concurrent.ExecutionException: java.net.ConnectException: Timeout connecting to [682fb71161354b0d812e6c2d5f5fc8ca.us-west-2.aws.found.io/52.26.59.44:443]]; nested: ExecutionException[java.net.ConnectException: Timeout connecting to [682fb71161354b0d812e6c2d5f5fc8ca.us-west-2.aws.found.io/52.26.59.44:443]]; nested: ConnectException[Timeout connecting to [682fb71161354b0d812e6c2d5f5fc8ca.us-west-2.aws.found.io/52.26.59.44:443]];
"""
package,file_path,isLine,line=parsing(error_message_example)
print(package)
print(file_path)
print(line)

#parsing test : line 넘버 추출 가능한 경우 
# error_message_example2='''
# C:\Users\user\Desktop\휴학\IssueTree-demo\demo\src\main\java\com\example\demo\controller\MemberController.java:4: error: package com.example.demo.service does not exist
# import com.example.demo.service.MemberService;'''





def get_git_blame_line(owner, repo, file_path, token, branch):
    headers = {
        'Authorization': f'token {token}'
    }
    
    # GraphQL 쿼리
    query = """
    query GetGitBlame($owner: String!, $repo: String!, $file_path: String!, $branch: String!) {
      repository(owner: $owner, name: $repo) {
        object(expression: $branch) {
          ... on Commit {
            blame(path: $file_path) {
              ranges {
                startingLine
                endingLine
                age
                commit {
                  oid
                  author {
                    name
                    email
                  }
                }
              }
            }
          }
        }
      }
    }
    """
    
    variables = {
        "owner": owner,
        "repo": repo,
        "file_path": file_path,
        "branch": branch
    }
    
    response = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': variables}, headers=headers)
    
    if response.status_code == 200:
        blame_data = response.json()
        return blame_data
    else:
        print(f"Failed to retrieve Git blame data: {response.status_code}")
        return None

def get_bit_blame(owner, repo, file_path, token, branch):
    # API 요청 보내기
    url = f'https://api.github.com/repos/{owner}/{repo}/commits?path={file_path}&sha={branch}'
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)

    # 응답 처리
    if response.status_code == 200:
        commits = response.json()
        for commit in commits:
            commit_info = {
                'commit_sha': commit['sha'],
                'author': commit['commit']['author']['name'],
                'email': commit['commit']['author']['email'],
                'message': commit['commit']['message']
            }
            print(commit_info)
            return commit_info
    else:
        print(f'API 요청에 실패했습니다. 상태 코드: {response.status_code}')

'''
# 파일 경로
file_path = 'demo/src/main/java/com/example/demo/Member/controller/MemberController.java'

# 사용자 인증 토큰
token = '당신의_사용자인증토큰을_넣어주세요'

# Git blame 정보 가져오기
blame_data = get_git_blame(owner, repo, file_path, token, branch)
if blame_data:
    # Git blame 정보 출력
    print(json.dumps(blame_data, indent=2))
'''

def send_form(reporter_name,error_message,comment,stack,version,package_name=None,manager_github_id=None):
    # POST 요청 보낼 URL
    url = 'http://ec2-43-202-41-32.ap-northeast-2.compute.amazonaws.com/api/v1/reports'  # 서버의 실제 URL로 변경해야 합니다.

    # POST 요청 보낼 데이터
    data = {
        'reporter_name': reporter_name,
        'package_name': package_name,
        'error_message': error_message,
        'manager_github_id': manager_github_id,
        'comment': comment,
        'stack': stack,
        'version': version
    }

    # POST 요청 보내기
    response = requests.post(url, data=data)

    # 응답 확인
    if response.status_code == 200:
        print('POST 요청이 성공적으로 보내졌습니다.')
    else:
        print('POST 요청이 실패하였습니다. 상태 코드:', response.status_code)