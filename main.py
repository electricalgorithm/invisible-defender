# App's Imports
from config import *
from utils import *

# Kivy Imports for GUI Building
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.theming import ThemeManager
from kivy.clock import Clock
from kivy.graphics.texture import Texture

# Other Imports
from time import sleep
import threading
import socket
import struct
import pickle
from random import randint
from functools import partial

# Cryptology
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Hash import SHA256

# Version Information
__version__ = "2.0.7"


class MainWindow(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # We're creating RSA here as a thread because of speed reasons.
        threading.Thread(target=self.init_rsa, daemon=True).start()

    @staticmethod
    def init_rsa():
        """
        Creates a RSA object for first encryption.
        :return: None
        """
        # Creating key pair for RSA protocol.
        App.key_pair = RSA.generate(2048)
        # Assigning public key for mobile
        App.public_key = App.key_pair.publickey().export_key()

    def login(self):
        """
        Callback function for "Log In" button.
        Note: is_connected attribute is for camera_receiver function.
        :return: Boolean
        """
        try:
            username = self.ids.usernameID.text.split("@")[0]
            App.conn_ip_addr = self.ids.usernameID.text.split("@")[1].split(":")[0]
            App.conn_port = int(self.ids.usernameID.text.split("@")[1].split(":")[1])
            password = self.ids.passwordID.text
        except IndexError:
            throw("ERROR", "Username seems not right. Try to check the data you provided.")
            App.is_connected = False
            return False
        except ValueError:
            throw("ERROR", "Username seems not right. Try to check the data you provided.")
            App.is_connected = False
            return False

        # Creating a socket
        App.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Trying to connect given address and port.
        try:
            App.connection.connect((App.conn_ip_addr, App.conn_port))
        except OSError as error:
            if error.errno == 111:
                throw("ERROR", f"Connection refused. Try to check the data you provided.", is_toasted=True)
            else:
                throw("ERROR", error)
            App.is_connected = False
            return False
        except OverflowError:
            throw("ERROR", f"Connection refused. Try to check the data you provided.", is_toasted=True)
            App.is_connected = False
            return False

        # Sending mobile's public key to server
        _ans = App.connection.sendto(App.public_key, (App.conn_ip_addr, App.conn_port))
        if not _ans:
            throw("ERROR", f"Couldn't send public key to the server.", is_toasted=True)
            App.is_connected = False
            return False

        # Storing the received server's public key
        public_key_server = App.connection.recv(512)
        if not public_key_server:
            throw("ERROR", f"Couldn't receive public key from the server.", is_toasted=True)
            App.is_connected = False
            return False

        # Creating a RSA object from server's public key with padding scheme
        encryptor_rsa = PKCS1_OAEP.new(RSA.import_key(public_key_server))
        # Creating a hash object to hash password
        hasher = SHA256.new()
        # Hash password with SHA256
        hasher.update(password.encode(FORMAT))
        # Encrypting the data for sending to server
        login_details = [encryptor_rsa.encrypt(username.encode(FORMAT)), encryptor_rsa.encrypt(hasher.digest())]

        # Sending username to server
        _ans = App.connection.sendto(login_details[0], (App.conn_ip_addr, App.conn_port))
        if not _ans:
            throw("ERROR", f"Couldn't send login details to the server.", is_toasted=True)
            App.is_connected = False
            return False

        # Sending password to server
        _ans = App.connection.sendto(login_details[1], (App.conn_ip_addr, App.conn_port))
        if not _ans:
            throw("ERROR", f"Couldn't send login details to the server.", is_toasted=True)
            App.is_connected = False
            return False

        # Receiving encrypted key from the server
        encrypted_key = App.connection.recv(256)
        if not encrypted_key:
            throw("ERROR", f"Couldn't receive session key from the server.", is_toasted=True)
            App.is_connected = False
            return False

        # Creating a RSA object from mobile's private key
        rsa_object_for_encrypted = RSA.import_key(App.key_pair.export_key())
        # Creating a object with padding scheme
        encryptor_for_rsa = PKCS1_OAEP.new(rsa_object_for_encrypted)
        # Decrypting so that we can save AES key
        key_aes = encryptor_for_rsa.decrypt(encrypted_key)

        try:
            # If server replied "False"
            if key_aes.decode(FORMAT) == "False":
                self.ids.usernameID.text = ""
                self.ids.passwordID.text = ""
                throw("ERROR", f"Wrong username and password.", is_toasted=True)
                App.is_connected = False
                return False
        except UnicodeDecodeError:
            # If server send us the real AES key, it'll start like
            # non-string byte so there'll be decode error.

            # Saving AES key to MainApp object.
            App.AES_key = key_aes

            # Creating a thread for receive function
            reciever_thread = threading.Thread(target=App.receive, daemon=True)
            reciever_thread.start()
            App.is_connected = True
            return True


class AdminPanel(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.resolution = (160, 120)
        # Starting threading for camera receiver
        video_thread = threading.Thread(target=self.camera_receiver, daemon=True)
        video_thread.start()

    def change_frame(self, frame, dt):
        # create a Texture the correct size and format for the frame
        texture = Texture.create(size=self.resolution, colorfmt='rgb')
        # copy the frame data into the texture
        texture.blit_buffer(frame, colorfmt='rgb', bufferfmt='ubyte')
        texture.flip_vertical()
        self.ids.live_photo.texture = texture

    def camera_receiver(self):
        data = b''
        payload_size = struct.calcsize("Q") + struct.calcsize("I") * 2
        waited_cycle = 0  # waited_cycle is the variable that holds cycles for connection tries.
        connection_camera = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connecting to the server with CONFIG details.
        # If port is closed, it'll give you a error and
        # try the next one.
        while True:
            port_bind = App.conn_port + 100
            if App.conn_port > 100 and App.is_connected:
                try:
                    connection_camera.connect((App.conn_ip_addr, port_bind))
                    break
                except ConnectionRefusedError:
                    throw("INFO", "Connection refused. Please check your ip address and port.", is_toasted=True)
            sleep(0.05)

        while True:
            # Receiving enough bytes to understand frame's length.
            # Payload_size is the size of message which will tell us the size of frame.
            while len(data) < payload_size:
                packet = connection_camera.recv(4 * 1024)  # 4KiB data receiving
                if not packet:
                    waited_cycle += 1
                    if waited_cycle >= 1000:
                        print("[SYSTEM] Connection went down. Restart the application. Exiting.")
                        connection_camera.close()
                        exit(0)
                    continue
                data += packet

            # Unpacking frame's size and resolution, which is data[:payload_size], with struct module.
            frame_size_and_resolution_packed = data[:payload_size]

            # Frame size unpacking
            unpacked_tuple = struct.unpack("IIQ", frame_size_and_resolution_packed)
            self.resolution = (unpacked_tuple[0], unpacked_tuple[1])
            frame_size = unpacked_tuple[2]
            data = data[payload_size:]  # Eliminating the frame size from received message.

            # Receiving message and combine it with older ones if there's space to frame_size.
            while len(data) < frame_size:
                data += connection_camera.recv(4 * 1024)

            # Selecting the frame from data with frame_size length.
            # We need to assign the remaining bytes to data for combining
            # with new ones received.
            frame = data[:frame_size]
            data = data[frame_size:]

            # Printing the frame
            Clock.schedule_once(partial(self.change_frame, frame))

    def temp_shield_toggle(self):
        msg_code = App.send("INFO", "tempshield_status", not App.tempshield_status)
        if not msg_code:
            throw("ERROR", "Sending tempshield_status data failed!", "")
            return False
        if not App.tempshield_status:
            self.ids.temp_shield_toggle_icon.icon = "layers"
            App.tempshield_status = not App.tempshield_status
        else:
            self.ids.temp_shield_toggle_icon.icon = "layers-off"
            App.tempshield_status = not App.tempshield_status
        return True

    def jammer_toggle(self):
        msg_code = App.send("INFO", "jammer_status", not App.jammer_status)
        if not msg_code:
            throw("ERROR", "Sending jammer_status data failed!", "")
            return False
        if not App.jammer_status:
            self.ids.jammer_toggle_icon.icon = "access-point-network"
            App.jammer_status = not App.jammer_status
        else:
            self.ids.jammer_toggle_icon.icon = "access-point-network-off"
            App.jammer_status = not App.jammer_status
        return True

    def car_light_toggle(self):
        msg_code = App.send("INFO", "light_status", not App.light_status)
        if not msg_code:
            throw("ERROR", "Sending light_status data failed!", "")
            return False
        if not App.light_status:
            self.ids.car_light_toggle_icon.icon = "car-light-high"
            App.light_status = not App.light_status
        else:
            self.ids.car_light_toggle_icon.icon = "car-light-fog"
            App.light_status = not App.light_status
        return True

    def car_engine_startstop(self):
        msg_code = App.send("INFO", "car_status", not App.car_status)
        if not msg_code:
            throw("ERROR", "Sending car_status data failed!", "")
            return False
        if not App.car_status:
            self.ids.car_engine_startstop_icon.icon = "engine"
            App.car_status = not App.car_status
        else:
            self.ids.car_engine_startstop_icon.icon = "engine-off"
            App.car_status = not App.car_status
        return True

    @staticmethod
    def quit():
        id_number = randint(11111, 99999)
        message = message_creator(id_number, "CLIENT", "!dis", False)
        message_encrypted, mac_tag, nonce = App.encrypt(message)
        num_of_bytes = App.connection.send(nonce + mac_tag + message_encrypted)
        if num_of_bytes:
            sleep(1)
            App.connection.close()
            throw("INFO", "Connection closed. You can close the app now.", "")
            exit()


class WinManager(ScreenManager):
    pass


class MainApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls = ThemeManager()
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_hue = "500"
        self.title = "Invisible Defender"

        self.connection = None
        self.is_connected = False
        self.conn_ip_addr = ""
        self.conn_port = 0
        self.AES_key = b''

        self.process_list = []
        self.car_status = 0
        self.light_status = 0
        self.tempshield_status = 0
        self.jammer_status = 0
        # First variable represent back and forward by -1 and 1 variables. Second one takes angle.
        self.engine_status = [0, 0]

    def build(self):
        self.root = Builder.load_file("template.kv")
        joystick = self.root.ids.apanel.ids.directionjoystick
        joystick.bind(pad=self.joystick_direction)
        return False

    @staticmethod
    def process(sett, val):
        if sett == "tempshield_status":
            if val:
                App.tempshield_status = True
                throw("INFO", "Temperature shield is activated.")
                return True
            elif not val:
                App.tempshield_status = False
                throw("INFO", "Temperature shield is deactivated.")
                return True
            else:
                return False
        elif sett == "jammer_status":
            if val:
                App.jammer_status = True
                throw("INFO", "Jammer is activated.")
                return True
            elif not val:
                App.jammer_status = False
                throw("INFO", "Jammer is deactivated.")
                return True
            else:
                return False
        elif sett == "light_status":
            if val:
                App.light_status = True
                throw("INFO", "Lights are activated.")
                return True
            elif not val:
                App.light_status = False
                throw("INFO", "Lights are deactivated.")
                return True
            else:
                return False
        elif sett == "car_status":
            if val:
                App.car_status = True
                throw("INFO", "Engine started.")
                return True
            elif not val:
                App.car_status = False
                throw("INFO", "Engine stopped.")
                return True
            else:
                return False
        elif sett == "battery_percentage":
            if isinstance(val, int):
                App.root.ids.apanel.ids.battery_item.text = str(val) + "%"
                return True
        elif sett == "outside_temperature":
            if isinstance(val, int):
                App.root.ids.apanel.ids.outside_temp_item.text = str(val) + "°C"
                return True
        elif sett == "inside_temperature":
            if isinstance(val, int):
                App.root.ids.apanel.ids.inside_temp_item.text = str(val) + "°C"
                return True
        elif sett == "peltier_right":
            if isinstance(val, int):
                App.root.ids.apanel.ids.pel_right_item.text = "pR: " + str(val) + "°C"
                return True
        elif sett == "peltier_left":
            if isinstance(val, int):
                App.root.ids.apanel.ids.pel_left_item.text = "pL: " + str(val) + "°C"
                return True
        elif sett == "peltier_top":
            if isinstance(val, int):
                App.root.ids.apanel.ids.pel_top_item.text = "pT: " + str(val) + "°C"
                return True
        elif sett == "peltier_back":
            if isinstance(val, int):
                App.root.ids.apanel.ids.pel_back_item.text = "pB: " + str(val) + "°C"
                return True
        else:
            pass

    @staticmethod
    def encrypt(message_to_send):
        """
        A function to encrypt given data with AES_GDC method
        and using MainApp.AES_key.

        :param message_to_send: as string
        :return: encrypted_message, mac_tag, nonce
        """
        aes_encrpytion_object = AES.new(App.AES_key, AES.MODE_GCM)
        encrypted_message, mac_tag = aes_encrpytion_object.encrypt_and_digest(message_to_send.encode(FORMAT))
        nonce = aes_encrpytion_object.nonce
        return encrypted_message, mac_tag, nonce

    @staticmethod
    def decrypt(nonce, mac_tag, encrypted_message):
        """
        A function to decrypt given data with AES_GDG method
        and using MainApp.AES_key.

        :param mac_tag: To verify the message (bytes)
        :param nonce: To create decryptor AES object (bytes)
        :param encrypted_message: The secret message (bytes)
        :return: decrypted message: The plain text (string)
        """
        decryptor = AES.new(App.AES_key, AES.MODE_GCM, nonce=nonce)
        try:
            decrypted_message_as_bytes = decryptor.decrypt_and_verify(encrypted_message, mac_tag)
        except ValueError:
            throw("ERROR", "The message is not trusted.", is_toasted=True)
            return False
        decrypted_message = decrypted_message_as_bytes.decode(FORMAT)
        return decrypted_message

    @staticmethod
    def send(typey, setting, value, id_number=None):
        if not id_number:
            # Creation of random id number.
            id_number = randint(11111, 99999)

        if typey == "INFO":
            # Adding to the process list for waiting confirmation
            App.process_list.append({
                "conf": int(id_number),
                "setting": setting,
                "value": value
            })

        # Creating message
        message = message_creator(id_number, typey, setting, value)

        # Encrypting the message
        message_encrypted, mactag, nonce = App.encrypt(message)

        # Combining return values of encryption into one bytes string.
        # It should be like: nonce+macTag+encrypted message
        message_to_send = nonce + mactag + message_encrypted

        # Sending message via thread
        thread_input = threading.Thread(target=App.connection.send,
                                        args=(message_to_send,), daemon=True)
        thread_input.start()
        return True

    @staticmethod
    def receive():
        try_attempt = 0
        while True:
            try:
                data = App.connection.recv(512)
                if data:
                    try:
                        nonce = data[:16]
                        mac_tag = data[16:32]
                        encrypted_message = data[32:]
                        data = App.decrypt(nonce, mac_tag, encrypted_message)
                    except Exception:
                        continue
                    throw("INFO", f"Received! {data}", "", is_toasted=False)

                if not data:
                    if data == b'':
                        try_attempt += 1
                        if try_attempt == 1000:
                            App.connection.close()
                            throw("ERROR", "Connection lost with server. You must restart the app.", "")
                    continue

                # message -> id:type:setting:value
                message = message_splitter(data)

                if message[1] == "CONF":
                    for item in App.process_list:
                        if int(message[0]) == item["conf"]:
                            threading.Thread(target=App.process, args=(item["setting"], item["value"],)).start()
                            App.process_list.remove(item)

                elif message[1] == "CLIENT" and message[2] == "!dis" and not message[3]:
                    throw("ERROR", f"Connection closed by the server.", "")
                    App.connection.close()

                else:
                    threading.Thread(target=App.process, args=(message[2], message[3],)).start()

                    # Sending confirmation message
                    App.send("CONF", "confirmation", True, id_number=message[0])

            except ConnectionResetError:
                throw("ERROR", f"Connection closed by the server.", "")
                App.connection.close()
                break
            except Exception as error:
                throw("ERROR", error, "")
                App.connection.close()
                break

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
        if 4 <= a <= 14 and App.engine_status[1] != a and App.engine_status[0] != 0:
            if App.send("INFO", "direction_angle", a):
                App.engine_status[1] = a
            else:
                throw("ERROR", "Sending forward direction_angle data failed!", "")
        elif 32 >= a >= 22 and App.engine_status[1] != (36 - a) and App.engine_status[0] != 0:
            a = 36 - a
            if App.send("INFO", "direction_angle", a):
                App.engine_status[1] = a
            else:
                throw("ERROR", "Sending backward direction_angle data failed!", "")

        # Sending the power - forward, backward or stop
        if float(y) >= 0.64 and App.engine_status[0] != 1:
            if App.send("INFO", "direction", "forward"):
                App.engine_status[0] = 1
            else:
                throw("ERROR", "Sending forward direction data failed.", "")
        elif float(y) <= -0.64 and App.engine_status[0] != -1:
            if App.send("INFO", "direction", "backward"):
                App.engine_status[0] = -1
            else:
                throw("ERROR", "Sending backward direction data failed.", "")
        elif -0.64 < float(y) < 0.64 and App.engine_status[0] != 0:
            if App.send("INFO", "direction", "stop"):
                App.engine_status[0] = 0
            else:
                throw("ERROR", "Sending stop direction data failed.", "")


if __name__ == "__main__":
    # Creating the App instance of MainApp class.
    App = MainApp()
    #  Running the instance.
    App.run()
    # Since we're calling instance in some of the methods
    # of screen and MainApp classes, don't change "App"
    # name for the instance. If you have to change,
    # change all "App" names to that name which you've
    # changed. Or you can change "App" to "MainApp.get_running_app()"
    # so that it can be dynamically find instance. We haven't used it
    # because it is so long and code looks like crap :P
