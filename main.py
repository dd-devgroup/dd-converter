import pyrogram
from pyrogram import Client
from pyrogram import filters
from pyrogram import enums
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from functools import wraps
import yaml

import os
import shutil
import subprocess
import threading
import time

from buttons import *
import aifunctions
import helperfunctions
import mediainfo
import guess
import tormag
import progconv
import others
import tictactoe


# Load config
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# env
bot_token = os.environ.get("TOKEN", "")
api_hash = os.environ.get("HASH", "")
api_id = os.environ.get("ID", "")


# bot
app = Client("my_bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token)
MESGS = {}

# Subscription check decorator
def check_subscription(func):
    @wraps(func)
    async def wrapper(client, message):
        news_channel_id = config['telegram']['news_channel_id']
        if news_channel_id.startswith('https://t.me/'):
            news_channel_id = '@' + news_channel_id.split('/')[-1]
        try:
            await client.get_chat_member(chat_id=news_channel_id, user_id=message.from_user.id)
        except UserNotParticipant:
            await message.reply_text(
                f"Для использования бота, пожалуйста, подпишитесь на наш новостной канал: {config['telegram']['news_channel_id']}"
            )
            return
        await func(client, message)
    return wrapper

# msgs functions
def saveMsg(msg, msg_type):
    MESGS[msg.from_user.id] = [msg, msg_type]

def getSavedMsg(msg):
    return MESGS.get(msg.from_user.id, [None, None])

def removeSavedMsg(msg):
    if msg.from_user.id in MESGS:
        del MESGS[msg.from_user.id]


# main function to follow
def follow(message,inputt,new,old,oldmessage):
    output = helperfunctions.updtname(inputt,new)


    # ffmpeg videos audios
    if (output.upper().endswith(VIDAUD) or new == "gif") and inputt.upper().endswith(VIDAUD):

        print("It is VID/AUD option")

        file,msg = down(message)
        srclink = helperfunctions.videoinfo(file)
        cmd = helperfunctions.ffmpegcommand(file,output,new)

        if msg != None:
            app.edit_message_text(message.chat.id, msg.id, 'Конвертация... ⏳')

        os.system(cmd)
        os.remove(file)
        conlink = helperfunctions.videoinfo(output)

        if os.path.exists(output) and os.path.getsize(output) > 0:
            caption=f'**Исходный файл**: `{srclink}`\n\n**Результат**: `{conlink}`'
            app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
            up(message,output,msg,capt=caption)
        else:
            app.send_message(message.chat.id,"❌ Ошибка во время конвертации", reply_to_message_id=message.id)
            
        if os.path.exists(output):
            os.remove(output)   


    # images
    elif output.upper().endswith(IMG) and inputt.upper().endswith(IMG):

        print("It is IMG option")
        file = app.download_media(message)
        srclink = helperfunctions.imageinfo(file)
        cmd = helperfunctions.magickcommand(file,output,new)
        os.system(cmd)
        conlink = helperfunctions.imageinfo(output)

        if os.path.exists(output) and os.path.getsize(output) > 0:
            app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
            app.send_document(message.chat.id,document=output, force_document=True,
                              caption=f'**Исходный файл**: `{srclink}`\n\n**Результат**: `{conlink}`',
                              reply_to_message_id=message.id)
        else:
            app.send_message(message.chat.id,"❌ Ошибка во время конвертации", reply_to_message_id=message.id)

        if os.path.exists(output):
            os.remove(output) 

        if new == "ocr":
            cmd = helperfunctions.tesrctcommand(file,message.id)
            os.system(cmd)
            with open(f"{message.id}.txt","r") as ocr:
                text = ocr.read()
            os.remove(f"{message.id}.txt")
            if text != "":
                app.send_message(message.chat.id, text, reply_to_message_id=message.id)
            
        if new == "ico":
            slist = ["256", "128", "96", "64", "48", "32", "16"]
            for ele in slist:
                toutput = helperfunctions.updtname(inputt,f"{ele}.png")
                os.remove(toutput)
        
        os.remove(file)


    # stickers
    elif output.upper().endswith(IMG) and inputt.upper().endswith("TGS"):

        if new == "webp" or new == "gif" or new == "png":

            print("It is Animated Sticker option")
            file = app.download_media(message)
            srclink = helperfunctions.imageinfo(file)        
            os.system(f'./tgsconverter "{file}" "{new}"')
            os.remove(file)
            output = helperfunctions.updtname(file,new)
            conlink = helperfunctions.imageinfo(output)

            if os.path.exists(output) and os.path.getsize(output) > 0:
                app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
                app.send_document(message.chat.id,document=output, force_document=True,
                                  caption=f'**Исходный файл**: `{srclink}`\n\n**Результат**: `{conlink}`',
                                  reply_to_message_id=message.id)
            else:
                app.send_message(message.chat.id,"❌ Ошибка во время конвертации", reply_to_message_id=message.id)

            if os.path.exists(output):
                os.remove(output)

        else:
            app.send_message(message.chat.id,
                 "Доступные преобразования для анимированных стикеров: только **GIF, PNG** и **WEBP**",
                 reply_to_message_id=message.id)


    # ebooks
    elif output.upper().endswith(EB) and inputt.upper().endswith(EB):

        print("It is Ebook option")
        file = app.download_media(message)
        cmd = helperfunctions.calibrecommand(file,output)
        os.system(cmd)
        os.remove(file)

        if os.path.exists(output) and os.path.getsize(output) > 0:
            app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
            app.send_document(message.chat.id, document=output, force_document=True, reply_to_message_id=message.id)
        else:
            app.send_message(message.chat.id,"❌ Ошибка во время конвертации", reply_to_message_id=message.id)
            
        if os.path.exists(output):
            os.remove(output) 


    # libreoffice documents
    elif (output.upper().endswith(LBW) and inputt.upper().endswith(LBW)) or (output.upper().endswith(LBI) and inputt.upper().endswith(LBI)) or (output.upper().endswith(LBC) and inputt.upper().endswith(LBC)):
        
        print("It is LibreOffice option")
        file = app.download_media(message)
        cmd = helperfunctions.libreofficecommand(file,new)
        subprocess.run([cmd],env={"HOME": "."},)
        os.remove(file)

        if os.path.exists(output) and os.path.getsize(output) > 0:
            app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
            app.send_document(message.chat.id,document=output, force_document=True, reply_to_message_id=message.id)
        else:
            app.send_message(message.chat.id,"❌ Ошибка во время конвертации", reply_to_message_id=message.id)
        
        if os.path.exists(output):
            os.remove(output) 


    # fonts
    elif output.upper().endswith(FF) and inputt.upper().endswith(FF):
        
        print("It is FontForge option")
        file = app.download_media(message)
        cmd = helperfunctions.fontforgecommand(file,output,message)
        os.system(cmd)
        os.remove(f"{message.id}-convert.pe")
        os.remove(file)

        if os.path.exists(output) and os.path.getsize(output) > 0:
            app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
            app.send_document(message.chat.id,document=output, force_document=True, reply_to_message_id=message.id)
        else:
            app.send_message(message.chat.id,"❌ Ошибка во время конвертации", reply_to_message_id=message.id)
            
        if os.path.exists(output):
            os.remove(output) 

    
    # subtitles
    elif output.upper().endswith(SUB) and inputt.upper().endswith(SUB):

        if not ((old.upper() in ["TTML", "SCC", "SRT"]) and (new.upper() in ["TTML","SRT", "VTT"])):
            app.send_message(message.chat.id,f"**{old.upper()}** to **{new.upper()}** is not Supported.\n\n**Supported Formats**\n**Inputs**: TTML, SCC & SRT\n**Outputs**: TTML, SRT & VTT", reply_to_message_id=message.id)

        else:
            print("It is Subtitles option")
            file = app.download_media(message)
            cmd = helperfunctions.subtitlescommand(file,output)
            os.system(cmd)
            os.remove(file)

            if os.path.exists(output) and os.path.getsize(output) > 0:
                app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
                app.send_document(message.chat.id,document=output, force_document=True, reply_to_message_id=message.id)
            else:
                app.send_message(message.chat.id,"❌ Ошибка во время конвертации", reply_to_message_id=message.id)
                
            if os.path.exists(output):
                os.remove(output)


    # programs
    elif output.upper().endswith(PRO) and inputt.upper().endswith(PRO):

        flag = 0
        if ((old.upper() == "C") and (new.upper() == "GO")):
            flag = 1

        elif ((old.upper() == "PY") and (new.upper() in ['CPP','RS','JL','KT','NIM','DART','GO'])):
            flag = 2
            extens = ['CPP','RS','JL','KT','NIM','DART','GO']
            langs = ['cpp','rust','julia','kotlin','nim','dart','go']
            for i in range(len(langs)):
                if new.upper() == extens[i]:
                    lang = langs[i]

        elif ((old.upper() == "JAVA") and (new.upper() in ["JS","TS"])):
            flag = 3
            lang = new.upper()

        if not flag:
            app.send_message(message.chat.id, f"**{old.upper()}** в **{new.upper()}** не поддерживается.\n\
            \n**Поддерживаемые форматы:**\nC -> GO\nPY -> CPP, RS, JL, KT, NIM, DART & GO\nJAVA -> JS & TS",
                             reply_to_message_id=message.id)
        else:
            print("It is Programs option")
            file = app.download_media(message)

            if flag == 1:
                output = progconv.c2Go(file)
            elif flag == 2:
                output = progconv.py2Many(file,lang)
            elif flag == 3:
                with open(file,"r") as jfile:
                    javacode = jfile.read()
                info = progconv.java2JSandTS(javacode,lang)
                if info[0] == 1:
                    with open(output,"w") as pfile:
                        pfile.write(info[1])
                else:
                    errormessage = ""
                    for ele in info[1]:
                        errormessage = errormessage + ele + "\n"

            os.remove(file)

            if os.path.exists(output) and os.path.getsize(output) > 0:
                app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
                app.send_document(message.chat.id,document=output, force_document=True, reply_to_message_id=message.id)
            else:
                if flag != 3:
                    errormessage = "Ошибка во время конвертации"
                app.send_message(message.chat.id,f"`{errormessage}`", reply_to_message_id=message.id)
                
            if os.path.exists(output):
                os.remove(output)


    # 3D files
    elif output.upper().endswith(T3D) and inputt.upper().endswith(T3D):

        if (old.upper() == "WRL"):
            app.send_message(message.chat.id,
                             f"**{old.upper()}** доступен только для экспорта, нельзя использовать для конвертации из этого формата",
                             reply_to_message_id=message.id)
        else:
            print("It is 3D files option")
            file = app.download_media(message)
            cmd = helperfunctions.ctm3dcommand(file,output)
            os.system(cmd)
            os.remove(file)

            if os.path.exists(output) and os.path.getsize(output) > 0:
                app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
                app.send_document(message.chat.id,document=output, force_document=True, reply_to_message_id=message.id)
            else:
                app.send_message(message.chat.id,"❌ Ошибка во время конвертации", reply_to_message_id=message.id)
                
            if os.path.exists(output):
                os.remove(output)


    # or else
    else:
        app.send_message(message.chat.id,"Выберите допустимое расширение, не вводите его вручную.", reply_to_message_id=message.id)


    # deleting message    
    app.delete_messages(message.chat.id,message_ids=oldmessage.id)


# negative to positive
def negetivetopostive(message,oldmessage):
    file = app.download_media(message)
    output = file.split("/")[-1]

    try:
        print("using c41lab")
        os.system(f'./c41lab.py "{file}" "{output}"')
        app.send_document(message.chat.id,document=output, force_document=True,caption="used tool -> **c41lab**", reply_to_message_id=message.id)
        os.remove(output)
    except: pass

    try: 
        print("using simple tool")
        aifunctions.positiver(file,output)
        app.send_document(message.chat.id,document=output, force_document=True,caption="used tool -> **openCV**", reply_to_message_id=message.id)
        os.remove(output)
    except: pass
    
    try:
        print("using negfix8")
        os.system(f'./negfix8 "{file}" "{output}"')
        app.send_document(message.chat.id,document=output, force_document=True,caption="used tool -> **negfix8**", reply_to_message_id=message.id)
        os.remove(output)
    except: pass

    os.remove(file)
    app.delete_messages(message.chat.id,message_ids=oldmessage.id)


# color image
def colorizeimage(message,oldmessage):
    file = app.download_media(message)
    output = file.split("/")[-1]

    try:
        aifunctions.deoldify(file,output)
        app.send_document(message.chat.id,document=output, force_document=True,caption="used tool -> **Deoldify**", reply_to_message_id=message.id)
        os.remove(output)
    except: pass

    try:
        aifunctions.colorize_image(output,file)
        app.send_document(message.chat.id,document=output, force_document=True,caption="used tool -> **Local Model**", reply_to_message_id=message.id)
        os.remove(output)
    except: pass

    os.remove(file)
    app.delete_messages(message.chat.id,message_ids=oldmessage.id)


# dalle
def genrateimages(message,prompt,msg):
    
    # dalle mini
    filelist = aifunctions.dallemini(prompt)
    app.send_message(message.chat.id,"**DALLE MINI**", reply_to_message_id=message.id)
    for ele in filelist:
        app.send_document(message.chat.id,document=ele,force_document=True)
        os.remove(ele)
    os.rmdir(prompt)

    # satbility ai
    filelist = aifunctions.stabilityAI(prompt)
    app.send_message(message.chat.id,"**STABLE DIFFUSION**", reply_to_message_id=message.id)
    for ele in filelist:
        app.send_document(message.chat.id,document=ele,force_document=True)
        os.remove(ele)

    # delete msg
    app.delete_messages(message.chat.id,message_ids=msg.id)


# riffusion
def genratemusic(message,prompt,msg):
    musicfile, thumbfile = aifunctions.riffusion(prompt)
    app.send_audio(message.chat.id, musicfile, duration=10, performer="Riffusion", title=prompt, thumb=thumbfile, reply_to_message_id=message.id)
    
    os.remove(musicfile)
    os.remove(thumbfile)
    app.delete_messages(message.chat.id,message_ids=msg.id)


# cog video
def genratevideos(message,prompt):

    hash, queuepos = aifunctions.cogvideo(prompt,AutoCall=False)
    msg = app.send_message(message.chat.id,f"**Prompt received and Request is sent. Expected waiting time is {(queuepos+1)*3} mins**", reply_to_message_id=message.id)

    file = aifunctions.cogvideostatus(hash,prompt)
    app.send_video(message.chat.id, video=file, reply_to_message_id=message.id) #,caption=f"COGVIDEO : {prompt}")
    os.remove(file)
    app.delete_messages(message.chat.id,message_ids=msg.id)


# delete msg
async def dltmsg(umsg,rmsg,sec=15):
    time.sleep(sec)
    await app.delete_messages(umsg.chat.id,message_ids=[umsg.id,rmsg.id])


# read file
def readf(message,oldmessage):
    file = app.download_media(message)
    
    try:
        with open(file,"r", encoding="utf-8") as rf:
            txt = rf.read()
        n = 4096
        split = [txt[i:i+n] for i in range(0, len(txt), n)]

        if len(split) > 10:
            app.send_message(message.chat.id, "Содержимое файла слишком длинное", reply_to_message_id=message.id)
            return

        for ele in split:
            app.send_message(message.chat.id, ele, disable_web_page_preview=True, reply_to_message_id=message.id)
            time.sleep(3)   
    except Exception as e:
            app.send_message(message.chat.id, f"❌ Ошибка во время чтении файла : {e}", reply_to_message_id=message.id)

    os.remove(file)
    app.delete_messages(message.chat.id,message_ids=oldmessage.id)


# send video
def sendvideo(message,oldmessage):
    file, msg = down(message)
    thumb,duration,width,height = mediainfo.allinfo(file)
    up(message, file, msg, video=True, capt=f'**{file.split("/")[-1]}**' ,
       thumb=thumb, duration=duration, height=height, widht=width)

    app.delete_messages(message.chat.id, message_ids=oldmessage.id)
    os.remove(file)


# send document
def senddoc(message,oldmessage):
    file, msg = down(message)
    up(message, file, msg)

    app.delete_messages(message.chat.id, message_ids=oldmessage.id)
    os.remove(file)


# send photo
def sendphoto(message,oldmessage):
    file = app.download_media(message)
    app.send_photo(message.chat.id, photo=file, reply_to_message_id=message.id)
    app.delete_messages(message.chat.id,message_ids=oldmessage.id)
    os.remove(file)


def extract(message, oldm):
    file, msg = down(message)
    cmd, foldername, infofile = helperfunctions.zipcommand(file, message)
    if msg != None:
        app.edit_message_text(message.chat.id, msg.id, 'Извлечение... 📂')
    os.system(cmd)
    os.remove(file)

    with open(infofile, 'r') as f:
        lines = f.read()
    last = lines.split("Everything is Ok\n\n")[-1].replace("      ", "")
    os.remove(infofile)

    if os.path.exists(foldername):
        dir_list = helperfunctions.absoluteFilePaths(foldername)
        if len(dir_list) > 30:
            if msg != None:
                app.delete_messages(message.chat.id, message_ids=msg.id)
            app.send_message(message.chat.id,
                             f"Количество файлов: **{len(dir_list)}**, что превышает лимит в **30** файлов",
                             reply_to_message_id=message.id)
        else:
            for ele in dir_list:
                if os.path.getsize(ele) > 0:
                    up(message, ele, msg, multi=True)
                    os.remove(ele)
                else:
                    app.send_message(message.chat.id,
                                     f'**{ele.split("/")[-1]}** пропущен, так как имеет размер 0 байт',
                                     reply_to_message_id=message.id)

            if msg != None:
                app.delete_messages(message.chat.id, message_ids=msg.id)
            app.send_message(message.chat.id, f'`{last}`', reply_to_message_id=message.id)

        shutil.rmtree(foldername)
    else:
        app.send_message(message.chat.id, "**Невозможно извлечь**", reply_to_message_id=message.id)

    app.delete_messages(message.chat.id, message_ids=oldm.id)


# getting magnet
def getmag(message,oldm):
    file = app.download_media(message)
    maglink = tormag.getMagnet(file)
    app.send_message(message.chat.id, f'`{maglink}`', reply_to_message_id=message.id)
    app.delete_messages(message.chat.id,message_ids=oldm.id)
    os.remove(file)


# getting tor file
def gettorfile(message,oldm):
    file = tormag.getTorFile(message.text)
    app.send_document(message.chat.id, file, reply_to_message_id=message.id)
    app.delete_messages(message.chat.id,message_ids=oldm.id)
    os.remove(file)


# compiling
def compile(message,oldm):
    ext = message.document.file_name.split(".")[-1]

    # jar compilation
    if ext.upper() == "JAR":
        file = app.download_media(message)
        cmd,folder,files = helperfunctions.warpcommand(file,message)
        os.system(cmd)
        if not os.path.exists(folder):
            cmd,folder,files = helperfunctions.warpcommand(file,message,True)
            os.system(cmd)

        os.remove(file)
        if os.path.exists(folder):
            app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
            for ele in files:
                if os.path.exists(ele) and os.path.getsize(ele) > 0:
                    app.send_document(message.chat.id,document=ele, force_document=True, reply_to_message_id=message.id)
                os.remove(ele)
            shutil.rmtree(folder)
        else:
            app.send_message(message.chat.id,"❌ Ошибка во время компиляции", reply_to_message_id=message.id)


    # c and c++ compilation
    elif ext.upper() in ['C','CPP']:
        file = app.download_media(message)
        cmd,output = helperfunctions.gppcommand(file)
        os.system(cmd)
        os.remove(file)
        if os.path.exists(output) and os.path.getsize(output) > 0:
            app.send_document(message.chat.id,document=output, caption="Исполняемый файл Linux", force_document=True, reply_to_message_id=message.id)
            os.remove(output)
        else:
            app.send_message(message.chat.id,"❌ Ошибка во время компиляции", reply_to_message_id=message.id)
        

    # python compile
    elif ext.upper() == "PY":
        file = app.download_media(message)
        cmd, output, ofold, tfold, temp = helperfunctions.pyinstallcommand(message,file)
        os.system(cmd)
        os.remove(file)
        if os.path.exists(output) and os.path.getsize(output) > 0:
            app.send_document(message.chat.id,document=output, caption="Исполняемый файл Linux", force_document=True, reply_to_message_id=message.id)
            os.remove(output)
        else:
            app.send_message(message.chat.id,"❌ Ошибка во время компиляции", reply_to_message_id=message.id)
        
        if os.path.exists(temp):
            os.remove(temp)
        if os.path.exists(ofold):
            shutil.rmtree(ofold)
        if os.path.exists(tfold):
            shutil.rmtree(tfold)


    # not supported yet
    else:
        app.send_message(message.chat.id,"В настоящее время компиляция поддерживается только из файлов JAR, PY, C и CPP.", reply_to_message_id=message.id)


    # delete message
    app.delete_messages(message.chat.id,message_ids=oldm.id)


# running a program
def runpro(message,oldm):
    ext = message.document.file_name.split(".")[-1]

    # python run
    if ext.upper() == "PY":
        file = app.download_media(message)
        code = open(file,"r",encoding="utf-8").read()
        os.remove(file)
        info = others.pyrun(code)
        app.send_message(message.chat.id, info, reply_to_message_id=message.id)
        app.delete_messages(message.chat.id,message_ids=oldm.id)
        

    # not supported yet
    else:
        app.send_message(message.chat.id,"В настоящее время запуск поддерживается только из файлов PY.", reply_to_message_id=message.id)


# bg remove
def bgremove(message,oldm):
    file = app.download_media(message)
    ofile = aifunctions.bg_remove(file)
    os.remove(file)
    app.send_document(message.chat.id, ofile, reply_to_message_id=message.id)
    app.delete_messages(message.chat.id,message_ids=oldm.id)
    os.remove(ofile)


# scanning
def scan(message,oldm):
    file = app.download_media(message)
    info = helperfunctions.scanner(file)
    app.send_message(message.chat.id,f"`{info}`", reply_to_message_id=message.id)
    app.delete_messages(message.chat.id,message_ids=oldm.id)
    os.remove(file)


# make file
def makefile(message,mtext,oldmessage):
    text = mtext.split("\n")
    if len(text) == 1:
        app.send_message(message.chat.id,
                         "Make-File берет первую строку вашего текста в качестве имени файла, "
                         "а содержимое файла начинается со второй строки",
                         reply_to_message_id=message.id)
        return

    firstline = text[0]
    firstline = "".join( x for x in firstline if (x.isalnum() or x in "._-@ "))
    text.remove(text[0])
    
    mtext = ""
    for ele in text: 
        mtext = mtext + f"{ele}\n"
    
    with open(firstline,"w") as file:
        file.write(mtext)

    if os.path.exists(firstline) and os.path.getsize(firstline) > 0:
        app.send_document(message.chat.id, document=firstline, reply_to_message_id=message.id)
    else:
        app.send_message(message.chat.id, "❌ Ошибка при создании файла", reply_to_message_id=message.id)

    app.delete_messages(message.chat.id,message_ids=oldmessage.id)
    os.remove(firstline)      	    


# transcript speech to text
def transcript(message,oldmessage):
    file = app.download_media(message)
    inputt = file.split("/")[-1]
    output = helperfunctions.updtname(inputt,"wav")
    temp = helperfunctions.updtname(inputt,"txt")
        
    if file.endswith("wav"):
        aifunctions.splitfn(file,message,temp)
    else:
        cmd = helperfunctions.ffmpegcommand(file,output,"wav")
        os.system(cmd)
        aifunctions.splitfn(output,message,temp)
        os.remove(output)

    if os.path.getsize(temp) > 0:
        app.send_document(message.chat.id, document=temp,caption="**Google Engine**", reply_to_message_id=message.id)
    os.remove(temp)

    data = aifunctions.whisper(file)
    if data is not None:
        with open(temp,"w") as wfile:
            wfile.write(data)
        if os.path.getsize(temp) > 0:
            app.send_document(message.chat.id, document=temp,caption="**OpenAI Engine** (whisper)", reply_to_message_id=message.id)
        os.remove(temp)

    app.delete_messages(message.chat.id,message_ids=oldmessage.id)
    os.remove(file)
    

# text to 3d
def textTo3d(prompt,message,msg):
    htmlfile = aifunctions.pointE(prompt)
    app.send_document(message.chat.id, htmlfile, reply_to_message_id=message.id)
    app.delete_messages(message.chat.id, message_ids=msg.id)
    os.remove(htmlfile)


# text to speech 
def speak(message,oldmessage):
    file = app.download_media(message)
    inputt = file.split("/")[-1]
    output = helperfunctions.updtname(inputt,"mp3")
   
    aifunctions.texttospeech(file,output)
    os.remove(file)

    app.send_document(message.chat.id, document=output, reply_to_message_id=message.id)
    app.delete_messages(message.chat.id,message_ids=oldmessage.id)
    os.remove(output)


# upscaling
def increaseres(message,oldmessage):
    file = app.download_media(message)
    inputt = file.split("/")[-1]
   
    try:
        aifunctions.upscale(file,inputt)
        os.remove(file)
        app.send_document(message.chat.id, document=inputt, reply_to_message_id=message.id)
    except Exception as e:
        app.send_message(message.chat.id, f"❌ Error : {e}", reply_to_message_id=message.id)
        
    app.delete_messages(message.chat.id,message_ids=oldmessage.id)
    os.remove(inputt)


# renaming
def rname(message,newname,oldm):
    app.delete_messages(message.chat.id,message_ids=message.id+1)
    file, msg = down(message)
    os.rename(file,newname)
    up(message, newname, msg)
    app.delete_messages(message.chat.id,message_ids=oldm.id)
    os.remove(newname)


# save restricted
def saverec(message):
    
    if "https://t.me/c/" in message.text:
        app.send_message(message.chat.id, "**Присылайте мне только ссылки на публичные каналы**",
                         reply_to_message_id=message.id)
        return

    datas = message.text.split("/")
    msgid = int(datas[-1])
    username = datas[-2]
    msg  = app.get_messages(username,msgid)
    app.copy_message(message.chat.id, msg.chat.id, msg.id)


# AI chat
def handleAIChat(message):
    if not config['features']['ai_chat']:
        app.send_message(message.chat.id, "Эта функция отключена.", reply_to_message_id=message.id)
        return
    hash = str(message.chat.id)
    if hash[0] == "-": hash = str(hash)[1:]

    app.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    reply = aifunctions.chatWithAI(message.text, hash)
    if reply != None: app.send_message(message.chat.id, reply, reply_to_message_id=message.id)
    else: app.send_chat_action(message.chat.id, enums.ChatAction.CANCEL)


# bloom
def handelbloom(para,message,msg):
    ans = aifunctions.bloom(para)
    if ans is not None: app.send_message(message.chat.id, f'`{ans}`', reply_to_message_id=message.id)
    app.delete_messages(message.chat.id, message_ids=msg.id)


# others
def other(message):
    if not config['features']['other_utils']:
        handleAIChat(message)
        return

    # time date
    if message.text in ["time","Time",'date','Date']:
        app.send_message(message.chat.id, others.timeanddate(), reply_to_message_id=message.id)
    
    # b64 decode
    elif message.text[:5] == "b64d ":
        try:
            app.send_message(message.chat.id, f'`{others.b64d(message.text[5:])}`', reply_to_message_id=message.id)
        except:
            app.send_message(message.chat.id, "Invalid", reply_to_message_id=message.id)

    # b64 encode
    elif message.text[:5] == "b64e ":
        try:
            app.send_message(message.chat.id, f'`{others.b64e(message.text[5:])}`', reply_to_message_id=message.id)
        except:
            app.send_message(message.chat.id, "Invalid", reply_to_message_id=message.id)

    # maths
    elif not message.text.isalnum():
        info = others.maths(message.text)
        if info != None:
            app.send_message(message.chat.id, info, reply_to_message_id=message.id)
        else:
            handleAIChat(message)
    
    # AI chat
    else:
        handleAIChat(message)

# download with progress
def down(message):

    try:
        size = int(message.document.file_size)
    except:
        try:
            size = int(message.video.file_size)
        except:
            size = 1

    if size > 25000000:
        msg = app.send_message(message.chat.id, 'Скачивание... 📥', reply_to_message_id=message.id)
        dosta = threading.Thread(target=lambda:downstatus(f'{message.id}downstatus.txt',msg),daemon=True)
        dosta.start()
    else:
        msg = None

    file = app.download_media(message,progress=dprogress, progress_args=[message])
    if os.path.exists(f'{message.id}downstatus.txt'):
        os.remove(f'{message.id}downstatus.txt')
    return file,msg


# uploading with progress
def up(message, file, msg, video=False, capt="", thumb=None, duration=0, widht=0, height=0, multi=False):

    if msg != None:
        try:
            app.edit_message_text(message.chat.id, msg.id, 'Загрузка... 📤')
        except:
            pass
        
    if os.path.getsize(file) > 25000000:
        upsta = threading.Thread(target=lambda:upstatus(f'{message.id}upstatus.txt',msg),daemon=True)
        upsta.start()

    if not video:
        app.send_document(message.chat.id, document=file, caption=capt, force_document=True ,reply_to_message_id=message.id, progress=uprogress, progress_args=[message])    
    else:
        app.send_video(message.chat.id, video=file, caption=capt, thumb=thumb, duration=duration, width=widht, height=height, reply_to_message_id=message.id, progress=uprogress, progress_args=[message]) 

    if thumb != None:
        os.remove(thumb)
    if os.path.exists(f'{message.id}upstatus.txt'):   
        os.remove(f'{message.id}upstatus.txt')

    if msg != None and not multi:
        app.delete_messages(message.chat.id,message_ids=msg.id)


# up progress
def uprogress(current, total, message):
    with open(f'{message.id}upstatus.txt',"w") as fileup:
        fileup.write(f"{current * 100 / total:.1f}%")


# down progress
def dprogress(current, total, message):
    with open(f'{message.id}downstatus.txt',"w") as fileup:
        fileup.write(f"{current * 100 / total:.1f}%")


# upload status
def upstatus(statusfile,message):

    while True:
        if os.path.exists(statusfile):
            break
        
    time.sleep(5)
    while os.path.exists(statusfile):

        with open(statusfile,"r") as upread:
            txt = upread.read()

        try:
            app.edit_message_text(message.chat.id, message.id, f"Загружено : **{txt}**")
            time.sleep(10)
        except:
            time.sleep(5)


# download status
def downstatus(statusfile,message):

    while True:
        if os.path.exists(statusfile):
            break
        
    time.sleep(5)
    while os.path.exists(statusfile):

        with open(statusfile,"r") as upread:
            txt = upread.read()
        
        try:
            app.edit_message_text(message.chat.id, message.id, f"Скачано : **{txt}**")
            time.sleep(10)
        except:
            time.sleep(5)


# app messages
@app.on_message(filters.command(['start']))
async def start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    await app.send_message(message.chat.id, f"👋 Добро пожаловать, {message.from_user.mention}!\n"
                                      f"Отправьте мне **файл**, а затем выберите **расширение** для конвертации.\n\n"
                                      f"🧐 Хотите узнать больше обо мне?\n"
                                      f"Используйте /help, чтобы получить список команд.\n"
                                      f"Используйте /detail, чтобы получить список поддерживаемых расширений.",
                                    reply_to_message_id=message.id)


# detail
@app.on_message(filters.command(['detail']))
@check_subscription
async def detail(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    oldm = await app.send_message(message.chat.id, START_TEXT, reply_to_message_id=message.id)
    dm = threading.Thread(target=lambda:dltmsg(message,oldm,30),daemon=True)
    dm.start()  
    

# help
@app.on_message(filters.command(['help']))
async def help_command(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    help_text = "Доступные команды:\n\n" \
                "/start - 🚀 Начало работы\n" \
                "/help - ℹ️ Справка\n" \
                "/detail - 📋 Поддерживаемые расширения\n"
    if config['features']['imagegen']:
        help_text += "/imagegen - 🎨 Текст в изображение\n"
    if config['features']['musicgen']:
        help_text += "/musicgen - 🎵 Текст в музыку\n"
    if config['features']['3dgen']:
        help_text += "/3dgen - 🧊 Текст в 3D\n"
    if config['features']['bloom']:
        help_text += "/bloom - ✍️ AI-генератор статей\n"
    help_text += "/cancel - ❌ Отмена\n" \
                 "/rename - ✏️ Переименовать файл\n" \
                 "/read - 📖 Прочитать файл\n" \
                 "/make - 📝 Создать файл\n"
    if config['features']['guess']:
        help_text += "/guess - 🤔 Бот угадает\n"
    if config['features']['tictactoe']:
        help_text += "/tictactoe - 🕹️ Игра в крестики-нолики\n"
    help_text += "/support - 👨‍💻 Поддержка"
    
    oldm = await app.send_message(message.chat.id, help_text, reply_to_message_id=message.id)
    dm = threading.Thread(target=lambda:dltmsg(message,oldm),daemon=True)
    dm.start()


#support
@app.on_message(filters.command(['support']))
async def support(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    support_channel = config['telegram']['support_channel_id']
    oldm = await app.send_message(message.chat.id,
                                  text = f"⚙️ [Поддержка]({support_channel})",
                                  disable_web_page_preview=True,
                                  reply_to_message_id=message.id)
    dm = threading.Thread(target=lambda:dltmsg(message,oldm),daemon=True)
    dm.start() 


# rename
@app.on_message(filters.command(['rename']))
@check_subscription
async def rename(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    try:
        newname = message.text.split("/rename ")[1]
    except:
        await app.send_message(message.chat.id, "Использование: `/rename новое-имя-файла`\n(с указанием расширения)",
                         reply_to_message_id=message.id)
        return

    nmessage, msg_type = getSavedMsg(message)
    if nmessage:
        oldm = await app.send_message(message.chat.id, "**Переименование...**",
                                reply_to_message_id=nmessage.id)
        rn = threading.Thread(target=lambda:rname(nmessage,newname,oldm),daemon=True)
        rn.start()
        removeSavedMsg(message)
    else:
        await app.send_message(message.chat.id, "Сначала нужно отправить мне файл", reply_to_message_id=message.id)


# cancel
@app.on_message(filters.command(['cancel']))
@check_subscription
async def cancel(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    nmessage, msg_type = getSavedMsg(message)
    if nmessage:
        removeSavedMsg(message)
        await app.delete_messages(message.chat.id,message_ids=nmessage.id+1)
        await app.send_message(message.chat.id,"Ваша задача была **Отменена**", reply_to_message_id=message.id)
    else:
        await app.send_message(message.chat.id,"Нет задач для отмены", reply_to_message_id=message.id)


# imagen command
@app.on_message(filters.command(["imagegen"]))
@check_subscription
async def getpompt_image(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if not config['features']['imagegen']:
        await message.reply_text("Эта функция отключена.")
        return
    try:
        prompt = message.text.split("/imagegen ")[1]
    except:
        await app.send_message(message.chat.id,'Отправьте запрос с командой,\nПример: `/imagegen dog with funny hat`', reply_to_message_id=message.id)
        return	

    msg = await app.send_message(message.chat.id,"Запрос получен, ожидание 1-2 минуты...", reply_to_message_id=message.id)
    ai = threading.Thread(target=lambda:genrateimages(message,prompt,msg),daemon=True)
    ai.start()


# music gen
@app.on_message(filters.command(["musicgen"]))
@check_subscription
async def getpompt_music(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if not config['features']['musicgen']:
        await message.reply_text("Эта функция отключена.")
        return
    try:
        prompt = message.text.split("/musicgen ")[1]
    except:
        await app.send_message(message.chat.id,'Отправьте запрос с командой,\nПример: `/musicgen a slow, emotional piano ballad`', reply_to_message_id=message.id)
        return	

    msg = await app.send_message(message.chat.id,"Запрос получен, ожидание 1 минута...", reply_to_message_id=message.id)
    mai = threading.Thread(target=lambda:genratemusic(message,prompt,msg),daemon=True)
    mai.start()


# read command
@app.on_message(filters.command(['read']))
@check_subscription
async def readcmd(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    nmessage, msg_type = getSavedMsg(message)
    if nmessage:
        removeSavedMsg(message)
    else:
        await app.send_message(message.chat.id,'Сначала отправьте мне файл', reply_to_message_id=message.id)
        return

    oldm = await app.send_message(message.chat.id,'Чтение файла... 📖', reply_to_message_id=message.id)
    rf = threading.Thread(target=lambda:readf(nmessage,oldm),daemon=True)
    rf.start()


# make command
@app.on_message(filters.command(['make']))
@check_subscription
async def makecmd(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    nmessage, msg_type = getSavedMsg(message)
    if nmessage:
        removeSavedMsg(message)
        text = nmessage.text
    else:
        try:
            text = str(message.reply_to_message.text)
        except:
            await app.send_message(message.chat.id,'Вам нужно сначала отправить мне текстовое сообщение или ответить на текстовое сообщение', reply_to_message_id=message.id)
            return

    oldm = await app.send_message(message.chat.id,'Создание файла... 📝', reply_to_message_id=message.id)
    mf = threading.Thread(target=lambda:makefile(message,text,oldm),daemon=True)
    mf.start()


# Point E
@app.on_message(filters.command(["3dgen"]))
@check_subscription
async def send_gpt(client: pyrogram.client.Client,message: pyrogram.types.messages_and_media.message.Message,):
    if not config['features']['3dgen']:
        await message.reply_text("Эта функция отключена.")
        return
    try: prompt = message.text.split("/3dgen ")[1]
    except:
        await app.send_message(message.chat.id,'Отправьте запрос с командой,\nПример: `/3dgen a red motorcycle`', reply_to_message_id=message.id)
        return	

    msg = await message.reply_text("3D-моделирование... 🧊", reply_to_message_id=message.id)
    pnte = threading.Thread(target=lambda:textTo3d(prompt,message,msg),daemon=True)
    pnte.start()


# Tic Tac Toe Game
@app.on_message(filters.command("tictactoe"))
@check_subscription
async def startTTT(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if not config['features']['tictactoe']:
        await message.reply_text("Эта функция отключена.")
        return
    if message.chat.id == message.from_user.id: 
		    return tictactoe.TTTgame(app,None,message,1)

    else:
        msg = await app.send_message(message.chat.id, f'Игрок 1 (X) : **{message.from_user.first_name}**',
		reply_markup=InlineKeyboardMarkup(
		[[ InlineKeyboardButton( text='🤵 Игрок 2', callback_data="TTT P2")],
		 [ InlineKeyboardButton( text='🤖 v/s AI', callback_data="TTT AI")]]))
        tictactoe.TTTstoredata(msg.id, p1=message.from_user.id)


# Guess Game
@app.on_message(filters.command(['guess']))
@check_subscription
async def startG(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if not config['features']['guess']:
        await message.reply_text("Эта функция отключена.")
        return
    try:
        N = int(message.text.split("/guess ")[1])
        if N > 1000:
            await app.send_message(message.chat.id,"**Не более 1000**",reply_to_message_id=message.id)
            return
    except: N = 100

    size = len(bin(N).replace("0b", ""))
    await app.send_message(message.chat.id,f"Загадайте число от **1** до **{N}**\nЯ угадаю его за **{size} шагов**\nВы **готовы?**",reply_to_message_id=message.id,
        reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton( text='Да', callback_data='G ready'),
                    InlineKeyboardButton( text='Нет', callback_data='G not')
                ]]))
 

# bloom 
@app.on_message(filters.command("bloom"))
@check_subscription
async def bloomcmd(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if not config['features']['bloom']:
        await message.reply_text("Эта функция отключена.")
        return
    try: para = message.reply_to_message.text
    except:
        try: para = message.text.split("/bloom ")[1]
        except:
            await app.send_message(message.chat.id,'Отправьте текст с командой или ответьте на сообщение\n\nПример: `/bloom A poem about the beauty of science`', reply_to_message_id=message.id)
            return	
    
    msg = await message.reply_text("Генерация... ✍️", reply_to_message_id=message.id)
    blm = threading.Thread(target=lambda:handelbloom(para,message,msg),daemon=True)
    blm.start()


# callback
@app.on_callback_query()
async def inbtwn(client: pyrogram.client.Client, call: pyrogram.types.CallbackQuery):
	if call.data[:4] == "TTT ":
		if config['features']['tictactoe']:
			await tictactoe.TTTgame(app,call,call.message)
	elif call.data[:2] == "G ":
		if config['features']['guess']:
			await guess.Ggame(app,call)


# document
@app.on_message(filters.document)
@check_subscription
async def documnet(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    saveMsg(message, "DOCUMENT")
    dext = message.document.file_name.split(".")[-1].upper()

    # VID / AUD
    if message.document.file_name.upper().endswith(VIDAUD):
        await app.send_message(message.chat.id,
                         f'Обнаружено расширение: **{dext}** 📹 / 🔊\nТеперь отправьте расширение для конвертации...\n\n'
                         f'--**Доступные форматы**-- \n\n`{VA_TEXT}`\n\n{message.from_user.mention} выберите или '
                         f'нажмите /cancel для отмены или используйте /rename для переименования',
                         reply_markup=VAboard, reply_to_message_id=message.id)

    # IMG
    elif message.document.file_name.upper().endswith(IMG):
        await app.send_message(message.chat.id,
                         f'Обнаружено расширение: **{dext}** 📷\nТеперь отправьте расширение для конвертации...\n\n'
                         f'--**Доступные форматы**-- \n\n`{IMG_TEXT}`\n\n'
                         f'{message.from_user.mention} выберите или нажмите /cancel для отмены или используйте '
                         f'/rename для переименования',
                         reply_markup=IMGboard, reply_to_message_id=message.id)

    # LBW
    elif message.document.file_name.upper().endswith(LBW):
        await app.send_message(message.chat.id,
                         f'Обнаружено расширение: **{dext}** 💼 \nТеперь отправьте расширение для конвертации...\n\n--**Доступные форматы**-- \n\n`{LBW_TEXT}`\n\n{message.from_user.mention} выберите или нажмите /cancel для отмены или используйте /rename для переименования',
                         reply_markup=LBWboard, reply_to_message_id=message.id)

    # LBC
    elif message.document.file_name.upper().endswith(LBC):
        await app.send_message(message.chat.id,
                         f'Обнаружено расширение: **{dext}** 💼 \nТеперь отправьте расширение для конвертации...\n\n--**Доступные форматы**-- \n\n`{LBC_TEXT}`\n\n{message.from_user.mention} выберите или нажмите /cancel для отмены или используйте /rename для переименования',
                         reply_markup=LBCboard, reply_to_message_id=message.id)

    # LBI
    elif message.document.file_name.upper().endswith(LBI):
        await app.send_message(message.chat.id,
                         f'Обнаружено расширение: **{dext}** 💼 \nТеперь отправьте расширение для конвертации...\n\n--**Доступные форматы**-- \n\n`{LBI_TEXT}`\n\n{message.from_user.mention} выберите или нажмите /cancel для отмены или используйте /rename для переименования',
                         reply_markup=LBIboard, reply_to_message_id=message.id)

    # FF
    elif message.document.file_name.upper().endswith(FF):
        await app.send_message(message.chat.id,
                         f'Обнаружено расширение: **{dext}** 🔤 \nТеперь отправьте расширение для конвертации...\n\n--**Доступные форматы**-- \n\n`{FF_TEXT}`\n\n{message.from_user.mention} выберите или нажмите /cancel для отмены или используйте /rename для переименования',
                         reply_markup=FFboard, reply_to_message_id=message.id)

    # EB
    elif message.document.file_name.upper().endswith(EB):
        await app.send_message(message.chat.id,
                         f'Обнаружено расширение: **{dext}** 📚 \nТеперь отправьте расширение для конвертации...\n\n--**Доступные форматы**-- \n\n`{EB_TEXT}`\n\n{message.from_user.mention} выберите или нажмите /cancel для отмены или используйте /rename для переименования',
                         reply_markup=EBboard, reply_to_message_id=message.id)

    # ARC
    elif message.document.file_name.upper().endswith(ARC):
        await app.send_message(message.chat.id,
                         f'Обнаружено расширение: **{dext}** 🗄\nХотите извлечь файлы?\n\n{message.from_user.mention} выберите или нажмите /cancel для отмены или используйте /rename для переименования',
                         reply_markup=ARCboard, reply_to_message_id=message.id)

    # TOR
    elif message.document.file_name.upper().endswith("TORRENT"):
        removeSavedMsg(message)
        oldm = await app.send_message(message.chat.id, 'Получение Magnet-ссылки... 🔗', reply_to_message_id=message.id)
        ml = threading.Thread(target=lambda: getmag(message, oldm), daemon=True)
        ml.start()
        return

    # SUB
    elif message.document.file_name.upper().endswith(SUB):
        await app.send_message(message.chat.id,
                         f'Обнаружено расширение: **{dext}** 🗯️ \nТеперь отправьте расширение для конвертации...\n\n--**Доступные форматы**-- \n\n`{SUB_TEXT}`\n\n{message.from_user.mention} выберите или нажмите /cancel для отмены или используйте /rename для переименования',
                         reply_markup=SUBboard, reply_to_message_id=message.id)

    # PRO
    elif message.document.file_name.upper().endswith(PRO):
        await app.send_message(message.chat.id,
                         f'Обнаружено расширение: **{dext}** 👨‍💻 \nТеперь отправьте расширение для конвертации...\n\n--**Доступные форматы**-- \n\n`{PRO_TEXT}`\n\n{message.from_user.mention} выберите или нажмите /cancel для отмены или используйте /rename для переименования',
                         reply_markup=PROboard, reply_to_message_id=message.id)

    # T3D
    elif message.document.file_name.upper().endswith(T3D):
        await app.send_message(message.chat.id,
                         f'Обнаружено расширение: **{dext}** 💠 \nТеперь отправьте расширение для конвертации...\n\n--**Доступные форматы**-- \n\n`{T3D_TEXT}`\n\n{message.from_user.mention} выберите или нажмите /cancel для отмены или используйте /rename для переименования',
                         reply_markup=T3Dboard, reply_to_message_id=message.id)

    # else
    else:
        await app.send_message(message.chat.id,
                         'Доступные конвертации не найдены.\n\nВы можете использовать:\n`/rename новое-имя-файла` для переименования\n`/read` для чтения файла')

# animation
@app.on_message(filters.animation)
@check_subscription
async def annimations(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    oldm = await app.send_message(message.chat.id,'**Преобразую в документ, затем вы сможете использовать его для конвертации**', reply_to_message_id=message.id)
    sd = threading.Thread(target=lambda:senddoc(message,oldm),daemon=True)
    sd.start()


# video
@app.on_message(filters.video)
@check_subscription
async def video(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    try:
        if message.video.file_name.upper().endswith(VIDAUD):
            saveMsg(message, "VIDEO")
            dext = message.video.file_name.split(".")[-1].upper()
            await app.send_message(message.chat.id,
                             f'Обнаружено расширение: **{dext}** 📹 / 🔊\nТеперь отправьте расширение для конвертации...\n\n--**Доступные форматы**-- \n\n`{VA_TEXT}`\n\n{message.from_user.mention} выберите или нажмите /cancel для отмены или используйте /rename для переименования',
                             reply_markup=VAboard, reply_to_message_id=message.id)
        else:
            await app.send_message(message.chat.id, f'--**Доступные форматы**--:\n\n**ВИДЕО/АУДИО** 📹 / 🔊\n`{VA_TEXT}`',
                             reply_to_message_id=message.id)

    except:
        oldm = await app.send_message(message.chat.id,
                                '**Преобразую в документ, затем вы сможете использовать его для конвертации**',
                                )
        sd = threading.Thread(target=lambda: senddoc(message, oldm), daemon=True)
        sd.start()


# video note
@app.on_message(filters.video_note)
@check_subscription
async def videonote(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    saveMsg(message, "VIDEO_NOTE")
    await app.send_message(message.chat.id,
                f'Обнаружено расширение: **MP4** 📹 / 🔊\nТеперь отправьте расширение для конвертации...\n\n--**Доступные форматы**-- \n\n`{VA_TEXT}`\n\n{message.from_user.mention} выберите или нажмите /cancel для отмены или используйте /rename для переименования',
                reply_markup=VAboard, reply_to_message_id=message.id)

# audio
@app.on_message(filters.audio)
@check_subscription
async def audio(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if message.audio.file_name.upper().endswith(VIDAUD):
        saveMsg(message, "AUDIO")
        dext = message.audio.file_name.split(".")[-1].upper()
        await app.send_message(message.chat.id,
                         f'Обнаружено расширение: **{dext}** 📹 / 🔊\nТеперь отправьте расширение для конвертации...\n\n--**Доступные форматы**-- \n\n`{VA_TEXT}`\n\n{message.from_user.mention} выберите или нажмите /cancel для отмены или используйте /rename для переименования',
                         reply_markup=VAboard, reply_to_message_id=message.id)
    else:
        await app.send_message(message.chat.id, f'--**Доступные форматы**--:\n\n**ВИДЕО/АУДИО** 📹 / 🔊 \n`{VIDAUD}`',
                         reply_to_message_id=message.id)

# voice
@app.on_message(filters.voice)
@check_subscription
async def voice(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    saveMsg(message, "VOICE")
    await app.send_message(message.chat.id,
                f'Обнаружено расширение: **OGG** 📹 / 🔊\nТеперь отправьте расширение для конвертации...\n\n--**Доступные форматы**-- \n\n`{VA_TEXT}`\n\n{message.from_user.mention} выберите или нажмите /cancel для отмены или используйте /rename для переименования',
                reply_markup=VAboard, reply_to_message_id=message.id)

# photo
@app.on_message(filters.photo)
@check_subscription
async def photo(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    saveMsg(message, "PHOTO")
    await app.send_message(message.chat.id,
                     f'Обнаружено расширение: **JPG** 📷\nТеперь отправьте расширение для конвертации...\n\n'
                     f'--**Доступные форматы**-- \n\n`{IMG_TEXT}`\n\n'
                     f'или нажмите /cancel для отмены или используйте /rename для переименования',
                     reply_markup=IMGboard, reply_to_message_id=message.id)

# sticker
@app.on_message(filters.sticker)
@check_subscription
async def sticker(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    saveMsg(message, "STICKER")
    if not message.sticker.is_animated and not message.sticker.is_video:
        await app.send_message(message.chat.id,
                     f'Обнаружено расширение: **WEBP** 📷\nТеперь отправьте расширение для конвертации...\n\n--**Доступные форматы**-- \n\n`{IMG_TEXT}`\n\n**СПЕЦИАЛЬНОЕ** 🎁\nColorize, Positive, Upscale & Scan\n\n{message.from_user.mention} выберите или нажмите /cancel для отмены или используйте /rename для переименования',
                     reply_markup=IMGboard, reply_to_message_id=message.id)
    else:
        await app.send_message(message.chat.id,
                    f'Обнаружено расширение: **TGS** 📷\nТеперь отправьте расширение для конвертации...\n\n--**Доступные форматы**-- \n\n`{IMG_TEXT}`\n\n**СПЕЦИАЛЬНОЕ** 🎁\nColorize, Positive, Upscale & Scan\n\n{message.from_user.mention} выберите или нажмите /cancel для отмены или используйте /rename для переименования',
                    reply_markup=IMGboard, reply_to_message_id=message.id)


# conversion starts here
@app.on_message(filters.text)
@check_subscription
async def text(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    # save restricted
    if "https://t.me/" in message.text:
        mf = threading.Thread(target=lambda: saverec(message), daemon=True)
        mf.start()
        return

    # magnet link
    if message.text[:8] == "magnet:?":
        oldm = await app.send_message(message.chat.id, 'Обработка... ⏳', reply_to_message_id=message.id)
        tf = threading.Thread(target=lambda: gettorfile(message, oldm), daemon=True)
        tf.start()
        return

    # normal
    nmessage, msg_type = getSavedMsg(message)
    if nmessage:
        removeSavedMsg(message)
        await app.delete_messages(message.chat.id, message_ids=nmessage.id + 1)

        if "COLOR" == message.text:
            if not config['features']['colorize']:
                await message.reply_text("Эта функция отключена.")
                return
            oldm = await app.send_message(message.chat.id, 'Обработка... 🎨',
                                    reply_to_message_id=nmessage.id)
            col = threading.Thread(target=lambda: colorizeimage(nmessage, oldm), daemon=True)
            col.start()

        elif "POSITIVE" == message.text:
            if not config['features']['positive']:
                await message.reply_text("Эта функция отключена.")
                return
            oldm = await app.send_message(message.chat.id, 'Обработка... ✨',
                                    reply_to_message_id=nmessage.id)
            pos = threading.Thread(target=lambda: negetivetopostive(nmessage, oldm), daemon=True)
            pos.start()

        elif "READ" == message.text:
            oldm = await app.send_message(message.chat.id, 'Чтение файла... 📖',
                                    reply_to_message_id=nmessage.id)
            rf = threading.Thread(target=lambda: readf(nmessage, oldm), daemon=True)
            rf.start()

        elif "SENDPHOTO" == message.text:
            oldm = await app.send_message(message.chat.id, 'Отправка в формате фото... 🖼️',
                                    reply_to_message_id=nmessage.id)
            sp = threading.Thread(target=lambda: sendphoto(nmessage, oldm), daemon=True)
            sp.start()

        elif "SENDDOC" == message.text:
            oldm = await app.send_message(message.chat.id, 'Отправка в формате документа... 📄',
                                     reply_to_message_id=nmessage.id)
            sd = threading.Thread(target=lambda: senddoc(nmessage, oldm), daemon=True)
            sd.start()

        elif "SENDVID" == message.text:
            oldm = await app.send_message(message.chat.id, 'Отправка в потоковом формате... 🎥',
                                     reply_to_message_id=nmessage.id)
            sv = threading.Thread(target=lambda: sendvideo(nmessage, oldm), daemon=True)
            sv.start()

        elif "SpeechToText" == message.text:
            if not config['features']['speech_to_text']:
                await message.reply_text("Эта функция отключена.")
                return
            oldm = await app.send_message(message.chat.id, 'Транскрибация, для длинных файлов требуется больше времени... 🎤',
                                     reply_to_message_id=nmessage.id)
            stt = threading.Thread(target=lambda: transcript(nmessage, oldm), daemon=True)
            stt.start()

        elif "TextToSpeech" == message.text:
            if not config['features']['text_to_speech']:
                await message.reply_text("Эта функция отключена.")
                return
            oldm = await app.send_message(message.chat.id, 'Генерация речи... 🗣️',
                                    reply_to_message_id=nmessage.id)
            tts = threading.Thread(target=lambda: speak(nmessage, oldm), daemon=True)
            tts.start()

        elif "UPSCALE" == message.text:
            if not config['features']['upscale']:
                await message.reply_text("Эта функция отключена.")
                return
            oldm = await app.send_message(message.chat.id, 'Увеличение разрешения вашего изображения... 🖼️',
                                     reply_to_message_id=nmessage.id)
            upscl = threading.Thread(target=lambda: increaseres(nmessage, oldm), daemon=True)
            upscl.start()

        elif "EXTRACT" == message.text:
            oldm = await app.send_message(message.chat.id, 'Извлечение файла... 📂',
                                    reply_to_message_id=nmessage.id)
            ex = threading.Thread(target=lambda: extract(nmessage, oldm), daemon=True)
            ex.start()

        elif "COMPILE" == message.text:
            oldm = await app.send_message(message.chat.id, 'Компиляция... ⚙️',
                                    reply_to_message_id=nmessage.id)
            cmp = threading.Thread(target=lambda: compile(nmessage, oldm), daemon=True)
            cmp.start()

        elif "SCAN" == message.text:
            if not config['features']['scan']:
                await message.reply_text("Эта функция отключена.")
                return
            oldm = await app.send_message(message.chat.id, 'Сканирование... 🔬',
                                    reply_to_message_id=nmessage.id)
            scn = threading.Thread(target=lambda: scan(nmessage, oldm), daemon=True)
            scn.start()

        elif "RUN" == message.text:
            oldm = await app.send_message(message.chat.id, 'Запуск... ▶️',
                                    reply_to_message_id=nmessage.id)
            rpro = threading.Thread(target=lambda: runpro(nmessage, oldm), daemon=True)
            rpro.start()

        elif "BG REMOVE" == message.text:
            if not config['features']['bg_remove']:
                await message.reply_text("Эта функция отключена.")
                return
            oldm = await app.send_message(message.chat.id, 'Удаление фона... 🏞️',
                                    reply_to_message_id=nmessage.id)
            bgrm = threading.Thread(target=lambda: bgremove(nmessage, oldm), daemon=True)
            bgrm.start()

        elif msg_type == "DOCUMENT":
            inputt = nmessage.document.file_name
            print("File is a Document")

        elif msg_type == "AUDIO" or msg_type == "VOICE":
            try:
                inputt = nmessage.audio.file_name
                print("File is a Audio")
            except:
                inputt = "voice.ogg"
                print("File is a Voice")

        elif msg_type == "VOICE":
            inputt = "voice.ogg"
            print("File is a Voice")

        elif msg_type == "STICKER":
            if (not nmessage.sticker.is_animated) and (not nmessage.sticker.is_video):
                inputt = nmessage.sticker.set_name + ".webp"
            else:
                inputt = nmessage.sticker.set_name + ".tgs"
            print("File is a Sticker")

        elif msg_type == "VIDEO":
            try:
                inputt = nmessage.video.file_name
                print("File is a Video")
            except:
                inputt = "video_note.mp4"
                print("File is a Video Note")

        elif msg_type == "VIDEO_NOTE":
            inputt = "voice_note.mp4"
            print("File is a Video Note")

        elif msg_type == "PHOTO":
            temp = await app.download_media(nmessage)
            inputt = temp.split("/")[-1]
            os.remove(temp)
            print("File is a Photo")

        else:
            if str(message.from_user.id) == str(message.chat.id):
                await app.send_message(message.chat.id, 'Формат не поддерживается, свяжитесь с разработчиком',
                                 reply_to_message_id=nmessage.id)
            return

        newext = message.text.lower()
        oldext = inputt.split(".")[-1]

        if oldext.upper() == newext.upper():
            await app.send_message(message.chat.id, "Хорошая попытка, не выбирайте то же самое расширение 😉",
                             reply_to_message_id=nmessage.id)

        else:
            msg = await app.send_message(message.chat.id, f'Конвертация из **{oldext.upper()}** в **{newext.upper()}**',
                                   reply_to_message_id=nmessage.id)
            conv = threading.Thread(target=lambda: follow(nmessage, inputt, newext, oldext, msg), daemon=True)
            conv.start()

    else:
        if str(message.from_user.id) == str(message.chat.id):
            if len(message.text.split("\n")) == 1:
                ots = threading.Thread(target=lambda: other(message), daemon=True)
                ots.start()
            else:
                saveMsg(message, "TEXT")
                await app.send_message(message.chat.id,
                                 'для текстовых сообщений вы можете использовать `/make` чтобы создать файл из него.\n(первая строка текста будет использована как имя файла)',
                                 reply_to_message_id=message.id)

#apprun
print("Bot Started")
app.run()
