# Omarchy Calendar 안내 사이트

안성훈이 사용하는 개인용 Google Calendar 읽기 전용 연동의 앱 소개와 개인정보처리방침입니다.

- `index.html`: 앱 기능, 요청 권한, 로컬 처리와 지원 연락처를 안내합니다.
- `privacy.html`: Google 데이터 접근·이용·보관·외부 연결·제한적 사용·접근 해제 및 삭제를 설명합니다.
- 이 저장소는 정적 안내 페이지입니다. Google 로그인, 캘린더 동기화 또는 토큰 수집을 웹에서 수행하지 않습니다.
- 실제 일정 표시는 Omarchy의 `tmn73.calendar` 플러그인과 Google Workspace CLI(`gws`)가 사용자 컴퓨터에서 처리합니다.

## 로컬 확인

두 HTML 파일은 직접 열 수 있습니다. 추가 패키지 없이 다음 명령으로 로컬 HTTP 및 페이지 연결을 검사할 수 있습니다.

```sh
python -m unittest discover -s tests -v
```

## 배포

GitHub Pages에서 `main` 브랜치의 루트 디렉터리(`/`)를 게시합니다. `.nojekyll` 파일로 정적 HTML을 그대로 제공합니다. OAuth 자격 증명, 일정 캐시, 로그 및 로컬 검토 기록은 공개 파일에 포함하지 않습니다.

## 정책 관리

현재 방침의 범위는 Google Calendar 읽기 전용 설정입니다. 일정 쓰기, 다른 백엔드 또는 데이터 처리 방식을 바꿀 때에는 실제 동작에 맞춰 정책을 다시 검토해야 합니다. 이 사이트는 Google 또는 Omarchy의 공식 서비스가 아니며, Google의 인증 심사 통과를 보장하지 않습니다.

운영 및 지원: 안성훈 · kjn0406@gmail.com
