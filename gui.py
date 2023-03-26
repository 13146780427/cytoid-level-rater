from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import json
import zipfile
from ffmpeg import audio
import os
import subprocess
import shutil
from tkinter import filedialog
import tkinter.messagebox



OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("517x751")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 751,
    width = 517,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    258.0,
    375.0,
    image=image_image_1
)


#转成ogg
def a_convert(input, output):
    try:
        cmd = "ffmpeg.exe -y -i %s -acodec libvorbis %s" % ('\"' + input + '\"', '\"' + output + '\"')
        res = subprocess.call(cmd, shell=True)
        if res != 0:
            return False
        return True
    except Exception:
        return False
def a_speed(input_file, speed, out_file):
    try:
        cmd = "ffmpeg.exe -y -i %s -filter_complex \"atempo=tempo=%s\" %s" % (input_file, speed, out_file)
        res = subprocess.call(cmd, shell=True)

        if res != 0:
            return False
        return True
    except Exception:
        return False
#压缩
def zip_dir(directory, zipname):
    if os.path.exists(directory):
        outZipFile = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)
        rootdir = os.path.basename(directory)
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath   = os.path.join(dirpath, filename)
                parentpath = os.path.relpath(filepath, directory)
                arcname    = os.path.join(rootdir, parentpath)
                outZipFile.write(filepath, arcname)
    outZipFile.close()
#倍速
def rater(order, rate, level_path):
    #创建临时文件夹
    temp_path = 'temp/'
    rate_path = temp_path + str(rate) + '/'
    os.mkdir(temp_path)
    os.mkdir(rate_path)
    #改成zip
    original_path = level_path
    level_name = os.path.basename(level_path).split(".")[len(os.path.basename(level_path).split("."))-2]
    shutil.copy(level_path, temp_path + level_name + '.zip')
    level_path = temp_path + level_name + '.zip'
    #指定谱面路径和音频路径和文件路径
    chart_out = str(rate) + '.json'
    music_out = str(rate) + '.ogg'
    chart_out_path = rate_path + chart_out 
    music_out_path = rate_path + music_out
    level_out_path =  level_name + '_' + str(rate) + '.zip'
    #解压
    level = zipfile.ZipFile(level_path)
    for f in level.namelist():
       level.extract(f, temp_path)
    level.close()
    #读level.json
    with open(temp_path + 'level.json', 'rb') as f:
        params = json.load(f)
        chart_path = temp_path + params['charts'][order]['path']
        music_path = temp_path + params['music']['path']
        bg = params['background']['path']
        prev = params['music_preview']['path']
        level_id = params['id']
        level_title = params['title']
    #判断是不是ogg，不是就转
    if music_path.split(".")[len(music_path.split("."))-1] != '.ogg':
        a_convert(music_path, music_path.split(".")[0] + '.ogg')
        music_path = music_path.split(".")[0] + '.ogg'
    #音频倍速输出
    a_speed('\"' + music_path + '\"', rate, '\"' + music_out_path + '\"')
    #谱面倍速
    with open(chart_path, 'rb') as f:
        param = json.load(f)
        for i in range(0, len(param['tempo_list'])):
            param['tempo_list'][i]['value'] = int(param['tempo_list'][i]['value'] / float(rate))
    #谱面倍速输出
    with open(chart_out_path, 'w') as r:
        json.dump(param, r)
    #level.json倍速输出
    with open(rate_path + 'level.json', 'w') as r:
        params['charts'][order]['path'] = chart_out
        params['charts'][order]['name'] = rate
        params['charts'][order]['difficulty'] = 0
        params['music']['path'] = music_out
        params['id'] = level_id + '.' + rate
        level_title = params['title'] = level_title + ' ' + rate
        json.dump(params, r)
    #bg、preview复制
    shutil.copy(temp_path + bg, rate_path + bg)
    shutil.copy(temp_path + prev, rate_path + prev)
    #压缩
    zip_dir(rate_path, level_out_path)
    shutil.copy(level_out_path, level_name + '_%s.cytoidlevel' % rate)
    #清除缓存
    shutil.rmtree(temp_path)
    os.remove(level_out_path)


def generate1():
    chart = chartget.get()
    rate = rateget.get()
    filepath = fileget.get()
    if chart == 'extreme' or chart == 'Extreme':
        order = 0
    elif  chart == 'hard' or chart == 'Hard':
        order = 1
    elif chart == 'easy' or chart == 'Easy':
        order = 2
    else:
        order = 0
    level_path = filepath
    rater(order, rate, level_path)
    tkinter.messagebox.showinfo(title="Successed!", message="Have a cake?")
    path = os.path.abspath('./')
    os.system("start explorer %s" % path)
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
generate = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=generate1,
    relief="flat"
)
generate.place(
    x=90.0,
    y=424.0,
    width=332.0,
    height=69.0
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    129.5,
    394.0,
    image=entry_image_1
)
rateget = Entry(
    bd=0,
    bg="#676A85",
    fg="white",
    highlightthickness=0
)
rateget.place(
    x=90.0,
    y=377.0,
    width=79.0,
    height=32.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    251.5,
    241.5,
    image=entry_image_2
)
fileget = Entry(
    bd=0,
    bg="#676A85",
    fg="white",
    highlightthickness=0
)
fileget.place(
    x=88.5,
    y=226.0,
    width=326.0,
    height=29.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    133.0,
    314.5,
    image=entry_image_3
)
chartget = Entry(
    bd=0,
    bg="#676A85",
    fg="white",
    highlightthickness=0
)
chartget.place(
    x=91.5,
    y=296.0,
    width=83.0,
    height=35.0
)

canvas.create_text(
    105.0,
    40.0,
    anchor="nw",
    text="Cytoid Level\nSpeed Changer",
    fill="#FFFFFF",
    font=("K2D Regular", 50 * -1)
)

canvas.create_text(
    83.0,
    193.0,
    anchor="nw",
    text="File Path",
    fill="#FFFFFF",
    font=("K2D ExtraBold", 20 * -1)
)

canvas.create_text(
    83.0,
    267.0,
    anchor="nw",
    text="Chart Select",
    fill="#FFFFFF",
    font=("K2D ExtraBold", 20 * -1)
)

canvas.create_text(
    83.0,
    347.0,
    anchor="nw",
    text="Rate",
    fill="#FFFFFF",
    font=("K2D ExtraBold", 20 * -1)
)

canvas.create_text(
    231.0,
    303.0,
    anchor="nw",
    text="Available options are:\nExtreme, Hard, Easy;\nNo fill in means Extreme",
    fill="#FFFFFF",
    font=("K2D ExtraBold", 14 * -1)
)
#输入
def selectpath():
    output_path = filedialog.askopenfilename()
    fileget.insert(0, output_path)
button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
filetaken = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command= selectpath,
    relief="flat"
)
filetaken.place(
    x=386.0,
    y=229.0,
    width=32.0,
    height=27.0
)

window.resizable(False, False)
window.mainloop()
