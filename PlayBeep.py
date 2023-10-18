import winsound
import threading

def beepsound():
    while True:
        fr = 2000
        du = 500
        winsound.Beep(fr, du)

def repeatBeepSound():
    soundThread = threading.Thread(target=beepsound)
    soundThread.daemon = True
    soundThread.start()

    input("예매 성공, 결제 요망\nEnter키를 눌러 종료")


repeatBeepSound()