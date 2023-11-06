import psutil
import platform
import datetime
import socket
import os



def get_battery_percentage():
    battery = psutil.sensors_battery()
    percentage = "%"+str(round(battery.percent,1)) if battery else "Bilinmiyor"
    return percentage

def get_memory_usage():
    memory = psutil.virtual_memory()
    total = memory.total / (1024 ** 3)  # GB
    used = memory.used / (1024 ** 3)  # GB
    percentage = memory.percent
    return round(total, 1), round(used,1), percentage



def get_cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    return cpu_percent      




def get_active_user() -> object:
    return os.getlogin()


def patlform_info() -> object:
    return platform.platform()




def get_current_time() -> object:
    """ herhangi bir arguman almaz

    Returns:
        str: anlık çağrılma tarihini döndürür 
    """
    an = datetime.datetime.now()
    time_is = str(datetime.datetime.strftime(an, '%c'))
    return time_is



def total_cpu_count() -> object:
    return os.cpu_count()


def get_hostname() -> object:
    try:
        return socket.gethostname()
    except Exception:
        return "failed-to-detect-host-name"



