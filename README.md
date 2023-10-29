# SRT 예약하기

## 설치

1. python, Chrome<br/>
   python과 Chrome으로 동작하므로 둘 모두 설치되어 있어야 한다.

2. 필요한 패키지 설치하기<br/>
   ```bash
   pip install -r requirements.txt
   ```
   <br/>

## 설정

1. settings.py 파일을 수정한다.
	```python
	SRT_INFO = {
		'ID'    : '회원번호',		# 문자열 형식
		'PW'    : '비밀번호',		# 문자열 형식
		'FROM'  : '동탄',		# 문자열 형식, 출발지
		'TO'    : '동대구',		# 문자열 형식, 도착지
		'DATE'  : 20231015,		# 숫자, 조회날짜
		'TIME'  : 18			# 숫자, 조회시간
	}
	GMAIL_INFO = {
		'ID': 'Gmail 주소',	    # 문자열 형식
		'PW': '비밀번호'		    # 문자열 형식
	}
	```
2. gmail 설정<br/>
   1. gmail 접속 후 우측 상단의 톱니바퀴 → 모든 설정 보기 클릭<br/>
      ![IMG1](README/1.png)
   2. 전달 및 POP/IMAP → IMAP 사용 체크 → 변경사항 저장<br/>
      ![IMG2](README/2.png)

<br/>

## 실행

1. settings.py파일의 정보를 확인한다.<br/>
   값의 형식에 맞게 작성한다.<br/>
   조회시간은 홈페이지에 나와있는 시간 중에서 선택한다.
2. searchTrain()함수의 while문 안에 있는 for문의 시작 숫자를 변경한다.<br/>
   ex) 첫번째부터 예매하고 싶다면 1, 세번째부터 예매하고 싶다면 3<br/>
   현재는 세번째부터 확인하도록 3으로 되어있다.<br/>
   `for i in range(3, 3 + trainToCheckNum):`
3. searchTrain()함수의 trainToCheckNum값을 원하는 값으로 변경한다.<br/>
   ex) 두개를 확인하고 싶다면 2
   현재는 3번째부터 2개를 확인할거라서 2로 되어있다.<br/>
   `int, trainToCheckNum = 2`
4. `ReservationSRT.py`파일을 실행한다.
   ```bash
   python ReservationSRT.py
   ```

<br/>

## 설명

- SRT가 예약되면 설정한 Gmail로 메일이 보내진다.
- 실행중인 기기에서 알림소리가 울린다. 알림소리는 `Enter`를 입력해야 꺼진다.
- 결제는 10분 이내로 완료해야 한다.
