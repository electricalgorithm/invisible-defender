from config import *
from time import asctime, localtime, time
from kivymd.toast import toast


def throw(msg_type, message, conn=None, is_toasted=True):
    logfile = open(f"{LOGFILE}.log", "a")
    _time = asctime(localtime(time()))
    if conn:
        print(f"[{msg_type}]\t{message} ({conn})")
        logfile.write(f"[{msg_type}][{_time}]\t{message} ({conn}\n")
        if is_toasted:
            toast(f"[{msg_type}]  {message} ({conn})")
    else:
        print(f"[{msg_type}]\t{message}")
        logfile.write(f"[{msg_type}][{_time}]\t{message}\n")
        if is_toasted:
            toast(f"[{msg_type}]  {message}")
    logfile.close()


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
