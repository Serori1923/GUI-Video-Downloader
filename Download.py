import json
import requests
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import webbrowser
import time

#載入設定檔
downloadHistoryJsonPath = __file__.replace("Download.py", "downloadHistory.json")
settingJsonPath = __file__.replace("Download.py", "setting.json")
iconPath = __file__.replace("Download.py", "ShigureUi_icon.ico")

with open(settingJsonPath, 'r', encoding='utf8') as jfile:
    setting = json.load(jfile)

#載入語言
with open(f'{__file__.replace("Download.py", "Language/")}/{setting["Language"]}.json', 'r', encoding='utf8') as jfile:
    text = json.load(jfile)

def updateUI():
    #更新標題
    root.title(text["windowsTitle"])
    if setting["Language"] == "zh_TW":
        root.minsize(550,350)
    if setting["Language"] == "ja_JP":
        root.minsize(580,350)
    if setting["Language"] == "en_US":
        root.minsize(700,350)

    #更新選單
    menu_preference_Button.config(text=text["preference_menu"]["preference"])
    menu_downloadHistory_Button.config(text=text["downloadHistory_menu"]["downloadHistory"])

    #更新下載按鈕
    download_Button.config(text=text["downloadButton"])    

    #更新下載選項標題
    download_Option_Label.config(text=text["downloadOptionsTitle"])

    #更新下載選項按鈕顏色和文字
    optionBtn1.config(text=text["downloadOptionsButton"]["videoAndAudio"], bg="#5a5158", fg="#d8f2da")
    optionBtn2.config(text=text["downloadOptionsButton"]["audioOnly"], bg="#5a5158", fg="#d8f2da")
    optionBtn3.config(text=text["downloadOptionsButton"]["videoOnly"], bg="#5a5158", fg="#d8f2da")

    #更新下載狀態
    download_Status_label.config(text=text["downloadStatusTitle"])
    stauts.config(text=text["status"]["ready"], fg="#678F8D")

    #更新下載資訊
    info_Title_label.config(text=text["infoTitle"]["download"])
    info_Description_label.config(text=text["infoDescription"]["notDownload"])

    #更新偏好設定中的語言設置
    preference_Window.title(text["preference_menu"]["preference"])
    language_Title.config(text=text["preference_menu"]["languageSetting"])
    save_Button.config(text=text["preference_menu"]["saveButton"])
    close_Button.config(text=text["preference_menu"]["closeButton"])

    #更新歷史下載視窗的內容
    downloadHistory_Window.title(text["downloadHistory_menu"]["downloadHistory"])
    history_Title.config(text=text["downloadHistory_menu"]["downloadHistory"])
    notice_Title.config(text=text["downloadHistory_menu"]["notice"])
    clear_Button.config(text=text["downloadHistory_menu"]["clearButton"])
    refrash_Button.config(text=text["downloadHistory_menu"]["refrashButton"])

    tree.heading("col1", text=text["downloadHistory_menu"]["list"]["number"])
    tree.heading("col2", text=text["downloadHistory_menu"]["list"]["downloadDate"])
    tree.heading("col3", text=text["downloadHistory_menu"]["list"]["fileName"])
    tree.heading("col4", text=text["downloadHistory_menu"]["list"]["fileLink"])
    tree.heading("col5", text=text["downloadHistory_menu"]["list"]["originalURL"])

    #刷新界面
    root.update_idletasks()

def setLanguage(language):
    global text

    language_map = {
        "繁體中文": "zh_TW",
        "English": "en_US",
        "日本語": "ja_JP"
    }
    
    setting["Language"] = language_map.get(language)
    with open(settingJsonPath, 'w', encoding='utf8') as sfile:
        json.dump(setting, sfile, ensure_ascii=False, indent=4)

    with open(f'{__file__.replace("Download.py", "Language/")}/{setting["Language"]}.json', 'r', encoding='utf8') as jfile:
        text = json.load(jfile)
    
    updateUI()

language_Title = None
save_Button = None
close_Button = None

preference_Window = None #建立偏好設定視窗變數
def openPreferenceWindow():
    global preference_Window, language_Title, save_Button, close_Button

    if not preference_Window or not preference_Window.winfo_exists():
        preference_Window = tk.Toplevel(root)
        preference_Window.title(text["preference_menu"]["preference"])
        preference_Window.geometry("400x250+700+300")
        preference_Window.minsize(400,250)
        preference_Window.configure(bg="#d8f2da")
        preference_Window.iconbitmap(iconPath)

        language_Title = tk.Label(preference_Window, text=text["preference_menu"]["languageSetting"],bg="#d8f2da", fg="#678F8D", font=("Yu Gothic UI", 15, "bold"))
        language_Title.pack(pady=20)

        #創建一個樣式物件
        if "comboStyle" not in comboboxStyle.theme_names():
            comboboxStyle.theme_create("comboStyle", parent="alt", settings={
                "TCombobox": {
                    "configure": {
                        "fieldbackground": "#fde4de",
                        "selectbackground": "#fde4de",
                        "selectforeground": "#102323",
                        "background": "#fde4de",
                        "foreground": "#102323",
                        "padding": 5,
                        "font": ("Yu Gothic UI", 10, "bold")
                    }
                }
            })

        # 修改 Combobox 的字體和背景
        comboboxStyle.theme_use("comboStyle")
        comboboxStyle.configure("TCombobox")

        combobox = ttk.Combobox(preference_Window, state='readonly', values=["繁體中文", "English", "日本語"], style="TCombobox")
        combobox.pack()

        match setting["Language"]:
            case "zh_TW":
                combobox.current(0)
            case "en_US":
                combobox.current(1)
            case "ja_JP":
                combobox.current(2)

        buttonFrame=tk.Frame(preference_Window, bg="#d8f2da", height=50, width=500) #設定按鈕區塊
        buttonFrame.pack(pady=10)

        save_Button = tk.Button(buttonFrame, text=text["preference_menu"]["saveButton"], borderwidth=0, bg="#5a5158",fg="#d8f2da", font=("Yu Gothic UI", 14, "bold"), padx=8, command=lambda: setLanguage(combobox.get()))
        save_Button.pack(side=tk.LEFT, padx=10, fill="y")

        close_Button = tk.Button(buttonFrame, text=text["preference_menu"]["closeButton"], borderwidth=0, bg="#5a5158",fg="#d8f2da", font=("Yu Gothic UI", 14, "bold"), padx=8, command=preference_Window.destroy)
        close_Button.pack(side=tk.LEFT, padx=10, fill="y")

history_Title = None
notice_Title = None
clear_Button = None
refrash_Button = None
tree = None

downloadHistory_Window = None #建立歷史下載視窗變數
def openDownloadHistoryWindow():
    global downloadHistory_Window, history_Title, notice_Title, clear_Button, refrash_Button, tree

    if not downloadHistory_Window or not downloadHistory_Window.winfo_exists():
        downloadHistory_Window = tk.Toplevel(root)
        downloadHistory_Window.title(text["downloadHistory_menu"]["downloadHistory"])
        screen_width = downloadHistory_Window.winfo_screenwidth()
        screen_height = downloadHistory_Window.winfo_screenheight()
        downloadHistory_Window.geometry(f"{screen_width-20}x{screen_height-100}+0+10")
        downloadHistory_Window.minsize(1000,500)
        downloadHistory_Window.configure(bg="#d8f2da")
        downloadHistory_Window.iconbitmap(iconPath)

        #標題
        history_Title = tk.Label(downloadHistory_Window, text=text["downloadHistory_menu"]["downloadHistory"], bg="#d8f2da", fg="#678F8D", font=("Yu Gothic UI", 15, "bold"))
        history_Title.pack(pady=10)

        #提示訊息Label
        notice_Title = tk.Label(downloadHistory_Window, text=text["downloadHistory_menu"]["notice"], bg="#d8f2da", fg="#678F8D", font=("Yu Gothic UI", 12, "bold"))
        notice_Title.pack(pady=10)

        # 創建一個樣式物件
        if "treeStyle" not in treeViewStyle.theme_names():
            treeViewStyle.theme_create("treeStyle", parent="alt", settings={
                "Treeview": {
                    "configure": {
                        "fieldbackground": "#fde4de",
                        "selectbackground": "#fde4de",
                        "selectforeground": "#102323",
                        "background": "#fde4de",
                        "foreground": "#102323",
                        "padding": 5,
                        "font": ("Yu Gothic UI", 12)
                    }
                }
            })

        # 修改 treeView 的字體和背景
        treeViewStyle.theme_use("treeStyle")
        treeViewStyle.configure("Treeview")

        treeViewStyle.map("Treeview", background=[("selected", "#bed1c0")], foreground=[("selected", "#000000")])
        
        tree = ttk.Treeview(downloadHistory_Window, columns=("col1", "col2", "col3", "col4", "col5"), show="headings", style="Treeview")

        # 定義欄位標題
        tree.heading("col1", text=text["downloadHistory_menu"]["list"]["number"])
        tree.heading("col2", text=text["downloadHistory_menu"]["list"]["downloadDate"])
        tree.heading("col3", text=text["downloadHistory_menu"]["list"]["fileName"])
        tree.heading("col4", text=text["downloadHistory_menu"]["list"]["fileLink"])
        tree.heading("col5", text=text["downloadHistory_menu"]["list"]["originalURL"])

        # 定義欄位寬度
        tree.column("col1", width=55, anchor="center", stretch=False)
        tree.column("col2", width=190, anchor="center", stretch=False)
        tree.column("col3", width=700, anchor="w", stretch=False)
        tree.column("col4", width=350, anchor="center", stretch=False)
        tree.column("col5", width=500, anchor="w", stretch=True)

        def loadData():
            for item in tree.get_children(): #清空表單
                tree.delete(item)

            with open(f'{downloadHistoryJsonPath}', 'r', encoding='utf8') as jfile: #讀取歷史資料
                data = json.load(jfile)

            if isinstance(data, list) and not data: #如果歷史紀錄是空的就顯示沒有資料
                tree.insert("", "end", values=("", "", text["downloadHistory_menu"]["list"]["noData"], "", ""))

            else:
                for item in data: #將資料放進表單
                    tree.insert("", "end", values=(item["number"], item["downloadDate"], item["fileName"], item["fileLink"], item["originalURL"]))

        def on_clear_button_click():
            result = messagebox.askyesno(parent=downloadHistory_Window, title=text["downloadHistory_menu"]["deleteConfirmTitle"], message=text["downloadHistory_menu"]["deleteConfirmText"])
            if result:
                removeAllData()

        def removeAllData():
            with open(f'{downloadHistoryJsonPath}', 'w', encoding='utf8') as jfile:
                json.dump([], jfile, ensure_ascii=False, indent=4)

            loadData()
                
        #載入資料
        loadData()

        # 顯示 Treeview
        tree.pack(pady=10, fill=tk.BOTH, expand=True)

        buttonFrame=tk.Frame(downloadHistory_Window, bg="#d8f2da", height=50, width=500) #設定按鈕區塊
        buttonFrame.pack(pady=10)

        clear_Button = tk.Button(buttonFrame, text=text["downloadHistory_menu"]["clearButton"], borderwidth=0, bg="#5a5158",fg="#d8f2da", font=("Yu Gothic UI", 14, "bold"), padx=8, command=on_clear_button_click)
        clear_Button.pack(side=tk.LEFT, padx=10, fill="y")

        refrash_Button = tk.Button(buttonFrame, text=text["downloadHistory_menu"]["refrashButton"], borderwidth=0, bg="#5a5158",fg="#d8f2da", font=("Yu Gothic UI", 14, "bold"), padx=8, command=loadData)
        refrash_Button.pack(side=tk.LEFT, padx=10, fill="y")

#初始化主視窗
root = tk.Tk()
root.geometry("600x400+600+250")
root.title(text["windowsTitle"])
root.configure(bg="#d8f2da")
root.iconbitmap(iconPath)
comboboxStyle = ttk.Style()
treeViewStyle = ttk.Style()

if setting["Language"] == "ja_JP":
    root.minsize(580,350)
elif setting["Language"] == "en_US":
    root.minsize(700,350)
else:
    root.minsize(550,350)

def callback(url): #定義Label的超連結功能
    webbrowser.open_new(url)

def writeDataToJson(fileName, fileLink, originalURL):
    with open(downloadHistoryJsonPath, 'r', encoding='utf8') as jfile:
        history = json.load(jfile)

    nowtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    new_data = {
        "number": f"{len(history)+1}",
        "downloadDate": f"{nowtime}",
        "fileName": fileName,
        "fileLink": fileLink,
        "originalURL": originalURL
    }

    history.append(new_data)

    with open(downloadHistoryJsonPath, 'w', encoding='utf-8') as file: #將資料寫入History
        json.dump(history, file, indent=4, ensure_ascii=False)


requestsData=setting["Default"].copy() #複製預設設定避免修改原始設定檔
def Download():
    requestsData["url"]=entry.get() #從輸入框取得原始影片網址

    stauts.config(text=text["status"]["downloading"], fg="#678F8D")
    root.update_idletasks() #強制刷新 GUI，讓文字立刻更新
    try:
        response = requests.post('http://192.168.50.51', headers=setting["headers"], data=json.dumps(requestsData)) #向API發送資料
        response_dict = response.json() #解析API回傳資料
        
    except requests.RequestException as e:
        stauts.config(text=text["status"]["requestFail"], fg="#ff0000")
        info_Title_label.config(text=text["infoTitle"]["error"])
        info_Description_label.config(text=text["infoDescription"]["failToConnectToServer"])
        info_Description_label.unbind("<Button-1>")
        return

    if response_dict["status"] == "error":
        stauts.config(text=text["status"]["fail"], fg="#ff0000")
        info_Title_label.config(text=text["infoTitle"]["error"])
        error_map = text["error_map"]
        info_Description_label.config(text=f"{error_map.get(response_dict['error']['code'], error_map['unknownError'])}") #從error_map中取得錯誤提示
        info_Description_label.unbind("<Button-1>") #取消超連結與Label綁定
        print(response_dict['error'])

    else:
        stauts.config(text=text["status"]["success"], fg="#65c365")
        info_Title_label.config(text=text["infoTitle"]["fileLink"])
        info_Description_label.config(text=f"{response_dict['filename']}")
        info_Description_label.bind("<Button-1>", lambda e: callback(f"{response_dict['url']}")) #設定超連結並與Label綁定

        writeDataToJson(response_dict['filename'], response_dict['url'], entry.get())

#---------------頂部選單區塊---------------
menuFrame=tk.Frame(root, bg="#bed1c0", height=50, width=500) 
menuFrame.pack(fill="x") #顯示並填滿x軸

#添加「偏好設定」選單
menu_preference_Button=tk.Button(menuFrame, text=text["preference_menu"]["preference"], borderwidth=0, bg='#bed1c0', fg='#f2f5f5', font=("Yu Gothic UI", 12, "bold"), command=openPreferenceWindow, padx=5)
menu_preference_Button.pack(side="left",fill="y")

#添加「歷史下載」選單
menu_downloadHistory_Button=tk.Button(menuFrame, text=text["downloadHistory_menu"]["downloadHistory"], borderwidth=0, bg='#bed1c0', fg='#f2f5f5', font=("Yu Gothic UI", 12, "bold"), command=openDownloadHistoryWindow, padx=5)
menu_downloadHistory_Button.pack(side="left",fill="y")

#------------------------------------------

#--------------網址輸入欄區塊----------------
frameUpper=tk.Frame(root, bg="#bed1c0", height=50, width=500)
frameUpper.pack(fill="x") #顯示並填滿x軸

entry = tk.Entry(frameUpper, width=38, bg="#fde4de", fg="#102323", font=("Yu Gothic UI", 15, "bold"))  #輸入框
entry.pack(side="left", fill="x", expand=True, padx=5)

download_Button=tk.Button(frameUpper, text=text["downloadButton"], borderwidth=0, bg='#bed1c0', fg='#f2f5f5', font=("Yu Gothic UI", 15, "bold"), command=Download, padx=5)
download_Button.pack(side="right",fill="y")

download_Option_Label = tk.Label(root, text=text["downloadOptionsTitle"], bg="#d8f2da", fg="#678F8D", width=30, font=("Yu Gothic UI", 15, "bold"))
download_Option_Label.pack()

#-------------------------------------------


#----------------設定按鈕區塊----------------
def VideoAndAudio():
    requestsData["downloadMode"] = "auto"
    optionBtn1.config(bg="#41313e",fg="#d8f0f2")
    optionBtn2.config(bg="#5a5158",fg="#d8f2da")
    optionBtn3.config(bg="#5a5158",fg="#d8f2da")

def AudioOnly():
    requestsData["downloadMode"] = "audio"
    optionBtn1.config(bg="#5a5158",fg="#d8f2da")
    optionBtn2.config(bg="#41313e",fg="#d8f0f2")
    optionBtn3.config(bg="#5a5158",fg="#d8f2da")

def VideoOnly():
    requestsData["downloadMode"] = "mute"
    optionBtn1.config(bg="#5a5158",fg="#d8f2da")
    optionBtn2.config(bg="#5a5158",fg="#d8f2da")
    optionBtn3.config(bg="#41313e",fg="#d8f0f2")

buttonFrame = tk.Frame(root, bg="#d8f2da")
buttonFrame.pack(pady=10)  #增加上下距離讓視覺效果更美觀

optionBtn1=tk.Button(buttonFrame, text=text["downloadOptionsButton"]["videoAndAudio"], command=VideoAndAudio, borderwidth=0, bg="#5a5158",fg="#d8f2da", font=("Yu Gothic UI", 18, "bold"))
optionBtn1.pack(side=tk.LEFT, padx=10, fill="y")

optionBtn2=tk.Button(buttonFrame, text=text["downloadOptionsButton"]["audioOnly"], command=AudioOnly, borderwidth=0, bg="#5a5158",fg="#d8f2da", font=("Yu Gothic UI", 18, "bold"))
optionBtn2.pack(side=tk.LEFT, padx=10, fill="y")

optionBtn3=tk.Button(buttonFrame, text=text["downloadOptionsButton"]["videoOnly"], command=VideoOnly, borderwidth=0, bg="#5a5158",fg="#d8f2da", font=("Yu Gothic UI", 18, "bold"))
optionBtn3.pack(side=tk.LEFT, padx=10, fill="y")

infoFrame = tk.Frame(root, bg="#d8f2da") #下載狀態與資訊區塊
infoFrame.pack(pady=10)  #增加上下距離讓視覺效果更美觀

#------------------------------------------

#-------------------下載狀態-----------------
download_Status_label = tk.Label(infoFrame, text=text["downloadStatusTitle"], bg="#d8f2da", fg="#678F8D", font=("Yu Gothic UI", 15, "bold"))
download_Status_label.pack(side=tk.LEFT, fill="y")

stauts = tk.Label(infoFrame, text=text["status"]["ready"], bg="#d8f2da", fg="#678F8D", justify="left", font=("Yu Gothic UI", 15, "bold"))
stauts.pack(side=tk.LEFT, fill="y")
#------------------------------------------

#--------------------下載訊息------------------
info_Title_label = tk.Label(root, text=text["infoTitle"]["download"], bg="#d8f2da", fg="#678F8D", font=("Yu Gothic UI", 15, "bold"))
info_Title_label.pack()
info_Description_label = tk.Label(root, text=text["infoDescription"]["notDownload"], bg="#d8f2da", fg="#aaa5ec", justify="left", wraplength=550, font=("Yu Gothic UI", 15, "bold"))
info_Description_label.pack()
#------------------------------------------


window_width, window_height = 600, 400
def resize(event): #視窗伸縮時避免檔案連結超出畫面
    global window_width, window_height
    if event.widget == root:
        if window_width != event.width:
            window_width, window_height = event.width, event.height
            info_Description_label.config(wraplength=window_width-40)

root.bind("<Configure>", resize)
root.mainloop()