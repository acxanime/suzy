from operator import add
import os
import logging


# import dotenv
# dotenv.load_dotenv()


from logging.handlers import RotatingFileHandler

#force user to join your backup channel leave 0 if you don't need.
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "0"))
FORCE_SUB_CHANNEL2 = int(os.environ.get("FORCE_SUB_CHANNEL2", "0"))

if FORCE_SUB_CHANNEL > FORCE_SUB_CHANNEL2:
    temp = FORCE_SUB_CHANNEL2 
    FORCE_SUB_CHANNEL2 = FORCE_SUB_CHANNEL
    FORCE_SUB_CHANNEL = temp

#bot stats
BOT_STATS_TEXT = os.environ.get("BOTS_STATS_TEXT","<b>BOT UPTIME 🌺</b>\n{uptime}")
#send custom message when user interact with bot
USER_REPLY_TEXT = os.environ.get("USER_REPLY_TEXT", "<b>ʙᴀᴋᴋᴀ ! ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ꜱᴇɴᴘᴀɪ</b>")

#your bot token here from https://telegram.me/BotFather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "") 
#your api id from https://my.telegram.org/apps
APP_ID = int(os.environ.get("APP_ID", "28918271"))
#your api hash from https://my.telegram.org/apps
API_HASH = os.environ.get("API_HASH", "29bf447b916a795191046a91317869fb")
#your channel_id from https://t.me/MissRose_bot by forwarding dummy message to rose and applying command `/id` in reply to that message
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002468801481"))
#your id of telegram can be found by https://t.me/MissRose_bot with '/id' command
OWNER_ID = int(os.environ.get("OWNER_ID", "7475464684"))
#port set to default 8080
PORT = os.environ.get("PORT", "8080")
#your database url mongodb only You can use mongo atlas free cloud database
DB_URL = os.environ.get("DB_URL", "mongodb+srv://stoons:stoons@ajay.v5uug.mongodb.net/?retryWrites=true&w=majority")
#your database name
DB_NAME = os.environ.get("DB_NAME", "Ajay")

START_PIC = os.environ.get("START_PIC", "https://graph.org/file/9eff9023429a2bf643574-add775ea5ee45e9d24.jpg")
FORCE_PIC = os.environ.get("FORCE_PIC", "https://graph.org/file/eb7c8ae9786956240d9f6-48d8610b8c5263ba0e.jpg")

#for creating telegram thread for bot to improve performance of the bot
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "60"))
#your start default command message.
START_MSG = os.environ.get("START_MESSAGE", "<b>Hello 💕 {mention} \n\n ɪ ᴀᴍ ғɪʟᴇ sᴛᴏʀᴇ ʙᴏᴛ, ɪ ᴄᴀɴ sᴛᴏʀᴇ ᴘʀɪᴠᴀᴛᴇ ғɪʟᴇs ɪɴ sᴘᴇᴄɪғɪᴇᴅ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴏᴛʜᴇʀ ᴜsᴇʀs ᴄᴀɴ ᴀᴄᴄᴇss ɪᴛ ғʀᴏᴍ sᴘᴇᴄɪᴀʟ ʟɪɴᴋ.\n\nᴄʜᴇᴄᴋ ᴏᴜᴛ ᴏᴜʀ ᴄʜᴀɴɴᴇʟꜱ ʙᴇʟᴏᴡ ꜰᴏʀ ᴍᴏʀᴇ!👇</b>")
#your telegram tag without @
OWNER_TAG = os.environ.get("OWNER_TAG", "Sitaratoons_Support_bot")
#Time in seconds for message delete, put 0 to never delete
TIME = int(os.environ.get("TIME", "60"))


#Shortner (token system) 
"""
some token verification sites
https://adrinolinks.in/
"""

# Turn this feature on or off using True or False put value inside  ""
# TRUE for yes FALSE if no 
USE_SHORTLINK = True if os.environ.get('USE_SHORTLINK', "True") == "True" else False 
# only shareus service known rightnow rest you can test on your own
SHORTLINK_API_URL = os.environ.get("SHORTLINK_API_URL", "adrinolinks.in")
# SHORTLINK_API_KEY = os.environ.get("SHORTLINK_API_KEY", "")
#use this key if not working ☠️ (jokin!!)
SHORTLINK_API_KEY = os.environ.get("SHORTLINK_API_KEY", "f84049b079c1eed14e5c254a53f0e2a2e2a40668")
#add your custom time in secs for shortlink expiration.
# 24hr = 86400
# 12hr = 43200
VERIFY_EXPIRE = int(os.environ.get('VERIFY_EXPIRE', "86400")) # Add time in seconds
#put TRUE if you want shortner in every link generated by the bot.
U_S_E_P = True if (True if os.environ.get('U_S_E_P', "True") == "True" else False) and (USE_SHORTLINK) else False
#Tutorial video for the user of your shortner on how to download.
TUT_VID = os.environ.get("TUT_VID","https://t.me/How_to_Download_7x/32")





#Payment to remove the token system
#put TRUE if you want this feature
USE_PAYMENT = True if (True if os.environ.get("USE_PAYMENT", "True") == "True" else False) and (USE_SHORTLINK) else False                                                                                          
#UPI ID
UPI_ID = os.environ.get("UPI_ID", "sitaratoons@axl")
#UPI QR CODE IMAGE
UPI_IMAGE_URL = os.environ.get("UPI_IMAGE_URL", "<b><a href='https://graph.org/file/9cc3ca2a0b8235e26ba3c-26c8f2754f9a4c3178.jpg'>Click here</a></b>")
#SCREENSHOT URL of ADMIN for verification of payments
SCREENSHOT_URL = os.environ.get("SCREENSHOT_URL", f"t.me/{OWNER_TAG}")
#Time and its price
#7 Days
PRICE1 = os.environ.get("PRICE1", "80 rs")
#1 Month
PRICE2 = os.environ.get("PRICE2", "150 rs")
#3 Month
PRICE3 = os.environ.get("PRICE3", "300 rs")
#6 Month
PRICE4 = os.environ.get("PRICE4", "500 rs")
#1 Year
PRICE5 = os.environ.get("PRICE5", "1000 rs")



#force message for joining the channel
FORCE_MSG = os.environ.get("FORCE_MSG", "<b>ʜᴇʟʟᴏ {mention} \nᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ᴀɴᴅ ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ʀᴇʟᴏᴀᴅ button ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ʀᴇǫᴜᴇꜱᴛᴇᴅ ꜰɪʟᴇ<b/> 🥺")
#custom caption 
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)
#protected content so that no files can be sent from the bot to anyone. recommended False
# TRUE for yes FALSE if no
PROTECT_CONTENT = True if os.environ.get("PROTECT_CONTENT", "FALSE") == "TRUE" else False
#used if you dont need buttons on database channel.
# True for yes False if no
DISABLE_CHANNEL_BUTTON = True if os.environ.get("DISABLE_CHANNEL_BUTTON", "TRUE") == "TRUE" else False
#you can add admin inside the bot(bug right now will fix later)

#add admins with space seperated
# 7195990000 289371935 248979023
ADMIN_LIST = os.environ.get("ADMINS", "").split()




#no need to add anything from now on
ADMINS = [int(admin) for admin in ADMIN_LIST if admin.isdigit()]
ADMINS.append(OWNER_ID)


LOG_FILE_NAME = "logs.txt"
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)

logging.getLogger("pyrogram").setLevel(logging.WARNING)
def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
