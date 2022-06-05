# 프로젝트 소개

![luluisher](https://velog.velcdn.com/images/sorin44/post/223b6137-92f2-414f-bc37-b78b8b69381c/image.jpg)

## 클론코딩 사이트
룰루레몬(https://shop.lululemon.com)

## 작업 기간
2022.05.23 ~ 2022. 06. 03

## 팀명
신난아이셔(luluIsher)

## 팀원 소개

| 개발 분야  | 팀원 명                        |
| ---------- | ------------------------------ |
| 프론트엔드 | 이해용, 김형겸, 장수연, 안현정 |
| 백엔드     | 이예은, 최혜인                 |

## 기술 스택
FrontEnd - HTML/CSS, JavaScript, React.js , React-Router, React-Router-DOM, Sass
BackEnd - Python, Django, MySQL, Bcrypt, pyJWT

## 프론트 엔드 업무 담당
이해용 - Navbar, Main </br>
김형겸 - 물품 리스트, footer </br>
안현정 - 물품 세부(+리뷰) </br>
장수연 - 회원가입/로그인, 장바구니 </br>

## 백엔드 업무 담당
이예은 - DB 모델링, 회원가입/로그인 API, 상품상세페이지 API, 장바구니 API </br>
최혜인 - DB 모델링, 상품상세페이지 API, 상품리스트 API, 장바구니 API, 리뷰 API </br>


#### Users app
- 정규식을 이용해 이메일과 비밀번호, 핸드폰번호 유효성 검사
- bcrypt 를 이용해 비밀번호 암호화
- 로그인 시 jwt 토큰 발행, 장바구니 접근 권한 허용

#### Products app
- 상품 상세 정보 : 상품 상세 페이지 Path parameter를 사용하여 특정 상품의 
상세 데이터 전송 구현
- 상품 리스트 : 메뉴별 혹은 카테고리 별 상품 리스트 Query parameter를 사용하여 메뉴별 혹은 카테고리별 상품 데이터 전송 구현
- 필터링 : 메뉴별 혹은 카테고리 별 상품 필터링 Q 객체를 사용하여 필터 조건에 따라 상품을 거르고 해당 상품들의 데이터를 전송 구현
- 검색 : 상품 검색 상품명에 검색어가 포함된 상품들의 데이터를 전송 구현
- 상품 이름 순, 가격오름차순, 가격내림차순 정렬 후 전송
- 상품 리뷰 및 별점 작성, 리뷰 총 개수, 별점 평균, 가져오기, 삭제하기 구현

#### Carts app
- 장바구니 담기, 가져오기, 장바구니 페이지에서 수정하기, 삭제 하기 구현

## 신난아이셔 주요 기능 소개

## 시연영상
[![시연영상](https://img.youtube.com/vi/W34uDKZyf1s/0.jpg)](https://www.youtube.com/embed/W34uDKZyf1s)

(클릭하시면 유튜브에서 시청 가능합니다.)

