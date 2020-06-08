import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)

#모터 상태
STOP=0
FORWARD=1
BACKWARD=2

#모터 채널
CH1=0
CH2=1

#핀 번
ENA=26
ENB=0
IN1=19 #왼쪽바퀴 앞으로
IN2=13 #왼쪽바퀴 뒤로
IN3=6 #오른쪽바퀴 앞으로
IN4=5 #오른쪽바퀴 뒤로


#핀설정
def setPinConfig(EN, INA, INB):
    GPIO.setup(EN, GPIO.OUT) #EN핀을 출력으로
    GPIO.setup(INA, GPIO.OUT) #IN핀을 출력으로 설정
    GPIO.setup(INB, GPIO.OUT)
    pwm=GPIO.PWM(EN, 100) #100khz(주파수)로 PWM 동작
    pwm.start(0) #초기값 설정(듀티사이클)/우선 멈
    return pwm

#모터 제어함수2(모터 제어함수1 한번 더 감쌈)
def setMotor(ch, speed, stat):
    if ch==CH1:
        setMotorControl(pwmA, IN1, IN2, speed, stat)
    else:
        setMotorControl(pwmB, IN3, IN4, speed, stat)

#모터 제어함수1
def setMotorControl(pwm, INA, INB, speed,stat):
    GPIO.output(ENA, GPIO.HIGH)
    GPIO.output(ENB, GPIO.LOW)
    pwm.ChangeDutyCycle(speed) #pwm 출력값(속도) 조절
    if stat==FORWARD:
        GPIO.output(INA, GPIO.HIGH)
        GPIO.output(INB, GPIO.LOW)
    elif stat==BACKWARD:
        GPIO.output(INA, GPIO.LOW)
        GPIO.output(INB, GPIO.HIGH)
    elif stat==STOP:
        GPIO.output(INA, GPIO.LOW)
        GPIO.output(INB, GPIO.LOW)
        
#좌회전
def left(speed):
    #왼쪽 바퀴 
    setMotor(CH2, 0, STOP)
    #오른쪽 바퀴 제어
    setMotor(CH1, speed, FORWARD)

#우회전
def right(speed) : 
        setMotor(CH1, 0, STOP)
        setMotor(CH2, speed, FORWARD)

pwmA=setPinConfig(ENA, IN1, IN2) #핀들을 모두 출력으로 설정 후 멈춰
pwmB=setPinConfig(ENB, IN3, IN4)

setMotor(CH1, 100, FORWARD) #앞으로 80프로 속도
setMotor(CH2, 100, FORWARD)
sleep(2.5)
right(100) #우회전
sleep(2.2)
setMotor(CH1, 80, FORWARD)
setMotor(CH2, 80, FORWARD)
sleep(2.5)
left(100) #좌회전
sleep(2.2)
setMotor(CH1, 80, FORWARD)
setMotor(CH2, 80, FORWARD)
sleep(2.5)
setMotor(CH1, 0, STOP)
setMotor(CH2, 0, STOP)
sleep(1)

GPIO.cleanup() #종료

