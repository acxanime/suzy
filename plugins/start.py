import asyncio
import os
import random
import sys
import time
import string
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, CHANNEL_ID, FORCE_MSG, FORCE_SUB_CHANNEL, FORCE_SUB_CHANNEL2, OWNER_TAG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT, OWNER_ID, SHORTLINK_API_URL, SHORTLINK_API_KEY, USE_PAYMENT, USE_SHORTLINK, VERIFY_EXPIRE, TIME, TUT_VID, U_S_E_P, START_PIC, FORCE_PIC
from helper_func import encode, get_readable_time, increasepremtime, subscribed, subscribed2, decode, get_messages, get_shortlink, get_verify_status, update_verify_status, get_exp_time
from database.database import add_admin, add_user, del_admin, del_user, full_adminbase, full_userbase, gen_new_count, get_clicks, inc_count, new_link, present_admin, present_hash, present_user

SECONDS = TIME 
TUT_VID = f"{TUT_VID}"

@Bot.on_message(filters.command('start') & filters.private & subscribed & subscribed2)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    verify_status = await get_verify_status(id)
    if USE_SHORTLINK and (not U_S_E_P):
        for i in range(1):
            if id in ADMINS:
                continue
            if verify_status['is_verified'] and VERIFY_EXPIRE < (time.time() - verify_status['verified_time']):
                await update_verify_status(id, is_verified=False)
            if "verify_" in message.text:
                _, token = message.text.split("_", 1)
                if verify_status['verify_token'] != token:
                    return await message.reply("Your token is invalid or Expired ⌛. Try again by clicking /start")
                await update_verify_status(id, is_verified=True, verified_time=time.time())
                if verify_status["link"] == "":
                    reply_markup = None
                await message.reply(f"Your token successfully verified and valid for: {get_exp_time(VERIFY_EXPIRE)} ⏳", reply_markup=reply_markup, protect_content=False, quote=True)
    if len(message.text) > 7:
        for i in range(1):
            if USE_SHORTLINK and (not U_S_E_P):
                if USE_SHORTLINK: 
                    if id not in ADMINS:
                        try:
                            if not verify_status['is_verified']:
                                continue
                        except:
                            continue
            try:
                base64_string = message.text.split(" ", 1)[1]
            except:
                return
            _string = await decode(base64_string)
            argument = _string.split("-")
            if (len(argument) == 5 )or (len(argument) == 4):
                if not await present_hash(base64_string):
                    try:
                        await gen_new_count(base64_string)
                    except:
                        pass
                await inc_count(base64_string)
                if len(argument) == 5:
                    try:
                        start = int(int(argument[3]) / abs(client.db_channel.id))
                        end = int(int(argument[4]) / abs(client.db_channel.id))
                    except:
                        return
                    if start <= end:
                        ids = range(start, end+1)
                    else:
                        ids = []
                        i = start
                        while True:
                            ids.append(i)
                            i -= 1
                            if i < end:
                                break
                elif len(argument) == 4:
                    try:
                        ids = [int(int(argument[3]) / abs(client.db_channel.id))]
                    except:
                        return
                temp_msg = await message.reply("<b>Wait a Second</b>")
                try:
                    messages = await get_messages(client, ids)
                except:
                    await message.reply_text("Something went wrong..! 🥲")
                    return
                await temp_msg.delete()
                snt_msgs = []
                for msg in messages:
                    if bool(CUSTOM_CAPTION) & bool(msg.document):
                        caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html,    filename=msg.document.file_name)
                    else:   
                        caption = "" if not msg.caption else msg.caption.html   
                    reply_markup = None 
                    try:    
                        snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML,  reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                        await asyncio.sleep(0.5)    
                        snt_msgs.append(snt_msg)    
                    except FloodWait as e:  
                        await asyncio.sleep(e.x)    
                        snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode= ParseMode.HTML,  reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                        snt_msgs.append(snt_msg)    
                    except: 
                        pass
                if (SECONDS == 0):
                    return
                notification_msg = await message.reply(f"<b>❗️ <u>IMPORTANT</u> ❗️</b>\n\n ⚠️ This Video / File Will Be Deleted In <b><u> {get_exp_time(SECONDS)}</u></b> 🫥 (Due To Copyright Issues).\n\n<b>📌 <i>Please forward this File/Video to your Saved Messages and Start Download there</i></b>")
                await asyncio.sleep(SECONDS)    
                for snt_msg in snt_msgs:    
                    try:    
                        await snt_msg.delete()  
                    except: 
                        pass    
                await notification_msg.edit("<b><i>Your Video / File Is Successfully Deleted ✅</i></b>")  
                return
            if (U_S_E_P):
                if verify_status['is_verified'] and VERIFY_EXPIRE < (time.time() - verify_status['verified_time']):
                    await update_verify_status(id, is_verified=False)

            if (not U_S_E_P) or (id in ADMINS) or (verify_status['is_verified']):
                if len(argument) == 3:
                    try:
                        start = int(int(argument[1]) / abs(client.db_channel.id))
                        end = int(int(argument[2]) / abs(client.db_channel.id))
                    except:
                        return
                    if start <= end:
                        ids = range(start, end+1)
                    else:
                        ids = []
                        i = start
                        while True:
                            ids.append(i)
                            i -= 1
                            if i < end:
                                break
                elif len(argument) == 2:
                    try:
                        ids = [int(int(argument[1]) / abs(client.db_channel.id))]
                    except:
                        return
                temp_msg = await message.reply("<b>Wait a Second</b>")
                try:
                    messages = await get_messages(client, ids)
                except:
                    await message.reply_text("Something went wrong..! 🥲")
                    return
                await temp_msg.delete()
                snt_msgs = []
                for msg in messages:
                    if bool(CUSTOM_CAPTION) & bool(msg.document):
                        caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html, filename=msg.document.file_name)
                    else:   
                        caption = "" if not msg.caption else msg.caption.html   
                    reply_markup = None 
                    try:    
                        snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML,  reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                        await asyncio.sleep(0.5)    
                        snt_msgs.append(snt_msg)    
                    except FloodWait as e:  
                        await asyncio.sleep(e.x)    
                        snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode= ParseMode.HTML,  reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                        snt_msgs.append(snt_msg)    
                    except: 
                        pass    
            try:
                if snt_msgs:
                    if (SECONDS == 0):
                        return
                    notification_msg = await message.reply(f"<b>❗️ <u>IMPORTANT</u> ❗️</b>\n\n ⚠️ This Video / File Will Be Deleted In <b><u>{get_exp_time(SECONDS)}</u></b> 🫥 (Due To Copyright Issues).\n\n<b>📌 <i>Please forward this File/Video to your Saved Messages and Start Download there</i></b>")
                    await asyncio.sleep(SECONDS)    
                    for snt_msg in snt_msgs:    
                        try:    
                            await snt_msg.delete()  
                        except: 
                            pass    
                    await notification_msg.edit("<b><i>Your Video / File Is Successfully Deleted ✅</i></b>")  
                    return
            except:
                    newbase64_string = await encode(f"sav-ory-{_string}")
                    if not await present_hash(newbase64_string):
                        try:
                            await gen_new_count(newbase64_string)
                        except:
                            pass
                    clicks = await get_clicks(newbase64_string)
                    newLink = f"https://t.me/{client.username}?start={newbase64_string}"
                    link = await get_shortlink(SHORTLINK_API_URL, SHORTLINK_API_KEY,f'{newLink}')
                    if USE_PAYMENT:
                        btn = [
                        [InlineKeyboardButton("• ᴏᴘᴇɴ ʟɪɴᴋ", url=link),
                        InlineKeyboardButton('ᴛᴜᴛᴏʀɪᴀʟ •', url=TUT_VID)],
                        [InlineKeyboardButton("• ʙᴜʏ ᴘʀɪᴍɪᴜᴍ •", callback_data="buy_prem")]
                        ]
                    else:
                        btn = [
                        [InlineKeyboardButton("Click Here 👆", url=link)],
                        [InlineKeyboardButton('How to open this link 👆', url=TUT_VID)]
                        ]
                    await message.reply (f"<b>⌯ ʏᴏᴜʀ ʟɪɴᴋ ɪꜱ ʀᴇᴀᴅʏ, ᴋɪɴᴅʟʏ ᴄʟɪᴄᴋ ᴏɴ ᴏᴘᴇɴ ʟɪɴᴋ ʙᴜᴛᴛᴏɴ..</b>", reply_markup=InlineKeyboardMarkup(btn), protect_content=False, quote=True)
                    return
    
    for i in range(1):
        if USE_SHORTLINK and (not U_S_E_P):
            if USE_SHORTLINK : 
                if id not in ADMINS:
                    try:
                        if not verify_status['is_verified']:
                            continue
                    except:
                        continue
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('🍁 K Dʀᴀᴍᴀ', url='https://t.me/+dAatIkcrgHs0OWY1'),
                    InlineKeyboardButton('⚡ Aɴɪᴍᴇ ', url='https://telegram.me/sitaratoons')
                ],
                [
                    InlineKeyboardButton('🤩 Aɴɪᴍᴇ Mᴏᴠɪᴇ', url='https://telegram.me/+Zutr-hfuNeFhNWM9'),
                    InlineKeyboardButton('🌐 Oᴜʀ Bᴀꜱᴇ', url='https://t.me/New_Anime_Hindi_dub_ST')
                ]        
            ]
        )
        await message.reply_photo(
            photo=START_PIC,
            caption=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup#,
            #message_effect_id=5104841245755180586  # 🔥
    
        )
        return
    if USE_SHORTLINK and (not U_S_E_P): 
        if id in ADMINS:
            return
        verify_status = await get_verify_status(id)
        if not verify_status['is_verified']:
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            await update_verify_status(id, verify_token=token, link="")
            link = await get_shortlink(SHORTLINK_API_URL, SHORTLINK_API_KEY,f'https://telegram.dog/{client.username}?start=verify_{token}')
            if USE_PAYMENT:
                btn = [
                [InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ", url=link),
                InlineKeyboardButton('ᴛᴜᴛᴏʀɪᴀʟ', url=TUT_VID)],
                [InlineKeyboardButton("ʙᴜʏ ᴘʀɪᴍɪᴜᴍ", callback_data="buy_prem")]
                ]
            else:
                btn = [
                [InlineKeyboardButton("Click Here 👆", url=link)],
                [InlineKeyboardButton('How to open this link 👆', url=TUT_VID)]
                ]
            await message.reply(f"Your Ads token is expired, refresh your token and try again. \n\nToken Timeout: {get_exp_time(VERIFY_EXPIRE)}\n\nWhat is the token?\n\nThis is an ads token. If you pass 1 ad, you can use the bot for {get_exp_time(VERIFY_EXPIRE)} after passing the ad", reply_markup=InlineKeyboardMarkup(btn), protect_content=False, quote=True)
            return
    return


    
#=====================================================================================#

WAIT_MSG = """<b>Processing ...</b>"""

REPLY_ERROR = """<code>Use this command as a replay to any telegram message without any spaces.</code>"""

#=====================================================================================#

@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    if FORCE_SUB_CHANNEL & FORCE_SUB_CHANNEL2:
        buttons = [
        [
            InlineKeyboardButton(
                "ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ 1",
                url=client.invitelink),
            InlineKeyboardButton(
                "ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ 2",
                url=client.invitelink2),
        ]
    ]
    elif FORCE_SUB_CHANNEL:
        buttons = [
            [
                InlineKeyboardButton(
                    "ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ",
                    url=client.invitelink)
            ]
        ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text='ᴛʀʏ ᴀɢᴀɪɴ',
                    url=f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply_photo(
        photo=FORCE_PIC,
        caption=FORCE_MSG.format(
        first=message.from_user.first_name,
        last=message.from_user.last_name,
        username=None if not message.from_user.username else '@' + message.from_user.username,
        mention=message.from_user.mention,
        id=message.from_user.id
    ),
    reply_markup=InlineKeyboardMarkup(buttons)#,
    #message_effect_id=5104841245755180586  # Add the effect ID here
    
    )

@Bot.on_message(filters.command('ch2l') & filters.private)
async def gen_link_encoded(client: Bot, message: Message):
    try:
        hash = await client.ask(text="Enter the code here... \n /cancel to cancel the operation",chat_id = message.from_user.id, timeout=60)
    except Exception as e:
        print(e)
        await hash.reply(f"😔 some error occurred {e}")
        return
    if hash.text == "/cancel":
        await hash.reply("Cancelled 😉!")
        return
    link = f"https://t.me/{client.username}?start={hash.text}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🎉 Click Here ", url=link)]])
    await hash.reply_text(f"<b>🧑‍💻 Here is your generated link", quote=True, reply_markup=reply_markup)
    return
        

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot 👥")
    return

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time ⌚</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1

        status = f"""<b><u>Broadcast Completed 🟢</u>
                
                Total Users: <code>{total}</code>
                Successful: <code>{successful}</code>
                Blocked Users: <code>{blocked}</code>
                Deleted Accounts: <code>{deleted}</code>
                Unsuccessful: <code>{unsuccessful}</code></b>"""

        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
    return

@Bot.on_message(filters.command('auth') & filters.private)
async def auth_command(client: Bot, message: Message):
    await client.send_message(
        chat_id=OWNER_ID,
        text=f"Message for @{OWNER_TAG}\n<code>{message.from_user.id}</code>\n/add_admin <code>{message.from_user.id}</code> 🤫",
    )

    await message.reply("Please wait for verification from the owner. 🫣")
    return


@Bot.on_message(filters.command('add_admin') & filters.private & filters.user(OWNER_ID))
async def command_add_admin(client: Bot, message: Message):
    while True:
        try:
            admin_id = await client.ask(text="Enter admin id 🔢\n /cancel to cancel : ",chat_id = message.from_user.id, timeout=60)
        except Exception as e:
            print(e)
            return
        if admin_id.text == "/cancel":
            await admin_id.reply("Cancelled 😉!")
            return
        try:
            await Bot.get_users(user_ids=admin_id.text, self=client)
            break
        except:
            await admin_id.reply("❌ Error 😖\n\nThe admin id is incorrect.", quote = True)
            continue
    if not await present_admin(admin_id.text):
        try:
            await add_admin(admin_id.text)
            await message.reply(f"Added admin <code>{admin_id.text}</code> 😼")
            try:
                await client.send_message(
                    chat_id=admin_id.text,
                    text=f"You are verified, ask the owner to add them to db channels. 😁"
                )
            except:
                await message.reply("Failed to send invite. Please ensure that they have started the bot. 🥲")
        except:
            await message.reply("Failed to add admin. 😔\nSome error occurred.")
    else:
        await message.reply("admin already exist. 💀")
    return


@Bot.on_message(filters.command('del_admin') & filters.private  & filters.user(OWNER_ID))
async def delete_admin_command(client: Bot, message: Message):
    while True:
        try:
            admin_id = await client.ask(text="Enter admin id 🔢\n /cancel to cancel : ",chat_id = message.from_user.id, timeout=60)
        except:
            return
        if admin_id.text == "/cancel":
            await admin_id.reply("Cancelled 😉!")
            return
        try:
            await Bot.get_users(user_ids=admin_id.text, self=client)
            break
        except:
            await admin_id.reply("❌ Error\n\nThe admin id is incorrect.", quote = True)
            continue
    if await present_admin(admin_id.text):
        try:
            await del_admin(admin_id.text)
            await message.reply(f"Admin <code>{admin_id.text}</code> removed successfully 😀")
        except Exception as e:
            print(e)
            await message.reply("Failed to remove admin. 😔\nSome error occurred.")
    else:
        await message.reply("admin doesn't exist. 💀")
    return

@Bot.on_message(filters.command('admins')  & filters.private & filters.private)
async def admin_list_command(client: Bot, message: Message):
    admin_list = await full_adminbase()
    await message.reply(f"Full admin list 📃\n<code>{admin_list}</code>")
    return

@Bot.on_message(filters.command('ping')  & filters.private)
async def check_ping_command(client: Bot, message: Message):
    start_t = time.time()
    rm = await message.reply_text("Pinging....", quote=True)
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f"Ping 🔥!\n{time_taken_s:.3f} ms")
    return


@Client.on_message(filters.private & filters.command('restart') & filters.user(ADMINS))
async def restart(client, message):
    msg = await message.reply_text(
        text="<i>Trying To Restarting.....</i>",
        quote=True
    )
    await asyncio.sleep(5)
    await msg.edit("<i>Server Restarted Successfully ✅</i>")
    try:
        os.execl(sys.executable, sys.executable, *sys.argv)
    except Exception as e:
        print(e)


if USE_PAYMENT:
    @Bot.on_message(filters.command('add_prem') & filters.private & filters.user(ADMINS))
    async def add_user_premium_command(client: Bot, message: Message):
        while True:
            try:
                user_id = await client.ask(text="Enter id of user 🔢\n /cancel to cancel : ",chat_id = message.from_user.id, timeout=60)
            except Exception as e:
                print(e)
                return  
            if user_id.text == "/cancel":
                await user_id.edit("Cancelled 😉!")
                return
            try:
                await Bot.get_users(user_ids=user_id.text, self=client)
                break
            except:
                await user_id.edit("❌ Error 😖\n\nThe admin id is incorrect.", quote = True)
                continue
        user_id = int(user_id.text)
        while True:
            try:
                timeforprem = await client.ask(text="Enter the amount of time you want to provide the premium \nChoose correctly. Its not reversible.\n\n⁕ <code>1</code> for 7 days.\n⁕ <code>2</code> for 1 Month\n⁕ <code>3</code> for 3 Month\n⁕ <code>4</code> for 6 Month\n⁕ <code>5</code> for 1 year.🤑", chat_id=message.from_user.id, timeout=60)
            except Exception as e:
                print(e)
                return
            if not int(timeforprem.text) in [1, 2, 3, 4, 5]:
                await message.reply("You have given wrong input. 😖")
                continue
            else:
                break
        timeforprem = int(timeforprem.text)
        if timeforprem==1:
            timestring = "7 days"
        elif timeforprem==2:
            timestring = "1 month"
        elif timeforprem==3:
            timestring = "3 month"
        elif timeforprem==4:
            timestring = "6 month"
        elif timeforprem==5:
            timestring = "1 year"
        try:
            await increasepremtime(user_id, timeforprem)
            await message.reply("Premium added! 🤫")
            await client.send_message(
            chat_id=user_id,
            text=f"Update for you\n\nPremium plan of {timestring} added to your account. 🤫",
        )
        except Exception as e:
            print(e)
            await message.reply("Some error occurred.\nCheck logs.. 😖\nIf you got premium added message then its ok.")
        return

        
