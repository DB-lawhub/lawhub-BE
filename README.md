# lawhub-BE

데이터베이스설계 프로젝트 'LawHub' 백엔드 레포지토리

## 프로젝트 설명
자영업자가 알아야 할 지출 계산 서비스<br/>
자신의 사업 등록을 하면, 관련 법률에 의한 세금 및 지출이 자동으로 계산된다!<br/>
(모든 법률은 2024년 기준으로 설정되었습니다.)<br/>

## 주요 앱
- accounts (사용자)
- business (사업)
- employee (직원)
- tax (세금)

### 1. accounts 앱
- django에서 제공하는 auth의 User 모델을 가져와 사용
- db에 저장된 user 정보를 입력하면 refresh token과 access token 반환
- login/logout 기능 존재

### 2. business 앱
- 사업에 관련된 데이터 관리
  - `Business(사업)` 테이블, `Revenue(사업 수익)` 테이블

### 3. employee 앱
---
근로기준법<br/>
최저임급법<br/>
고용보호법<br/>
산업재해보상보험법<br/>
국민건강보험법<br/>
국민연금법<br/>
---
- 직원에 관련된 데이터 관리
    - `Employee(직원)` 테이블, `EmployeeSalary(직원 급여)` 테이블, `EmployeeTax(직원 세금)` 테이블<br/>

- EmployeeSalary
    - `Employee` 테이블에 입력된 직원의 월급 혹은 시급과 주 근무시간으로 급여 자동 계산<br/>

- EmployeeTax
    - 만약 직원이 4대보험에 가입되어 있다면, 자영업자가 부담해야 할 4대보험금 계산
    - 4대보험 가입자인 경우 테이블 자동 생성
    - `Business` 테이블에 있는 `business_type(업종)`에 따른 산재보험료율 상이
    - 3.3%를 뗄 시에는 자영업자 부담 x<br/>

### 4. tax 앱
---
부가가치세법<br/>
소득세법<br/>
법인세법<br/>
상가건물임대차보호법<br/>
---
- 세금에 관련된 데이터 관리
    - `VAT(부가가치세)` 테이블, `IncomeTax(종합소득세)` 테이블, `CorporateTax(법인세)` 테이블, `Rental(임대료)` 테이블<br/>

- VAT
    - 일반과세자/간이과세자에 따른 부가가치세 계산 차이
    - 일반과세자 납부세액: **(매출액 x 10%) - (매입액 x 10%) - 공제세액**
    - 간이과세자일경우 `Business` 테이블에 있는 `business_type(업종)`에 따른 부가가치율 상이
    - 간이과세자 납부세액: **(매출액 x 업종별 부가가치율 x 10%) - (매입액 x 0.5%)**<br/>

- IncomeTax
    - 개인/법인에 따라 종합소득세/법인세 중 하나만 납부
    - 과세표준에 따른 세율 및 누진공제 상이
    - 납부세액: **과세표준(종합소득금액 - 소득공제) * 과세표준에 따른 세율 - 세액공제**<br/>

- CorporateTax
    - 법인으로 등록된 모든 사업체 해당
    - 과세표준에 따른 세율 및 누진공제 상이
    - 납부세액: **(법인 순이익 x 과세표준에 따른 세율) - 공제 및 감면액**<br/>

- Rental
    - 임대료: **보증금 + 월세(관리비 별도)**

## 실행 방법
1. 가상환경 생성
```commandline
python -m venv venv
source venv/Scripts/activate
```

2. 의존성 모듈 설치
```commandline
pip install -r requirements.txt
```

3. 실행
```commandline
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
