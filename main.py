import os
import sys
import threading
import sqlite3
import time 
import io
from sigint_lib import os_info
from sigint_lib import db_tools
from sigint_lib import app_env
from sigint_lib import rtl_sdr



import tkinter as tk
from tkinter import ttk
from tkinter import ttk
from tkinter import filedialog
from tkinter.font import Font

from PIL import Image, ImageTk




MAIN_DBS_NAME = "sigint.sqlite3"
#MAIN_DBS_FILE_PATH = str(sys._MEIPASS) + str(os.sep) + str(MAIN_DBS_NAME)
MAIN_DBS_FILE_PATH = MAIN_DBS_NAME
MAIN_DB_CONNECTIONS = sqlite3.connect(MAIN_DBS_FILE_PATH)
MAIN_DB_CURSOR = MAIN_DB_CONNECTIONS.cursor()


system_vendor = db_tools.get_value_sysmtemCore(key=app_env.KEY_DB__APP_VENDOR,
    sqlite_db_cursor=MAIN_DB_CURSOR,
    sqlite_db_object=MAIN_DB_CONNECTIONS
    )["data"]

system_name = db_tools.get_value_sysmtemCore(key=app_env.KEY_DB__APP_TITLE,
    sqlite_db_cursor=MAIN_DB_CURSOR,
    sqlite_db_object=MAIN_DB_CONNECTIONS
    )["data"]


app_icon_blob = db_tools.get_value_blobStorage(key=app_env.KEY_DB__APP_ICON,
    sqlite_db_cursor=MAIN_DB_CURSOR,
    sqlite_db_object=MAIN_DB_CONNECTIONS
)["data"]






class SigintProject(tk.Tk):
    
    def __init__(self):
        super().__init__()
        
        self.title(f"{system_name}")
        self.geometry("900x500+200+50")
        
        self.TabController = ttk.Notebook()
        
        
        self.tab_1_gbakis = ttk.Frame(self.TabController)
        self.tab_2_rtlsdr = ttk.Frame(self.TabController)
        self.TabController.add(self.tab_1_gbakis, text="Genel bakış")
        self.TabController.add(self.tab_2_rtlsdr, text="Dinleme Ekranı")
        
        
        self.TabController.pack(expand=1, fill="both")
        icon_image = Image.open(io.BytesIO(app_icon_blob))
        self.iconphoto(True, ImageTk.PhotoImage(icon_image))
        self.TitleFonts = Font(family="arial",size="16",)
        self.StandartFonts = Font(family="arial",  size="12",)   
        
        self.helv12 = Font(family="Helvatica",size=12, weight="bold")
        
        
        self.StandartColor = "#0a1e4a"
        
        
        self.tab_1__WelcomeScreen = tk.Label(self.tab_1_gbakis,text="", justify="left", font=self.helv12 ,fg="#0a1e4a")
        self.tab_1__WelcomeScreen.place(relx=0.001, rely=0.001)
        self.tab_1__update_info()
        
        
        
        # PAGE 2 
        
        
        self.tab_2__CihazSecmeBildirisi = tk.Label(self.tab_2_rtlsdr, text="RTL-SDR cihazı: ", justify="left", font=self.helv12,fg="#0a1e4a")
        self.tab_2__CihazSecmeBildirisi.place(relx=0.001, rely=0.001)
        
        self.VarolanRTlSDRcihazlari = []
        self.SelectedDevice = tk.StringVar()
        
        raw_cihaz_list = rtl_sdr.list_of_device_in_system_id()
        
        if raw_cihaz_list["success"] != "true":
            self.VarolanRTlSDRcihazlari.append(raw_cihaz_list["message"])
        else:
            for single_cihaz in raw_cihaz_list["data"]:
                self.VarolanRTlSDRcihazlari.append(single_cihaz)
        
        
        self.SelectTargetDevice = ttk.Combobox(
            master=self.tab_2_rtlsdr,
            textvariable=self.SelectedDevice,
            values=self.VarolanRTlSDRcihazlari,
            
        )    
        self.SelectTargetDevice.set(self.VarolanRTlSDRcihazlari[0])
        self.SelectTargetDevice.place(relx=0.16, rely=0.001,height=30)
        
        
        self.UpdateDeviceList_button = tk.Button(
            master=self.tab_2_rtlsdr,
            text="güncelle",
            command=self.tab_2__cihaz_listesi_guncelleme,
        )
        self.UpdateDeviceList_button.place(relx=0.38, rely=0.001,width=100, height=30)
        
        
        
        
        
    def tab_2__cihaz_listesi_guncelleme(self):
        self.VarolanRTlSDRcihazlari = []
        raw_cihaz_list = rtl_sdr.list_of_device_in_system_id()
        
        if raw_cihaz_list["success"] != "true":
            self.VarolanRTlSDRcihazlari.append(raw_cihaz_list["message"])
        else:
            for single_cihaz in raw_cihaz_list["data"]:
                self.VarolanRTlSDRcihazlari.append(single_cihaz)

        self.SelectTargetDevice.config(values=self.VarolanRTlSDRcihazlari)
        self.SelectTargetDevice.set(self.VarolanRTlSDRcihazlari[0])


    def tab_1__update_info(self) -> None:
        total_ram, used_ram, yuzdelik_ram = os_info.get_memory_usage()
        cpu_usage = os_info.get_cpu_usage()
        batary_status = os_info.get_battery_percentage()
        os_platform = os_info.patlform_info()
        date_and_time = os_info.get_current_time()
        self.tab_1__WelcomeScreen.config(text=f"""> Sisteme hoş geldin {os_info.get_active_user()}@{os_info.get_hostname()}

> Ram kullanımı: {total_ram} / {used_ram} GB, %{yuzdelik_ram}
> İşlemci kullanımı: %{cpu_usage}
> Batarya durumu: {batary_status}
> Platfom: {os_platform}
> Total CPU: {os_info.total_cpu_count()}
> Tarih ve saat: {date_and_time}
> SigintUI sürümü: {app_env.VERSION}
    """)
        self.after(1000, self.tab_1__update_info)
    


if __name__ == "__main__":
    app_root = SigintProject()
    app_root.mainloop()