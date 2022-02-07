from pydub import AudioSegment  # 先导入这个模块
import json,os,re
import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.withdraw()
dic_music = {}
dic_docName = {}
with open(rf"音效对照.csv", "r") as f:
    contentList = f.readlines()
    for content in contentList:
        docName = content.split(",")[0]
        docChineseName = content.split(",")[1]
        if len(docChineseName) > 0:
            dic_docName[docName] = docChineseName
print(dic_docName)
with open(rf"D:\work\python\received\00f977080681e6a10a247a7959f82932.json","r") as f:
    file = f.read()
    # file_name = re.findall(r'([a-z0-9]+\.ogg)"\],"autoDecode":[a-zA-Z]{4,6},"devKey":"([a-zA-Z0-9\_]+)"\}',file)
    file_name = re.findall(r'([a-z0-9]+\.ogg)".+?"devKey":"([a-zA-Z0-9\_]+)"', file)
    jsons_file_name = re.findall(r'([a-z0-9]+\.json)".+?"devKey":"([a-zA-Z0-9\_]+)"', file)
    for file_names in file_name:
        dic_music[file_names[0]] = file_names[1]
    for file_names in jsons_file_name:
        dic_music[file_names[0]] = file_names[1]
    print(dic_music)
    Folderpath = filedialog.askdirectory()
    path = Folderpath
    for root, dirs, files_list in os.walk(path):
        for files in files_list:
            file_name_list = files.split(".")
            type_file = file_name_list[-1]
            apath = os.path.join(root, files)
            if files in dic_music.keys():
                new_file_name = os.path.join(root, dic_docName.get(dic_music[files],"") + dic_music[files])
                os.rename(apath,new_file_name+"."+type_file)
                print(files,"=>",dic_docName.get(dic_music[files],"") + dic_music[files]+"."+type_file)
