from gpiozero import MotionSensor, LED
from time import sleep, time
from sys import exit
import serial
import threading


# Raspberry Pi GPIO pin config
sensor = MotionSensor(14)

# Modem configuration
device = '/dev/ttyUSB2'
message = 'motion detected'
phone_number = '4124456289'
sms_timeout = 120 # min seconds between SMS messages


def setup():
    port.close()

    try:
        port.open()
    except serial.SerialException as e:
        print('Error opening device: ' + str(e))
        return False

    # Turn off echo mode
    port.write(b'ATE0 \r')
    if not check_response('OK', 10):
        print('Failed on ATE0')
        return False

    # Enter SMS text mode
    port.write(b'AT+CMGF=1 \r')
    if not check_response('OK', 6):
        print('Failed on CMGF')
        return False

    # Switch character set to 'international reference alphabet'
    # Note: this still doesn't support all characters
    port.write(b'AT+CSCS="IRA" \r')
    if not check_response('OK', 6):
        print('Failed on CSCS')
        return False

    return True


def check_response(string, amount):
    result = ''

    try:
        result = port.read(amount).decode()
    except:
        return False

    if not string in result:
        try:
            # Write 'ESC' to exit SMS input mode, just in case
            port.write(b'\x1B \r')
        except:
            return False

    return string in result


# def send_sms():
#     global currently_sending, last_msg_time
#     currently_sending = True

#     try:
#         port.write('AT+CMGS="{}" \r'.format(phone_number).encode())
#         if not check_response('>', 6):
#             print('Failed on CMGS')
#             currently_sending = False
#             return

#         # Write the message terminated by 'Ctrl+Z' or '1A' in ASCII
#         port.write('{}\x1A \r'.format(message).encode())

#         while True:
#             result = port.readline().decode()

#             if 'OK' in result:
#                 print('> SMS sent successfully')
#                 last_msg_time = time()
#                 currently_sending = False
#                 return

#             if 'ERROR' in result:
#                 print('> Failed to send SMS [{}]'.format(result.rstrip()))
#                 currently_sending = False
#                 return
#     except:
#         # Initiate setup if the got while the program was running
#         setup()
#         currently_sending = False


def on_motion():
    print('Motion detected!')

    # if time() - last_msg_time > sms_timeout and not currently_sending:
    #     print('> Sending SMS...')
    #     threading.Thread(target=send_sms).start()


def no_motion():
    print("motion")


print('* Setting up...')


port = serial.Serial()
port.port = device
port.baudrate = 115200
port.timeout = 2

# last_msg_time = 0
# currently_sending = False

if not setup():
    print('* Retrying...')
    if not setup():
        print('* Try restarting the modem')
        exit(1)

print('* Do not move, setting up the PIR sensor...')
sensor.wait_for_no_motion()

print('* Device ready! ', end='', flush=True)


sensor.when_motion = on_motion
sensor.when_no_motion = no_motion
input('Press Enter or Ctrl+C to exit\n\n')