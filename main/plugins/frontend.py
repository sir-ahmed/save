#Developer : Gagan 


import time, os

import logging
import json
from .. import bot as gagan
from .. import userbot, Bot
from .. import FORCESUB as fs
from main.plugins.pyroplug import get_msg
from main.plugins.helpers import get_link, join, screenshot

from telethon import events
from pyrogram.errors import FloodWait

#from ethon.telefunc import force_sub
from main.plugins.helpers import force_sub

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.INFO)
logging.getLogger("telethon").setLevel(logging.INFO)

ft = f"↢ لاستخدام البوت اشتـرك هنا : @{fs}."

message = "↢ ارسل لي المحتوي الذي تريد حفظة \n\n مـثال : `https://t.me/ID_CW/16`"
          
process=[]
timer=[]
user=[]


@gagan.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def clone(event):
    logging.info(event)
    file_name = ''
    if event.is_reply:
        reply = await event.get_reply_message()
        if reply.text == message:
            return
    lit=event.text
    li=lit.split("\n")
    if len(li) > 10:
        await event.reply("الحد الأقصى 10 روابط لكل رسالة")
        return
    for li in li:
        #1239
    
        try:
            link = get_link(li)
            if not link:
                return
    
        except TypeError:
            return
        s, r = await force_sub(event.client, fs, event.sender_id, ft)
        if s == True:
            await event.reply(r)
            return
        edit = await event.reply("جاري المعالجة..")
        if f'{int(event.sender_id)}' in user:
            return await edit.edit("**من فضلك لا ترسل روابط غير مرغوب فيها، انتظر حتى تتم العملية الجارية**")
        user.append(f'{int(event.sender_id)}')
        if "|" in li:
            url = li
            url_parts = url.split("|")
            if len(url_parts) == 2:
            
                file_name = url_parts[1]
        if file_name is not None:
            file_name = file_name.strip()                
        try:
            if 't.me/' not in link:
                await edit.edit("رابط غير صحيح حـاول مجددا")
                ind = user.index(f'{int(event.sender_id)}')
                user.pop(int(ind))
                return
            if 't.me/+' in link:
                q = await join(userbot, link)
                await edit.edit(q)
                ind = user.index(f'{int(event.sender_id)}')
                user.pop(int(ind))
                return
            if 't.me/' in link:
                msg_id = 0
                try:
                    msg_id = int(link.split("/")[-1])
                except ValueError:
                    if '?single' in link:
                        link_ = link.split("?single")[0]
                        msg_id = int(link_.split("/")[-1])
                    else:
                        msg_id = -1
                m = msg_id
                await get_msg(userbot, Bot, event.sender_id, edit.id, link, m, file_name)
        except FloodWait as fw:
            await gagan.send_message(event.sender_id, f'حاول مرة أخرى بعد ذلك {fw.value} ثانيه..')
            await edit.delete()
        except Exception as e:
            logging.info(e)
            await gagan.send_message(event.sender_id, f"حدث خطأ أثناء استنساخ `{link}`\n\n**الخطا:** {str(e)}")
            await edit.delete()
        ind = user.index(f'{int(event.sender_id)}')
        user.pop(int(ind))
        time.sleep(1)
