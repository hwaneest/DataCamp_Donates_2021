# 학습 목표 및 목차

### 학습 목표

---

- Git과 GitHub의 차이
    - Git은 버전관리 어플리케이션. Github는 git을 클라우드 환경에서 업로드하는 원격 저장소. 흔히 제일 많이 쓰이고, 다른 거는 gitlab 등이 있음

        → git은 소스코드 버전 관리 시스템

        → github은 버전 관리 호스팅 사이트

- Git의 add, commit, push, pull
    - add : 스테이지 영역으로 올리는 것
    - commit : 스테이지 영역에서 확정하는거 (push와 pull시 commit이 되어있어야함)
    - push : 원격저장소에 깃을 업로드 하는 것
    - pull : 원격저장소에 업로드되어 있는 것을 받아오는 것
- Github 소스코드 버전 관리
    - 일반적인내용일듯
- Jupyter Notebook
- 마크다운 문법

# 사전 궁금증

- add 와 commit 시 각각 stage 영역을 왔다갔다 하는데, 영역을 정확히 모르겠다

# 몰랐던 것

### Git의 Repository 구조

![스크린샷 2021-09-09 오전 10.08.30.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/cd34d7c6-36b2-4283-8afa-c400c3000194/스크린샷_2021-09-09_오전_10.08.30.png)

작업폴더(Working directory), 인덱스(Staging Area), 저장소(Head-Repository)

**작업폴더**

- 우리가 작업하는 폴더

**인덱스**

- commit을 실행하기 전에 작업트리와 저장소 사이에 존제하는 가상의 영역

작업폴더에서 Untracked files(추가), Modified files(변경)을 인덱스에 stage(기록) 해야만 commit 할 수 있음 → git add

`git rm --cached <files>` 를 통해서 인덱스에 추가된 파일 제외 가능

---

# 더 나아가기 (질문)

```python
git add .

git commit -a -m

git commit -am

gcam

다똑같은거 맞나?
```

- 원격저장소에 이미 올라간 파일 삭제하는 매커니즘 이해하기

git push -u 할때 u가 정확히 뭐지

ssh-keygen을 해서 만들면 뭐 문제가 있나 → 없는듯

[Git - SSH 공개키 만들기](https://git-scm.com/book/ko/v2/Git-서버-SSH-공개키-만들기)

**단상**

token 방식이 30일짜리 발급받으면 30일동안은 써도 되는 개념이면 그냥 token으로 하는 것도 나쁘지는 않을 것 같다.