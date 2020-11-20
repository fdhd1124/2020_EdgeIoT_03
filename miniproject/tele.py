import time
import telepot
import pymysql
import os

my_token = "1279543640:AAEFgpZyfJh5q-1SidXWyXLRWFObNpY4N0w"
bot = telepot.Bot(my_token)

InfoMsg = "아래 확인할 요청 번호를 고르세요!\n"\
          "1. 사용자 정보 확인\n"\
          "2. 사용자 로그정보 확인\n"\
          "3. 종료\n"

status = True


def handle(msg):
    content, chat, id = telepot.glance(msg)
    print(content,chat,id)
    
    
    conn = pymysql.connect(host="192.168.100.41", user="raspberryPi", password="Ab1!", db="memberdb", charset="utf8", port=9876)
    cur = conn.cursor()
    cur2 = conn.cursor()

    if content == "text":
        if msg['text'] == "1":
            bot.sendMessage(id, "모든 회원정보를 확인")
            cur.execute("select * from info")

            for result in cur.fetchall():
                print(result)
                result_msg = f"{result[0]} {result[1]} {result[2]}\n"
                bot.sendMessage(id,result_msg)

        elif msg["text"] == "2":
            bot.sendMessage(id, "로그인 시간을 조회")

            cur2.execute("select * from login_log3")

            for result2 in cur2.fetchall():
                print(result2)
                result_msg2 = f"{result2[1]} {result2[2]}\n"
                bot.sendMessage(id, result_msg2)

        elif msg["text"] == "3":
            bot.sendMessage(id,"Bye~")
            os._exit(1)     # 스크립트 강제 종료

        else:
            bot.sendMessage(id, InfoMsg)
            cur.close()
            cur2.close()
            conn.close()

bot.message_loop(handle)

while status == True:
    time.sleep(10)