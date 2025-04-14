import requests
import time
import telebot
from telebot import types
import re,sys
import threading
import random
dub=[]

tok = '6406176756:AAEThDcHfw07T3lCWAMQQms1AvMegY5LILs'

l='qwertyuiopasdfghjklzxcvbnm1234567890'
bot= telebot.TeleBot(tok)
user_data = {}

def check_session_valid(session_text):
    headers = {
        "user-agent": "Mozilla/5.0",
        "cookie": f'sessionid={session_text}',
    }
    try:
        response = requests.get('https://accountscenter.instagram.com/', headers=headers).text
        token_match = re.search('token":"(.*?)"}', response).group(1)
        print(token_match)
        a = re.search('"actorID":"(.*?)"}', response).group(1)
        actor_id_match = a.split('","')[0]

        if token_match and actor_id_match and len(token_match) > 20:
            actor_id = actor_id_match
            csrf_token = token_match

            profile_url = 'https://www.instagram.com/accounts/edit/'
            headers_profile = {
                "User-Agent": "Mozilla/5.0",
                "cookie": f'sessionid={session_text}',
            }
            profile_response = requests.get(profile_url, headers=headers_profile).text
            user = re.search('"username":"(.*?)"}', profile_response).group(1)
            username=user.split('"')[0]

            return username, actor_id, csrf_token
    except Exception as e:
        print(f"خطأ أثناء التحقق: {e}")
    return None, None, None



import json
from telebot import types

admin_id = 5376094649

def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return {"allowed": [], "requests": []}

# حفظ البيانات
def save_users(data):
    with open("users.json", "w") as f:
        json.dump(data, f, indent=2)

# أمر /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    data = load_users()

    if user_id not in data["allowed"]:
        m = types.InlineKeyboardMarkup()
        m.add(types.InlineKeyboardButton("إرسال طلب", callback_data="send_request"))
        bot.send_message(message.chat.id, "لا يمكنك استخدام البوت لأنك غير مشترك. يرجى التواصل مع المطور أو الضغط على الزر لإرسال طلب.", reply_markup=m)
        return

    # القائمة الأصلية بعد القبول
    m = types.InlineKeyboardMarkup()
    m.add(types.InlineKeyboardButton("خاصية 14day", callback_data="se"))
    m.add(types.InlineKeyboardButton("نقل يوزر", callback_data="start_bot"))
    m.add(types.InlineKeyboardButton("المبرمج", url="t.me/For_X9"))
    bot.send_message(message.chat.id, "أهلاً بك عزيزي في بوت نقل يوزرات انستا", reply_markup=m)

# طلب انضمام
@bot.callback_query_handler(func=lambda call: call.data == "send_request")
def request_access(call):
    user_id = str(call.from_user.id)
    data = load_users()

    if user_id in data["requests"]:
        bot.answer_callback_query(call.id, "تم إرسال طلبك مسبقاً.")
        return

    data["requests"].append(user_id)
    save_users(data)

    bot.answer_callback_query(call.id, "تم إرسال طلبك، سيتم مراجعته.")
    bot.send_message(admin_id, f"طلب جديد من المستخدم {call.from_user.first_name}\nID: `{user_id}`", parse_mode="Markdown")

# أمر الإدارة
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != admin_id:
        return

    text = message.text.split()
    if len(text) < 3:
        bot.send_message(message.chat.id, "/admin add <id> لإضافة عضو\n/admin remove <id> لحذف عضو")
        return

    action, user_id = text[1], text[2]
    data = load_users()

    if action == "add":
        if user_id not in data["allowed"]:
            data["allowed"].append(user_id)
            if user_id in data["requests"]:
                data["requests"].remove(user_id)
            save_users(data)
            bot.send_message(message.chat.id, f"تمت إضافة {user_id} إلى القائمة.")
            bot.send_message(int(user_id), "تمت الموافقة على طلبك! يمكنك الآن استخدام البوت.")
        else:
            bot.send_message(message.chat.id, "المستخدم مضاف مسبقاً.")

    elif action == "remove":
        if user_id in data["allowed"]:
            data["allowed"].remove(user_id)
            save_users(data)
            bot.send_message(message.chat.id, f"تم حذف {user_id} من القائمة.")
        else:
            bot.send_message(message.chat.id, "المستخدم غير موجود في القائمة.")
    else:
        bot.send_message(message.chat.id, "استخدم: /admin add <id> أو /admin remove <id>")

@bot.callback_query_handler(func=lambda call:True)
def call1(call):
    if call.data=='se':
        zi = bot.send_message(call.message.chat.id,text='أرسل الان سيشن الحساب الذي عليه خاصيه نقل ليوزر')
        bot.register_next_step_handler(zi,n1)

    elif call.data == 'start_bot':
        bot.send_message(call.message.chat.id, "ارسل الان سيشن اليوزر الذي تريد نقله", parse_mode="Markdown")
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, get_main_session)




def n1(message):
    cookie1 = str(message.text)
    cookie=f'sessionid={cookie1}'
    headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "dpr": "1",
    "priority": "u=0, i",
    "sec-ch-prefers-color-scheme": "light",
    "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
    "sec-ch-ua-full-version-list": "\"Not/A)Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"126.0.6478.127\", \"Google Chrome\";v=\"126.0.6478.127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-ch-ua-platform-version": "\"10.0.0\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "viewport-width": "601",
    'cookie': cookie,
    }
    rr = requests.get('https://accountscenter.instagram.com/', headers=headers).text
    token = re.search('token":"(.*?)"}', rr).group(1)
    if len(token) > 20:
        print('Session Accepted :)' )
        bot.send_message(message.chat.id,'تم العثور عل الحساب جاري فك الخاصيه.....')
        a = re.search('"actorID":"(.*?)"}', rr).group(1)
        id = a.split('","')[0]
        ue = 'https://www.instagram.com/accounts/edit/'
        he = {
                "User-Agent": "Mozilla/5.0",
                'cookie': cookie,
                }
        rt = requests.get(ue, headers=he).text
        b = re.search('"username":"(.*?)"}', rt).group(1)
        user=b.split('"')[0]
        def skip(user):
            u1 = 'https://accountscenter.instagram.com/api/graphql/'
            h1 = {
                "accept": "*/*",
                "accept-language": "en-US,en;q=0.9",
                "content-type": "application/x-www-form-urlencoded",
                "priority": "u=1, i",
                "sec-ch-prefers-color-scheme": "light",
                "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
                "sec-ch-ua-full-version-list": "\"Not/A)Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"126.0.6478.127\", \"Google Chrome\";v=\"126.0.6478.127\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-model": "\"\"",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-ch-ua-platform-version": "\"10.0.0\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "x-asbd-id": "129477",
                "x-fb-friendly-name": "useFXIMUpdateUsernameMutation",
                "x-fb-lsd": "KGgaT9VpiSaqmSmTINYCMd",
                "x-ig-app-id": "936619743392459",
                "cookie":cookie,
                "Referer": f"https://accountscenter.instagram.com/profiles/{id}/username/?entrypoint=fb_account_center",
                "Referrer-Policy": "strict-origin-when-cross-origin"
            }
            d1 = {
                'fb_dtsg': token,
                'variables': '{"client_mutation_id":"da938a48-c263-46b2-9ec3-25e7614148ae","family_device_id":"device_id_fetch_ig_did","identity_ids":["' + id + '"],"target_fx_identifier":"' + id + '","username":"' + user + '","interface":"IG_WEB"}',
                'doc_id': '7485583154900325',
            }
            s1 = requests.post(u1, headers=h1, data=d1).text
            if '"Rate limit exceeded"' in s1:
                bot.send_message(message.chat.id,f'@{user}\nblocked try after 1 hour')
                sys.exit()
            else:
                us=str(''.join(random.choice(l) for i in range(4)))
                user1=f'{user}.{us}'
                d2={
                    'fb_dtsg': token,
                    'variables': '{"client_mutation_id":"da938a48-c263-46b2-9ec3-25e7614148ae","family_device_id":"device_id_fetch_ig_did","identity_ids":["' + id + '"],"target_fx_identifier":"' + id + '","username":"' + user1 + '","interface":"IG_WEB"}',
                    'doc_id': '9814613795237729',
                }
                s2 = requests.post(u1, headers=h1, data=d2).text
                hp = {'X-Pigeon-Session-Id': '50cc6861-7036-43b4-802e-fb4282799c60','X-Pigeon-Rawclienttime': '1700251574.982','X-IG-Connection-Speed': '-1kbps','X-IG-Bandwidth-Speed-KBPS': '-1.000','X-IG-Bandwidth-TotalBytes-B': '0','X-IG-Bandwidth-TotalTime-MS': '0','X-Bloks-Version-Id': '009f03b18280bb343b0862d663f31ac80c5fb30dfae9e273e43c63f13a9f31c0','X-IG-Connection-Type': 'WIFI','X-IG-Capabilities': '3brTvw==','X-IG-App-ID': '567067343352427','User-Agent': 'Instagram 100.0.0.17.129 Android (29/10; 420dpi; 1080x2129; samsung; SM-M205F; m20lte; exynos7904; en_GB; 161478664)','Accept-Language': 'en-GB, en-US','Cookie': 'mid=ZVfGvgABAAGoQqa7AY3mgoYBV1nP; csrftoken=9y3N5kLqzialQA7z96AMiyAKLMBWpqVj','Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8','Accept-Encoding': 'gzip, deflate','Host': 'i.instagram.com','X-FB-HTTP-Engine': 'Liger','Connection': 'keep-alive','Content-Length': '356'}
                dp = {
                    'signed_body': '0d067c2f86cac2c17d655631c9cec2402012fb0a329bcafb3b1f4c0bb56b1f1f.{"_csrftoken":"9y3N5kLqzialQA7z96AMiyAKLMBWpqVj","adid":"0dfaf820-2748-4634-9365-c3d8c8011256","guid":"1f784431-2663-4db9-b624-86bd9ce1d084","device_id":"android-b93ddb37e983481c","query":"'+user+'"}','ig_sig_key_version': '4'}
                rp = requests.post('https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/',headers=hp,data=dp,).text
                if 'User not found' in rp:
                    ee = requests.post(u1, headers=h1, data=d1).text
                    dd = requests.post(u1, headers=h1, data=d1).text
                    bot.send_message(message.chat.id,f'@{user}\n✅The account feature has been skipped. ')
                    sys.exit()
        def main():
            while True:
                 skip(user)
        Threads=[] 
        for t in range(1):
            x = threading.Thread(target=main)
            x.start()
            Threads.append(x)
        for Th in Threads:
            Th.join()
    else:
        bot.send_message(message.chat.id,'السيشن غير شغال!! يرجى تحقق منه والمحاوله مره اخرى .')
        exit()


def get_main_session(message):
    main_session = message.text.strip()
    chat_id = message.chat.id

    main_user, main_id, main_token = check_session_valid(main_session)
    if main_user:
        user_data[chat_id] = {
            "main_user": main_user,
            "main_id": main_id,
            "main_token": main_token,
            "main_session": main_session
        }

        bot.send_message(chat_id, f"✅ تم قبول الجلسة بنجاح\n👤 اسم المستخدم: `{main_user}`", parse_mode="Markdown")
        bot.send_message(chat_id, "ارسل الان سيشن الحساب الذي تريد نقل اليوزر اليه", parse_mode="Markdown")
        bot.register_next_step_handler(message, get_target_session)
    else:
        bot.send_message(chat_id, "Main Session غير صالحة. حاول مرة أخرى.")
        bot.register_next_step_handler_by_chat_id(chat_id, get_main_session)

def get_target_session(message):
    target_session = message.text.strip()
    chat_id = message.chat.id

    if chat_id not in user_data:
        bot.send_message(chat_id, "⚠️ انتهت الجلسة. أرسل /start للبدء من جديد.")
        return

    main_session = user_data[chat_id]['main_session']
    main_user = user_data[chat_id]['main_user']
    main_id = user_data[chat_id]['main_id']
    main_token = user_data[chat_id]['main_token']

    if main_session == target_session:
        bot.send_message(chat_id, "❌ لا يمكن إرسال نفس الجلسة مرتين.\nيرجى البدء من جديد باستخدام /start")
        return

    target_user, target_id, target_token = check_session_valid(target_session)
    if target_user:
        user_data[chat_id].update({
            "target_session": target_session,
            "target_user": target_user,
            "target_id": target_id,
            "target_token": target_token
        })

        bot.send_message(chat_id, f"✅ تم قبول الجلسة بنجاح\n👤 اسم المستخدم: `{target_user}`", parse_mode="Markdown")
        bot.send_message(chat_id, f"🟢 سيتم نقل هذا اليوزر: `{main_user}`\nإلى هذا الحساب: `{target_user}`", parse_mode="Markdown")

        new_username = ''.join(random.choice(letters) for _ in range(10))
        u1 = 'https://accountscenter.instagram.com/api/graphql/'
        h1 = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded",
            "priority": "u=1, i",
            "sec-ch-prefers-color-scheme": "light",
            "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
            "sec-ch-ua-full-version-list": "\"Not/A)Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"126.0.6478.127\", \"Google Chrome\";v=\"126.0.6478.127\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": "\"\"",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-ch-ua-platform-version": "\"10.0.0\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-asbd-id": "129477",
            "x-fb-friendly-name": "useFXIMUpdateUsernameMutation",
            "x-fb-lsd": "KGgaT9VpiSaqmSmTINYCMd",
            "x-ig-app-id": "936619743392459",
            "cookie": f'sessionid={main_session}',
            "Referer": f"https://accountscenter.instagram.com/profiles/{main_id}/username/?entrypoint=fb_account_center",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }
        d1 = {
            'fb_dtsg': main_token,
            'variables': '{"client_mutation_id":"da938a48-c263-46b2-9ec3-25e7614148ae","family_device_id":"device_id_fetch_ig_did","identity_ids":["' + main_id + '"],"target_fx_identifier":"' + main_id + '","username":"' + new_username + '","interface":"IG_WEB"}',
            'doc_id': '7485583154900325',
        }
        s1 = requests.post(u1, headers=h1, data=d1).text
        print(s1)
        if not '"errors"' in s1:
            u2 = 'https://accountscenter.instagram.com/api/graphql/'
            h2 = {
                "accept": "*/*",
                "accept-language": "en-US,en;q=0.9",
                "content-type": "application/x-www-form-urlencoded",
                "priority": "u=1, i",
                "sec-ch-prefers-color-scheme": "light",
                "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
                "sec-ch-ua-full-version-list": "\"Not/A)Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"126.0.6478.127\", \"Google Chrome\";v=\"126.0.6478.127\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-model": "\"\"",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-ch-ua-platform-version": "\"10.0.0\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "x-asbd-id": "129477",
                "x-fb-friendly-name": "useFXIMUpdateUsernameMutation",
                "x-fb-lsd": "KGgaT9VpiSaqmSmTINYCMd",
                "x-ig-app-id": "936619743392459",
                "cookie": f'sessionid={target_session}',
                "Referer": f"https://accountscenter.instagram.com/profiles/{target_id}/username/?entrypoint=fb_account_center",
                "Referrer-Policy": "strict-origin-when-cross-origin"
            }
            d2 = {
                'fb_dtsg': target_token,
                'variables': '{"client_mutation_id":"da938a48-c263-46b2-9ec3-25e7614148ae","family_device_id":"device_id_fetch_ig_did","identity_ids":["' + target_id + '"],"target_fx_identifier":"' + target_id + '","username":"' + main_user + '","interface":"IG_WEB"}',
                'doc_id': '7485583154900325',
            }
            s2 = requests.post(u2, headers=h2, data=d2).text
            print(s2)
            if not '"Rate limit exceeded"' in s2:
                bot.send_message(chat_id, f"جار التحقق من نقل اليوز...")
                uu = 'https://www.instagram.com/accounts/edit/'
                hh = {
                    "User-Agent": "Mozilla/5.0",
                    "cookie": f'sessionid={target_session}',
                }
                rr = requests.get(uu, headers=hh).text
                uuser = re.search('"username":"(.*?)"}', rr).group(1)
                userf=uuser.split('"')[0]
                if userf==main_user:
                    bot.send_message(chat_id, f"✅ تم نقل اليوزر {main_user} بنجاح")
                else:
                    d1 = {
                        'fb_dtsg': main_token,
                        'variables': '{"client_mutation_id":"da938a48-c263-46b2-9ec3-25e7614148ae","family_device_id":"device_id_fetch_ig_did","identity_ids":["' + main_id + '"],"target_fx_identifier":"' + main_id + '","username":"' + main_user + '","interface":"IG_WEB"}',
                        'doc_id': '7485583154900325',
                    }
                    s1 = requests.post(u1, headers=h1, data=d1).text
                    if not '"Rate limit exceeded"' in s1:
                        uu = 'https://www.instagram.com/accounts/edit/'
                        hh = {
                            "User-Agent": "Mozilla/5.0",
                            "cookie": f'sessionid={main_session}',
                        }
                        rr = requests.get(uu, headers=hh).text
                        uuser = re.search('"username":"(.*?)"}', rr).group(1)
                        userf=uuser.split('"')[0]
                        if userf==main_user:
                            bot.send_message(chat_id, f"تم ارجاع اليوزر بالحساب الاساسي")
            else:
                d1 = {
                        'fb_dtsg': main_token,
                        'variables': '{"client_mutation_id":"da938a48-c263-46b2-9ec3-25e7614148ae","family_device_id":"device_id_fetch_ig_did","identity_ids":["' + main_id + '"],"target_fx_identifier":"' + main_id + '","username":"' + main_user + '","interface":"IG_WEB"}',
                        'doc_id': '7485583154900325',
                    }
                s1 = requests.post(u1, headers=h1, data=d1).text
                if not '"Rate limit exceeded"' in s1:
                    uu = 'https://www.instagram.com/accounts/edit/'
                    hh = {
                        "User-Agent": "Mozilla/5.0",
                        "cookie": f'sessionid={main_session}',
                    }
                    rr = requests.get(uu, headers=hh).text
                    uuser = re.search('"username":"(.*?)"}', rr).group(1)
                    userf=uuser.split('"')[0]
                    if userf==main_user:
                        bot.send_message(chat_id, f"الحساب المنقول عليه محضور\nتم ارجاع اليوزر بالحساب الاصلي ")
        else:
            bot.send_message(chat_id, "❌اليوزر محضور من النقل  حاول بعد ساعه ")
    else:
        bot.send_message(chat_id, "❌ Target Session غير صالحة. حاول مرة أخرى.")
        bot.register_next_step_handler_by_chat_id(chat_id, get_target_session)





while True:
	try:
		bot.infinity_polling()
	except Exception as e:
		print(e)

#حسو ال علي
