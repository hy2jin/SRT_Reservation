import argparse
import smtplib
import settings
from email.message import EmailMessage

def main(count):
    # STMP 서버의 url과 port 번호
    SMTP_SERVER = 'smtp.gmail.com'  # GMAIL smtp 주소
    SMTP_PORT = 465                 # GMAIL smtp 포트 번호 (고정, 변경불가)

    # 1. SMTP 서버 연결
    smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)

    EMAIL_ADDR = settings.GMAIL_INFO['ID']
    EMAIL_PASSWORD = settings.GMAIL_INFO['PW']

    # 2. SMTP 서버에 로그인
    smtp.login(EMAIL_ADDR, EMAIL_PASSWORD)

    # 3. MIME 형태의 이메일 메세지 작성
    message = EmailMessage()
    message["Subject"] = "SRT 예매 완료, 결제 요망"
    message["From"] = EMAIL_ADDR
    message["To"] = EMAIL_ADDR
    content = f"{count}회 시도 끝에 SRT 예매 성공"
    message.set_content(content)

    # 4. 서버로 메일 보내기
    smtp.send_message(message)

    # 5. 메일을 보내면 서버와의 연결 끊기
    smtp.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, help="Count value to pass to main function")
    args = parser.parse_args()

    if args.count is not None:
        main(args.count)