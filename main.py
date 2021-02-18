# App's Imports
import config

# Kivy Imports for GUI Building
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.toast import toast
from kivymd.theming import ThemeManager
from kivy.clock import Clock
from kivy.graphics.texture import Texture

# Other Imports
from time import asctime, localtime, time, sleep
import threading
import socket
import struct
import pickle
from random import randint
from functools import partial

# Cryptology
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
# ###########################################################################


# Configs and Variables #####################################################
__version__ = "2.0.0"  # For buildozer
waiting_conf = []
process_list = []
Window.size = config.WINDOW_SIZE
process_list = []
car_status = 0
light_status = 0
tempshield_status = 0
jammer_status = 0
engine_status = [0, 0]  # First variable represent back and forward by -1 and 1 variables. Second one takes angle.
# These variables are necessary because every wrong connection try by trying to access by using user_name and password
# close the connection and for the next try we connect again with new keyPair and n_rasp and also new connection socket.
connection = None
mobile_keys = None
public_rasp = None
_PORT = 0
_IP_ADDR = ""
isUser = False
# ###########################################################################


# General Functions #########################################################
def type_conversion(to_convert, conversion_type=True):
    # conversion_type's:
    # True -> name to code
    # False -> code to name
    # Strings to Bytes
    if conversion_type:
        if to_convert is "ERROR":
            return b'000'
        elif to_convert is "INFO":
            return b'001'
        elif to_convert is "START":
            return b'010'
        elif to_convert is "STOP":
            return b'011'
        elif to_convert is "CLIENT":
            return b'100'
        elif to_convert is "CONF":
            return b'101'
        else:
            return b'111'
    # Bytes to Strings
    else:
        if to_convert == b'000':
            return "ERROR"
        elif to_convert == b'001':
            return "INFO"
        elif to_convert == b'010':
            return "START"
        elif to_convert == b'011':
            return "STOP"
        elif to_convert == b'100':
            return "CLIENT"
        elif to_convert == b'101':
            return "CONF"
        else:
            return "OPS!"


def throw(msg_type, message, conn=None, is_toasted=True):
    logfile = open(f"{config.LOGFILE}.log", "a")
    _time = asctime(localtime(time()))
    if conn:
        print(f"[{msg_type}]\t{message} ({conn})")
        logfile.write(f"[{msg_type}][{_time}]\t{message} ({conn}\n")
        if is_toasted:
            toast(f"[{msg_type}]\t{message} ({conn})")
    else:
        print(f"[{msg_type}]\t{message}")
        logfile.write(f"[{msg_type}][{_time}]\t{message}\n")
        if is_toasted:
            toast(f"[{msg_type}]\t{message}")
    logfile.close()


def message_converter(message, conversion_type=True, conversion_data="none"):
    # conversion_type Usage
    # true for name -> converted
    # false for converted -> name
    # ----------------------------------
    #   Message Name    |     Converted
    # tempshield_status |       000
    # jammer_status     |       001
    # light_status      |       010
    # car_status        |       011
    # !dis              |       111
    # direction_angle   |       100
    # direction         |       101
    # confirmation      |       110
    # ----------------------------------
    #     Values        |     Converted
    # False             | 00000
    # True              | 00001
    # forward           | 00010
    # backward          | 00011
    # stop              | 00100
    # 1                 | 00101
    # 2                 | 00110
    # 3                 | 00111
    # 4                 | 01000
    # 5                 | 01001
    # 6                 | 01010
    # 7                 | 01011
    # 8                 | 01100
    # 9                 | 01101
    # 10                | 01110
    # 11                | 01111
    # 12                | 10000
    # 13                | 10001
    # 14                | 10010
    # 15                | 10011
    # 16                | 10100
    # empty-            | 10101
    # empty-            | 10110
    # empty-            | 10111
    # empty-            | 11000
    # empty-            | 11001
    # empty-            | 11010
    # empty-            | 11011
    # empty-            | 11100
    # empty-            | 11101
    # empty-            | 11110
    # empty-            | 11111
    if conversion_data == "none":
        if not message:
            throw("ERROR", f"Message converter can't handle {message}", "")
            return message
        else:
            # Strings to Bytes
            if conversion_type:
                message = message.split("/")

                # Message Type
                if message[0] == "tempshield_status":
                    message[0] = b'000'
                elif message[0] == "jammer_status":
                    message[0] = b'001'
                elif message[0] == "light_status":
                    message[0] = b'010'
                elif message[0] == "car_status":
                    message[0] = b'011'
                elif message[0] == "direction_angle":
                    message[0] = b'100'
                elif message[0] == "direction":
                    message[0] = b'101'
                elif message[0] == "!dis":
                    message[0] = b'111'
                elif message[0] == "Confirmation":
                    message[0] = b'110'
                else:
                    throw("ERROR", f"Message Type can not be understood.", "")

                # Message Value
                if message[1] == "False":
                    message[1] = b'00000'
                elif message[1] == "True":
                    message[1] = b'00001'
                elif message[1] == "forward":
                    message[1] = b'00010'
                elif message[1] == "backward":
                    message[1] = b'00011'
                elif message[1] == "stop":
                    message[1] = b'00100'
                elif message[1] == "1":
                    message[1] = b'00101'
                elif message[1] == "2":
                    message[1] = b'00110'
                elif message[1] == "3":
                    message[1] = b'00111'
                elif message[1] == "4":
                    message[1] = b'01000'
                elif message[1] == "5":
                    message[1] = b'01001'
                elif message[1] == "6":
                    message[1] = b'01010'
                elif message[1] == "7":
                    message[1] = b'01011'
                elif message[1] == "8":
                    message[1] = b'01100'
                elif message[1] == "9":
                    message[1] = b'01101'
                elif message[1] == "10":
                    message[1] = b'01110'
                elif message[1] == "11":
                    message[1] = b'01111'
                elif message[1] == "12":
                    message[1] = b'10000'
                elif message[1] == "13":
                    message[1] = b'10001'
                elif message[1] == "14":
                    message[1] = b'10010'
                elif message[1] == "15":
                    message[1] = b'10011'
                elif message[1] == "16":
                    message[1] = b'10100'
                else:
                    throw("ERROR", f"Message value can not be understood.", "")
                return message
            # If conversion_type == False
            # Bytes to Strings
            else:
                if message[0] == b'000':
                    message[0] = "tempshield_status"
                elif message[0] == b'001':
                    message[0] = "jammer_status"
                elif message[0] == b'010':
                    message[0] = "light_status"
                elif message[0] == b'011':
                    message[0] = "car_status"
                elif message[0] == b'100':
                    message[0] = "direction_angle"
                elif message[0] == b'101':
                    message[0] = "direction"
                elif message[0] == b'111':
                    message[0] = "!dis"
                elif message[0] == b'110':
                    message[0] = "Confirmation"
                else:
                    throw("ERROR", f"Message Type can not be understood.", "")

                # Message Value
                if message[1] == b'00000':
                    message[1] = "False"
                elif message[1] == b'00001':
                    message[1] = "True"
                elif message[1] == b'00010':
                    message[1] = "forward"
                elif message[1] == b'00011':
                    message[1] = "backward"
                elif message[1] == b'00100':
                    message[1] = "stop"
                elif message[1] == b'00101':
                    message[1] = "1"
                elif message[1] == b'00110':
                    message[1] = "2"
                elif message[1] == b'00111':
                    message[1] = "3"
                elif message[1] == b'01000':
                    message[1] = "4"
                elif message[1] == b'01001':
                    message[1] = "5"
                elif message[1] == b'01010':
                    message[1] = "6"
                elif message[1] == b'01011':
                    message[1] = "7"
                elif message[1] == b'01100':
                    message[1] = "8"
                elif message[1] == b'01101':
                    message[1] = "9"
                elif message[1] == b'01110':
                    message[1] = "10"
                elif message[1] == b'01111':
                    message[1] = "11"
                elif message[1] == b'10000':
                    message[1] = "12"
                elif message[1] == b'10001':
                    message[1] = "13"
                elif message[1] == b'10010':
                    message[1] = "14"
                elif message[1] == b'10011':
                    message[1] = "15"
                elif message[1] == b'10100':
                    message[1] = "16"
                else:
                    throw("ERROR", f"Message value can not be understood.", "")
                return message
    # Strings to Bytes
    elif conversion_data == "type" and conversion_type is True:
        if message == "tempshield_status":
            message = b'000'
        elif message == "jammer_status":
            message = b'001'
        elif message == "light_status":
            message = b'010'
        elif message == "car_status":
            message = b'011'
        elif message == "direction_angle":
            message = b'100'
        elif message == "direction":
            message = b'101'
        elif message == "!dis":
            message = b'111'
        elif message == "Confirmation":
            message = b'110'
        else:
            throw("ERROR", f"Message Type can not be understood.", "")
        return message
    # Bytes to Strings
    elif conversion_data == "type" and conversion_type is False:
        if message == b'000':
            message = "tempshield_status"
        elif message == b'001':
            message = "jammer_status"
        elif message == b'010':
            message = "light_status"
        elif message == b'011':
            message = "car_status"
        elif message == b'100':
            message = "direction_angle"
        elif message == b'101':
            message = "direction"
        elif message == b'111':
            message = "!dis"
        elif message == b'110':
            message = "Confirmation"
        else:
            throw("ERROR", f"Message Type can not be understood.", "")
        return message
    # Strings to Bytes
    elif conversion_data == "value" and conversion_type is True:
        if message == "False":
            message = b'00000'
        elif message == "True":
            message = b'00001'
        elif message == "forward":
            message = b'00010'
        elif message == "backward":
            message = b'00011'
        elif message == "stop":
            message = b'00100'
        elif message == "1":
            message = b'00101'
        elif message == "2":
            message = b'00110'
        elif message == "3":
            message = b'00111'
        elif message == "4":
            message = b'01000'
        elif message == "5":
            message = b'01001'
        elif message == "6":
            message = b'01010'
        elif message == "7":
            message = b'01011'
        elif message == "8":
            message = b'01100'
        elif message == "9":
            message = b'01101'
        elif message == "10":
            message = b'01110'
        elif message == "11":
            message = b'01111'
        elif message == "12":
            message = b'10000'
        elif message == "13":
            message = b'10001'
        elif message == "14":
            message = b'10010'
        elif message == "15":
            message = b'10011'
        elif message == "16":
            message = b'10100'
        else:
            throw("ERROR", f"Message value can not be understood.", "")
        return message
    # Bytes to Strings
    elif conversion_data == "value" and conversion_type is False:
        if message == b'00000':
            message = "False"
        elif message == b'00001':
            message = "True"
        elif message == b'00010':
            message = "forward"
        elif message == b'00011':
            message = "backward"
        elif message == b'00100':
            message = "stop"
        elif message == b'00101':
            message = "1"
        elif message == b'00110':
            message = "2"
        elif message == b'00111':
            message = "3"
        elif message == b'01000':
            message = "4"
        elif message == b'01001':
            message = "5"
        elif message == b'01010':
            message = "6"
        elif message == b'01011':
            message = "7"
        elif message == b'01100':
            message = "8"
        elif message == b'01101':
            message = "9"
        elif message == b'01110':
            message = "10"
        elif message == b'01111':
            message = "11"
        elif message == b'10000':
            message = "12"
        elif message == b'10001':
            message = "13"
        elif message == b'10010':
            message = "14"
        elif message == b'10011':
            message = "15"
        elif message == b'10100':
            message = "16"
        else:
            throw("ERROR", f"Message value can not be understood.", "")
        return message
# ###########################################################################


# Networking Functions ######################################################
def try_to_connect(ip, port):
    isError = False
    _connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        _connection.connect((ip, port))
    except OSError as error:
        if error.errno == 111:
            throw("INFO", f"Connection refused. Try to check the data you provided.", is_toasted=True)
        else:
            throw("ERROR", error)
        isError = True
    except OverflowError:
        throw("INFO", f"Connection refused. Try to check the data you provided.", is_toasted=True)
        isError = True

    if isError:
        return False, False, False, False
    
    _key_pair = RSA.generate(2048)
    _public_mobile = _key_pair.publickey().export_key()
    _connection.sendto(_public_mobile, (ip, port))
    _public_rasp = _connection.recv(512)

    return True, _connection, _key_pair, _public_rasp


def encrypt(message_to_send):
    # Used rasp's n-value and standart publickey e=65537 for encryption.
    public_key_rasp = RSA.import_key(public_rasp)
    encryptor = PKCS1_OAEP.new(public_key_rasp)
    message_to_send = encryptor.encrypt(message_to_send)
    return message_to_send


def decrypt(received_data):
    private_key_mobile = RSA.import_key(mobile_keys.export_key())
    decryptor = PKCS1_OAEP.new(private_key_mobile)
    received_data = decryptor.decrypt(received_data)
    return received_data


def receive():
    try_attempt = 0
    global process_list
    while True:
        try:
            data = connection.recv(512)
            if data:
                try:
                    data = decrypt(data)
                except Exception as error:
                    print(error)
                    continue
                throw("INFO", f"Received! {data}", "", is_toasted=False)
            if not data:
                if data == b'':
                    try_attempt += 1
                    if try_attempt == 1000:
                        connection.close()
                        throw("ERROR", "Connection lost with server. You must restart the app.", "")
                        exit()

                continue
            # message: [message code, message type, data type, data]
            message = [data[0:5], type_conversion(data[5:8], False), data[8:11], data[11:17]]

            if message[1] is "CONF":
                for item in process_list:
                    if int(message[0]) == item["conf"]:
                        threading.Thread(target=process, args=("in", item["type"], item["value"])).start()
                        process_list.remove(item)

            else:
                # Process adding to list
                process_list.append({
                    "conf": int(message[0]),
                    "type": message_converter(message[2], False, "type"),
                    "value": message_converter(message[3], False, "value")
                     })
                
                print(process_list)

                # Sending confirmation message
                type_code = type_conversion("CONF")
                conf_message = message[0] + type_code + b'110' + b'00001'
                conf_message = encrypt(conf_message)
                thread_conf = threading.Thread(target=connection.send, args=(conf_message,), daemon=True)
                thread_conf.start()

        except ConnectionResetError:
            throw("ERROR", f"Connection closed by the server.", "")
            connection.close()
            break
        except Exception as error:
            throw("ERROR", error, "")
            connection.close()
            break


def send(message):
    # example usage: send("temp_status/True")
    # Message Template - there are no blanks: message-code message-type data-type  data
    #                                            5 byte        3 byte    3 byte   5 byte
    c_message = randint(11111, 99999)

    if message == "!dis":
        c_type = type_conversion("CLIENT")
        message = message_converter(message, conversion_data="type")
        message = f"{c_message}".encode(config.FORMAT) + c_type + message
        message = encrypt(message)

    else:
        c_type = type_conversion("INFO")
        message = message_converter(message)
        process_list.append({
            "conf": int(c_message),
            "type": message_converter(message[0], False, "type"),
            "value": message_converter(message[1], False, "value")
        })
        message = f"{c_message}".encode(config.FORMAT) + c_type + message[0] + message[1]
        message = encrypt(message)
    # Sending message via thread
    thread_input = threading.Thread(target=connection.send, args=(message,), daemon=True)
    thread_input.start()
    return True
# ###########################################################################


# GPIO Functions ############################################################
def process(opt, sett, val):
    global tempshield_status, car_status, jammer_status, light_status, engine_status
    throw("INFO", f"{sett} {val}", "", is_toasted=False)

    if opt == "in":
        if sett == "tempshield_status":
            if val == "True":
                tempshield_status = True
                toast("Temperature shield is activated.")
                return True
            elif val == "False":
                tempshield_status = False
                toast("Temperature shield is deactivated.")
                return True
            else:
                return False
        elif sett == "jammer_status":
            if val == "True":
                jammer_status = True
                toast("Jammer is activated.")
                return True
            elif val == "False":
                jammer_status = False
                toast("Jammer is deactivated.")
                return True
            else:
                return False
        elif sett == "light_status":
            if val == "True":
                light_status = True
                toast("Lights are activated.")
                return True
            elif val == "False":
                light_status = False
                toast("Lights are deactivated.")
                return True
            else:
                return False
        elif sett == "car_status":
            if val == "True":
                car_status = True
                toast("Engine started.")
                return True
            elif val == "False":
                car_status = False
                toast("Engine stopped.")
                return True
            else:
                return False


def update_data():
    global process_list
    # This function is running background within a thread.
    # To update sidebar datas per half second.
    while True:
        if len(process_list) > 0:
            for item in process_list:
                # car_status
                if item["type"] == "car_status":
                    if item["value"] == "True":
                        throw("INFO", "Engine started.")
                    elif item["value"] == "False":
                        throw("INFO", "Engine stopped.")
                    else:
                        throw("ERROR", "Something wrong with the process list.")
                
                # light_status
                if item["type"] == "light_status":
                    if item["value"] == "True":
                        throw("INFO", "Lights are activated.")
                    elif item["value"] == "False":
                        throw("INFO", "Lights are deactivated.")
                    else:
                        throw("ERROR", "Something wrong with the process list.")
                
                # tempshield_status
                if item["type"] == "tempshield_status":
                    if item["value"] == "True":
                        throw("INFO", "Temperature shield is activated.")
                    elif item["value"] == "False":
                        throw("INFO", "Temperature shield is deactivated.")
                    else:
                        throw("ERROR", "Something wrong with the process list.")

                # jammer_status
                if item["type"] == "jammer_status":
                    if item["value"] == "True":
                        throw("INFO", "Jammer is activated.")
                    elif item["value"] == "False":
                        throw("INFO", "Jammer is deactivated.")
                    else:
                        throw("ERROR", "Something wrong with the process list.")
                process_list.remove(item)
        sleep(0.5)
# ###########################################################################


# Screens ###################################################################
class MainWindow(Screen):

    def login(self):
        global connection, mobile_keys, public_rasp
        global _IP_ADDR, _PORT, isUser

        # Reading textboxes
        username = self.ids.usernameID.text.split("@")[0]
        _IP_ADDR = self.ids.usernameID.text.split("@")[1].split(":")[0]
        _PORT = int(self.ids.usernameID.text.split("@")[1].split(":")[1])
        password = self.ids.passwordID.text

        # Sending the user information
        status, connection, mobile_keys, public_rasp = try_to_connect(_IP_ADDR, _PORT)

        if status:
            connection.send(encrypt(
                bytes(username + "/" + password, config.FORMAT)
                ))

            # Receiving the connection status
            data = connection.recv(512)
            data = decrypt(data)
            if data == b'01':
                isUser = True
                # Receiving
                reciever_thread = threading.Thread(target=receive, daemon=True)
                reciever_thread.start()
                return 0
            elif data == b'00':
                isUser = False
                self.ids.usernameID.text = ""
                self.ids.passwordID.text = ""
                toast("Wrong password or username. Try again.")
                return 1
        else:
            _PORT = 0
            return 1


class AdminPanel(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        video_thread = threading.Thread(target=self.camera_receiver, daemon=True)
        video_thread.start()
        update_thread = threading.Thread(target=update_data, daemon=True)
        update_thread.start()

    def change_frame(self, frame, dt): 
        # create a Texture the correct size and format for the frame
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        # copy the frame data into the texture
        texture.blit_buffer(frame.tobytes(order=None), colorfmt='bgr', bufferfmt='ubyte')
        texture.flip_vertical()
        self.ids.live_photo.texture = texture

    def camera_receiver(self):
        global _PORT, _IP_ADDR, isUser

        data = b''
        payload_size = struct.calcsize("Q")
        waited_cycle = 0  # waited_cycle is the variable that holds cycles for connection tries.
        connection_camera = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connecting to the server with CONFIG details.
        # If port is closed, it'll give you a error and
        # try the next one.
        while True:
            port_bind = _PORT + 100
            if _PORT > 100 and isUser:
                try:
                    connection_camera.connect((_IP_ADDR, port_bind))
                    break
                except ConnectionRefusedError as error:
                    throw("INFO", "Connection refused. Please check your ip address and port.", is_toasted=True)
            sleep(0.05)

        while True:
            # Receiving enough bytes to understand frame's length.
            # Payload_size is the size of message which will tell us the size of frame.
            while len(data) < payload_size:
                packet = connection_camera.recv(4*1024)  # 4KiB data receiving
                if not packet:
                    waited_cycle += 1
                    if waited_cycle >= 1000:
                        print("[SYSTEM] Connection went down. Restart the application. Exiting.")
                        connection_camera.close()
                        exit(0)
                    continue
                data += packet

            # Unpacking frame's size, which is data[:payload_size], with struct module.
            frame_size_packed = data[:payload_size]
            frame_size = struct.unpack("Q", frame_size_packed)[0]
            data = data[payload_size:]  # Eliminating the frame size from received message.

            # Receiving message and combine it with older ones if there's space to frame_size.
            while len(data) < frame_size:
                data += connection_camera.recv(4*1024)

            # Selecting the frame from data with frame_size length.
            # We need to assign the remaining bytes to data for combining
            # with new ones received.
            frame = data[:frame_size]
            data = data[frame_size:]

            # Unpacking the frame with pickle module.
            frame = pickle.loads(frame)

            # Printing the frame
            Clock.schedule_once(partial(self.change_frame, frame))

    def temp_shield_toggle(self):
        global tempshield_status
        msg_code = send(f"tempshield_status/{not tempshield_status}")
        if not msg_code:
            throw("ERROR", "[1] Sending tempshield_status data failed!", "")
            return False
        if tempshield_status is not True:
            self.ids.temp_shield_toggle_icon.icon = "layers"
            tempshield_status = not tempshield_status
        else:
            self.ids.temp_shield_toggle_icon.icon = "layers-off"
            tempshield_status = not tempshield_status
        return True

    def jammer_toggle(self):
        global jammer_status
        msg_code = send(f"jammer_status/{not jammer_status}")
        if not msg_code:
            throw("ERROR", "[2] Sending jammer_status data failed!", "")
            return False
        if jammer_status is not True:
            self.ids.jammer_toggle_icon.icon = "access-point-network"
            jammer_status = not jammer_status
        else:
            self.ids.jammer_toggle_icon.icon = "access-point-network-off"
            jammer_status = not jammer_status
        return True

    def car_light_toggle(self):
        global light_status
        msg_code = send(f"light_status/{not light_status}")
        if not msg_code:
            throw("ERROR", "[3] Sending light_status data failed!", "")
            return False
        if light_status is not True:
            self.ids.car_light_toggle_icon.icon = "car-light-high"
            light_status = not light_status
        else:
            self.ids.car_light_toggle_icon.icon = "car-light-fog"
            light_status = not light_status
        return True

    def car_engine_startstop(self):
        global car_status
        msg_code = send(f"car_status/{not car_status}")
        if not msg_code:
            throw("ERROR", "[4] Sending car_status data failed!", "")
            return False
        if car_status is not True:
            self.ids.car_engine_startstop_icon.icon = "engine"
            car_status = not car_status
        else:
            self.ids.car_engine_startstop_icon.icon = "engine-off"
            car_status = not car_status
        return True

    @staticmethod
    def quit():
        send("!dis")
        connection.close()
        throw("INFO", "Connection closed. You can close the app now.", "")
        exit()


class WinManager(ScreenManager):
    pass
# ###########################################################################


# App Settings ##############################################################
class MainApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls = ThemeManager()
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_hue = "500"
        self.title = "IUC Thermoelectricity Laboratory"

    def build(self):
        self.root = Builder.load_file("template.kv")
        joystick = self.root.ids.apanel.ids.directionjoystick
        joystick.bind(pad=self.joystick_direction)
        return 0

    # engine_status variable in the function necessary to know old data.
    # Direction has been handing here and will control motors in server.
    # x, y in x axis and y axis. a is angle which stars with x axis.
    @staticmethod
    def joystick_direction(instance, pad):
        sleep(0.005)
        x, y = pad
        x, y = (str(x)[0:4], str(y)[0:4])
        a = int(instance.angle / 10)
        # Sending the angle - after 180* degree, it'll show 0 to 180 again.
        # It means that third and fourth region in coordinate plane will be start
        # with zero.
        # Ex. 190* turns 10*, 340* turns 160
        if 4 <= a <= 14 and engine_status[1] is not a and engine_status[0] is not 0:
            if send(f"direction_angle/{a}"):
                engine_status[1] = a
            else:
                throw("ERROR", "[C5] Sending forward direction_angle data failed!", "")
        elif 32 >= a >= 22 and engine_status[1] is not (36-a) and engine_status[0] is not 0:
            a = 36 - a
            if send(f"direction_angle/{a}"):
                engine_status[1] = a
            else:
                throw("ERROR", "[C6] Sending backward direction_angle data failed!", "")

        # Sending the power - forward, backward or stop
        if float(y) >= 0.64 and engine_status[0] is not 1:
            if send("direction/forward"):
                engine_status[0] = 1
            else:
                throw("ERROR", "[C7] Sending forward direction data failed.", "")
        elif float(y) <= -0.64 and engine_status[0] is not -1:
            if send("direction/backward"):
                engine_status[0] = -1
            else:
                throw("ERROR", "[C8] Sending backward direction data failed.", "")
        elif -0.64 < float(y) < 0.64 and engine_status[0] is not 0:
            if send("direction/stop"):
                engine_status[0] = 0
            else:
                throw("ERROR", "[C9] Sending stop direction data failed.", "")


if __name__ == "__main__":

    # Starting the App
    MainApp().run()
