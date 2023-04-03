# API-study_2023

Wellysis 두번째 사내 스터디 (기초 백엔드 API) 기록 repo입니다.

회사 계정으로 진행 중이라 관련 내용은 별도로 현 계정에 업데이트 중입니다.

첫번째 스터디와 다른 점: token 인증 구현, 사용자 구현, 코드 리뷰 등, 첫번째 스터디에서 스킵했던 것을 모두 구현하고, 코드 리뷰를 통해 더욱 좋은 코드를 구현하고자 합니다.
- 첫번째 스터디 보러 가기 [링크](https://github.com/HeesunPark26/API-study_2022/)

기간: 2023.02 - 진행 중

## 코드 구조
- `create_db.py`: `db_schema.sql`에 정의되어 있는대로 전체 DB 만들기
- `db_schema.sql`: 각 table이 정의되어 있음
- `main.py`: 메인 코드 구현
- `utils_func.py`: 메인 api 구현 시 중복되는 로직 등을 따로 저장해놓은 파일
- `utils_sql.py`: 메인 api 구현 시 중복되는 DB 콜 로직을 따로 저장해놓은 파일


## 레퍼런스
- [소개](https://medium.com/@ericsimons/introducing-realworld-6016654d36b5#id_token=eyJhbGciOiJSUzI1NiIsImtpZCI6Ijc0ODNhMDg4ZDRmZmMwMDYwOWYwZTIyZjNjMjJkYTVmZTM5MDZjY2MiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYmYiOjE2NTQ0OTg5OTgsImF1ZCI6IjIxNjI5NjAzNTgzNC1rMWs2cWUwNjBzMnRwMmEyamFtNGxqZGNtczAwc3R0Zy5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjExNjYxMDAzNDU1OTcyMDg3ODE1MCIsImVtYWlsIjoiamluc29vYnllb25AZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF6cCI6IjIxNjI5NjAzNTgzNC1rMWs2cWUwNjBzMnRwMmEyamFtNGxqZGNtczAwc3R0Zy5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsIm5hbWUiOiJKaW5zb28gQnllb24iLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUFUWEFKd2lPSTRXTlVyTjV6aGNNX3R4akxDUmI0MWdtMU00TEpxZXR6enM9czk2LWMiLCJnaXZlbl9uYW1lIjoiSmluc29vIiwiZmFtaWx5X25hbWUiOiJCeWVvbiIsImlhdCI6MTY1NDQ5OTI5OCwiZXhwIjoxNjU0NTAyODk4LCJqdGkiOiIzZjQyM2JjNDg3OWRkZjk2MzYwOTZjYzAxODJkOGFlMTY2ZjAyYjA4In0.fWGLeXIJ-AwZixhwdZ7KPrTISbYgto1fP1kLxI4NuUDQhoKFdWDYH0qC2uEkGKMTGY5bWwsU1T5QTGE6ei4HseZuiUzAOsDoMeEItM5OJp7SrEYP1e3-s8fIWm_wGjSmH86XqhQIbplms0ZjKem1-CHFokPuZWSTN3ezV7CaeiF8__AMw3G-kL8652FAxae0y-gd4rUd6WC5JjENLx38HT_Rfle31jW5EXr2mavLkEmkqB1_z6rIMdLfhVJ2upCPyBL2gT4YgrCUQLF9M4PwP4rRz-DJNgqk4WlHVH7VcmqKXb-6wG5SukKR45jjiVBCKYbHjySfjH_vmayB4CMqIQ)
- [공식 홈페이지](https://realworld-docs.netlify.app/)
- [데모](https://demo.realworld.io/#/)
- [API 문서](https://api.realworld.io/api-docs/#/)
- [Best Practice](https://codebase.show/projects/realworld)
