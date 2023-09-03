# -*- coding: utf-8 -*-
from vkbottle.bot import Bot, Message,rules
import config
import asyncio
import urllib.request
import json

bot = Bot(token=config.api)

helpmsg = ""
hellomsg = "[id"

names = {}

def nickToCharname(nicknames,extra = False):
    localNames = []
    for val in nicknames:
        if not extra:
            localNames.append(f"{names.get(str(val).lower())} ({val})")
        else:
            localNames.append(f"{names.get(str(val['name_clean']).lower())} ({val['name_clean']})")
    return localNames




def getOnlineUsers():
    message = ""
    #try:
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

    url = "https://api.mcsrvstat.us/2/95.217.68.85:25797"
    extraUrl = "https://api.mcstatus.io/v2/status/java/95.217.68.85:25797"
    headers={'User-Agent':user_agent,}

    request=urllib.request.Request(url,None,headers) #The assembled request
    response = urllib.request.urlopen(request)
    data = response.read() # The data u need
    parsed = json.loads(data)
    if(parsed.get('players') is not None):
        online = parsed["players"]["online"]
        max = parsed["players"]["max"]
        if(online == 0):
            message = "Сейчас Гнездо пустует."
        else:
            message = f"Сейчас на сервере находится {online}/{max} Вторженцев. Список:\n"+"\n".join(nickToCharname(parsed["players"]["list"]))
       # except:
          #  message = "Не удалось получить число игроков. Что-то сломалось."

        #finally:
        return message
    else:
        request = urllib.request.Request(extraUrl, None, headers)  # The assembled request
        response = urllib.request.urlopen(request)
        data = response.read()  # The data u need
        parsed = json.loads(data)
        online = parsed["players"]["online"]
        max = parsed["players"]["max"]
        if (online == 0):
            message = "Сейчас Гнездо пустует."
        else:
            nickToCharname(parsed["players"]["list"],True)
            message = f"Сейчас на сервере находится {online}/{max} Вторженцев. Список:\n" + "\n".join(nickToCharname(parsed["players"]["list"],True))
        # except:
        #  message = "Не удалось получить число игроков. Что-то сломалось."

        # finally:
        return message



@bot.on.message(text="!онлайн")
async def hi_handler(message: Message):
    await message.answer(getOnlineUsers())

@bot.on.message(text="!проверка")
async def help_handler(message: Message):
    await message.answer("@all БОТ СУЩЕСТВУЕТ")

bot.run_forever()
