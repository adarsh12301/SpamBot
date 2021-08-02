import importlib
import time
import re
from sys import argv
from spambot.events import register
from spambot import (
    DEV_USERS,
    OWNER_ID,
    OWNER_USERNAME,
    SUDO_USERS
)
from spambot import (
    ALLOW_EXCL,
    CERT_PATH,
    TOKEN,
    URL,
    SUPPORT_CHAT,
    dispatcher,
    StartTime,
    telethn,
    pbot,
    updater,
)
import asyncio
import io
import os
from asyncio import sleep
from telethon import utils
from spambot.modules.helper_funcs.chat_status import dev_plus, sudo_plus
from spambot.modules.helper_funcs.extraction import extract_user
from telegram.ext import CallbackContext, CommandHandler, run_async, CallbackQueryHandler, MessageHandler, DispatcherHandlerStop
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
client = tbot


DEFAULTUSER = str(OWNER_USERNAME)

help_img = "https://telegra.ph/file/6e92103071aa47ee7023e.mp4"

dev_caption = """
**░░░▒▒▓ᏂᏋᏝᎮ ᎷᏋᏁᏬ▓▒▒░░░**


**/addsudo:** Use this while replying to anyone will add him as a sudo user!!

**/rmsudo:** Use this while replying to anyone will remove him from sudo user!!

**/leave <chat id>:** Bot will leave that chat!!

**/updates:** Check new updates and updates the bot!!

**/restart:** Restarts the bot!!(Too fast!! **Supersonic**)

[©️](https://telegra.ph/file/6e92103071aa47ee7023e.mp4) @TeamGladiators
"""
spam_caption = """
**░░░▒▒▓ᏂᏋᏝᎮ ᎷᏋᏁᏬ▓▒▒░░░**


**/spam:** Spams text for given counter!!\nSyntax: /spam <counter> <text>

**/dspam:** Delay spam a text for given counter after given time!!
Syntax: /dspam <seconds> <counter> <text>

**/mspam:** Spams media for given counter!!
Syntax: /mspam <counter>
(replying to any media)

**/packspam:** Spams all stickers from sticker pack!!
Syntax: /packspam (replying to any sticker)

**/replyraid:** Activates reply raid on the user!!
Syntax: /replyraid (replying to anyone)

**/dreplyraid:** Deactivates reply raid on the user!!
Syntax: /dreplyraid (replying to anyone)

[©️](https://telegra.ph/file/6e92103071aa47ee7023e.mp4) @TeamGladiators
"""

start_img = "https://telegra.ph/file/1312f063f0395fc933edd.mp4"

help_caption = """
**Hᴇʏ ᴍᴀsᴛᴇʀ,
ʏᴏᴜ ᴄᴀɴ ᴀᴄᴄᴇss ᴛʜᴇ ᴡʜᴏʟᴇ ʜᴇʟᴘ ᴍᴇɴᴜ ʙʏ ᴜsɪɴɢ ᴛʜᴇ ɢɪᴠᴇɴ ʙᴜᴛᴛᴏɴs!**

[©️](https://telegra.ph/file/6e92103071aa47ee7023e.mp4) @TeamGladiators
"""
start_caption = f"""
**Nᴏᴡ ᴍᴇ ᴛᴏ ɪɴᴛʀᴏᴅᴜᴄᴇ ᴍʏsᴇʟғ.
I ᴀᴍ ᴍᴏsᴛ ᴘᴏᴡᴇʀғᴜʟʟ sᴘᴀᴍ-ʙᴏᴛ ᴇᴠᴇʀ ᴍᴀᴅᴇ!
I'ᴍ ʜᴇʀᴇ ᴛᴏ ᴅᴇsᴛʀᴏʏ ʏᴏᴜʀ ᴏᴘᴘᴏɴᴇɴᴛ 🔥[🔥](https://telegra.ph/file/1312f063f0395fc933edd.mp4)🔥
I ᴄᴀɴ sᴘᴀᴍ ᴄᴏɴᴛɪɴᴜᴏsʟʏ ᴡɪᴛʜ ʟᴇss ғʟᴏᴏᴅ-ᴡᴀɪᴛ ᴇʀʀᴏʀ ᴀɴᴅ ᴡɪᴛʜ ᴍᴏʀᴇ ᴀᴄᴄᴜʀᴀᴄʏ!**

_↼★᭄ꦿ᭄ꦿmaster★᭄ꦿ᭄ꦿ⇀_
**『 [{DEFAULTUSER}](tg://user?id={OWNER_ID}) 』**

©️ @TeamGladiators
"""

close_caption = """
**Hᴇʟᴘ ᴍᴇɴᴜ ʜᴀs ʙᴇᴇɴ ᴄʟᴏsᴇᴅ!!**
"""

helpbuttons = [
    [
        InlineKeyboardButton(text="Spam Cmds", callback_data="spamcmds"),
        InlineKeyboardButton(text="Dev Cmds", callback_data="devcmds")
    ],
    [
        InlineKeyboardButton(text="Close", callback_data="close")
    ]
]

help_buttons = [
    [
        InlineKeyboardButton(text="Back", callback_data="back"),
        InlineKeyboardButton(text="Close", callback_data="close")
    ]
]


startbuttons = [
    [
        InlineKeyboardButton(
            text="Repo", url="https://github.com/Gladiators-Projects/SpamBot"),
        InlineKeyboardButton(
            text="Support", url=f"https://t.me/Gladiators_Support"
        ),
    ],
    [
        InlineKeyboardButton(
            text="Github Organisation", url="https://github.com/Gladiators-Projects"),
    ]
]
  
openbuttons = [
    [
        InlineKeyboardButton(text="Open Again", callback_data="open")
    ]
]

# @register(pattern="^/start(?: |$)(.*)")
# async def gladiators(event):
#  if "-" not in str(event.chat_id):
#    try:
#        await event.client.send_file(event.chat_id, start_img, caption=f"Now let me introduce myself.\nI am most powerfull spam-bot ever made\nI'm here to destroy your opponent!!\nI can spam continuosly with less flood-wait error and more accuracy!\n\n_↼★᭄ꦿ᭄ꦿmaster★᭄ꦿ᭄ꦿ⇀_\n**『 [{DEFAULTUSER}](tg://user?id={OWNER_ID}) 』**\n\n©️ @TeamGladiators")
#    except:
#        await event.client.send_message(event.chat_id, f"Now let me introduce myself.\nI am most powerfull spam-bot ever made\nI'm here to destroy your opponent!!\nI can spam continuosly with less flood-wait error and more accuracy!\n\n_↼★᭄ꦿ᭄ꦿmaster★᭄ꦿ᭄ꦿ⇀_\n**『 [{DEFAULTUSER}](tg://user?id={OWNER_ID}) 』**\n\n©️ @TeamGladiators")


# @register(pattern="^/help(?: |$)(.*)")
# async def gladiators(event):
#   if event.sender_id in SUDO_USERS or event.sender_id in DEV_USERS:
#     if "-" in str(event.chat_id):
#         try:
#             await event.reply(help_img, caption=f"**░░░▒▒▓ᏂᏋᏝᎮ ᎷᏋᏁᏬ▓▒▒░░░**\n\n**/addsudo:** use this while replying to anyone will add him as a sudo user!!\n\n**/rmsudo:** use this while replying to anyone will remove him from sudo user!!\n\n**/spam:** Spams text for given counter!!\nSyntax: /spam <counter>;<text>\n\n**/bigspam:** Spams text for given counter!!\nSyntax: /bigspam <counter>;<text>\n\n**/dspam:** Delay spam a text for given counter after given time!!\nSyntax: /dspam <seconds>;<counter>;<text>\n\n**/mspam:** Spams media for given counter!!\nSyntax: /mspam <counter>\n(replying to any media)\n\n**/packspam:** Spams all stickers from sticker pack!!\nSyntax: /packspam\n(replying to any sticker)\n\n**/replyraid:** Activates reply raid on the user!!\nSyntax: /replyraid\n(replying to anyone)\n\n**/dreplyraid:** Deactivates reply raid on the user!!\nSyntax: /dreplyraid\n(replying to anyone)\n\n©️ @TeamGladiators")
#         except:
#             await event.reply(f"**░░░▒▒▓ᏂᏋᏝᎮ ᎷᏋᏁᏬ▓▒▒░░░**\n\n**/addsudo:** use this while replying to anyone will add him as a sudo user!!\n\n**/rmsudo:** use this while replying to anyone will remove him from sudo user!!\n\n**/spam:** Spams text for given counter!!\nSyntax: /spam <counter>;<text>\n\n**/bigspam:** Spams text for given counter!!\nSyntax: /bigspam <counter>;<text>\n\n**/dspam:** Delay spam a text for given counter after given time!!\nSyntax: /dspam <seconds>;<counter>;<text>\n\n**/mspam:** Spams media for given counter!!\nSyntax: /mspam <counter>\n(replying to any media)\n\n**/packspam:** Spams all stickers from sticker pack!!\nSyntax: /packspam\n(replying to any sticker)\n\n**/replyraid:** Activates reply raid on the user!!\nSyntax: /replyraid\n(replying to anyone)\n\n**/dreplyraid:** Deactivates reply raid on the user!!\nSyntax: /dreplyraid\n(replying to anyone)\n\n©️ @TeamGladiators")
#     else:
#         try:
#             await event.client.send_file(event.chat_id, help_img, caption="**░░░▒▒▓ᏂᏋᏝᎮ ᎷᏋᏁᏬ▓▒▒░░░**\n\n**/addsudo:** use this while replying to anyone will add him as a sudo user!!\n\n**/rmsudo:** use this while replying to anyone will remove him from sudo user!!\n\n**/spam:** Spams text for given counter!!\nSyntax: /spam <counter>;<text>\n\n**/bigspam:** Spams text for given counter!!\nSyntax: /bigspam <counter>;<text>\n\n**/dspam:** Delay spam a text for given counter after given time!!\nSyntax: /dspam <seconds>;<counter>;<text>\n\n**/mspam:** Spams media for given counter!!\nSyntax: /mspam <counter>\n(replying to any media)\n\n**/packspam:** Spams all stickers from sticker pack!!\nSyntax: /packspam\n(replying to any sticker)\n\n**/replyraid:** Activates reply raid on the user!!\nSyntax: /replyraid\n(replying to anyone)\n\n**/dreplyraid:** Deactivates reply raid on the user!!\nSyntax: /dreplyraid\n(replying to anyone)\n\n©️ @TeamGladiators")
#         except:
#             await event.client.send_message(event.chat_id, "**░░░▒▒▓ᏂᏋᏝᎮ ᎷᏋᏁᏬ▓▒▒░░░**\n\n**/addsudo:** use this while replying to anyone will add him as a sudo user!!\n\n**/rmsudo:** use this while replying to anyone will remove him from sudo user!!\n\n**/spam:** Spams text for given counter!!\nSyntax: /spam <counter>;<text>\n\n**/bigspam:** Spams text for given counter!!\nSyntax: /bigspam <counter>;<text>\n\n**/dspam:** Delay spam a text for given counter after given time!!\nSyntax: /dspam <seconds>;<counter>;<text>\n\n**/mspam:** Spams media for given counter!!\nSyntax: /mspam <counter>\n(replying to any media)\n\n**/packspam:** Spams all stickers from sticker pack!!\nSyntax: /packspam\n(replying to any sticker)\n\n**/replyraid:** Activates reply raid on the user!!\nSyntax: /replyraid\n(replying to anyone)\n\n**/dreplyraid:** Deactivates reply raid on the user!!\nSyntax: /dreplyraid\n(replying to anyone)\n\n©️ @TeamGladiators")

    
@run_async
def start(update: Update, context: CallbackContext):
    if update.effective_chat.type != "private":
        return
    update.effective_message.reply_text(
        start_caption,
        reply_markup=InlineKeyboardMarkup(startbuttons),
        parse_mode=ParseMode.MARKDOWN,
        timeout=60,
    )




@run_async
@sudo_plus
def help(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        help_caption,
        reply_markup=InlineKeyboardMarkup(helpbuttons),
        parse_mode=ParseMode.MARKDOWN,
        timeout=60,
    )


# @run_async
# def help_menu(update, context):
#     query = update.callback_query
#     if query.data == "spamcmds":
#         query.message.edit_text(
#             text=spam_caption,
#             reply_markup=InlineKeyboardMarkup(help_buttons),
#             parse_mode=ParseMode.MARKDOWN,
#         )
#     if query.data == "devcmds":
#         query.message.edit_text(
#             text=dev_caption,
#             reply_markup=InlineKeyboardMarkup(help_buttons),
#             parse_mode=ParseMode.MARKDOWN,
#         )
#     if query.data == "back":
#         query.message.edit_text(
#             text=help_caption,
#             reply_markup=InlineKeyboardMarkup(helpbuttons),
#             parse_mode=ParseMode.MARKDOWN,
#         )
#     if query.data == "open":
#         query.message.edit_text(
#             text=help_caption,
#             reply_markup=InlineKeyboardMarkup(openbuttons),
#             parse_mode=ParseMode.MARKDOWN,
#         )
    
    
    
@run_async
def help_menu(update, context):
    query = update.callback_query
    spam_cmd = re.match(r"spamcmds\((.+?)\)", query.data)
    dev_cmd = re.match(r"devcmds\((.+?)\)", query.data)
    back_cmd = re.match(r"back\((.+?)\)", query.data)
    open_cmd = re.match(r"open\((.+?)\)", query.data)
    close_cmd = re.match(r"close\((.+?)\)", query.data)
    try:
        if spam_cmd:
            query.message.edit_text(
                text=spam_caption,
                reply_markup=InlineKeyboardMarkup(help_buttons),
                parse_mode=ParseMode.MARKDOWN,
            )
        elif dev_cmd:
            query.message.edit_text(
                text=dev_caption,
                reply_markup=InlineKeyboardMarkup(help_buttons),
                parse_mode=ParseMode.MARKDOWN,
            )
        elif back_cmd:
            query.message.edit_text(
                text=help_caption,
                reply_markup=InlineKeyboardMarkup(helpbuttons),
                parse_mode=ParseMode.MARKDOWN,
            )
        elif close_cmd:
            query.message.edit_text(
                text=close_caption,
                reply_markup=InlineKeyboardMarkup(openbuttons),
                parse_mode=ParseMode.MARKDOWN,
            )
        elif open_cmd:
            query.message.edit_text(
                text=help_caption,
                reply_markup=InlineKeyboardMarkup(helpbuttons),
                parse_mode=ParseMode.MARKDOWN,
            )
    except Exception as xy:
        query.message.edit_text("Oops!! Something went wrong, forward this message to @Gladiators_Support\n\n" + str(xy))

           

start_handler = CommandHandler("start", start)
help_handler = CommandHandler("help", help)
callback_handler = CallbackQueryHandler(help_menu, pattern=r"help_.*")

dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(callback_handler)
