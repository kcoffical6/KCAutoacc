from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import filters, Client, errors, enums
from pyrogram.errors import UserNotParticipant
from pyrogram.errors.exceptions.flood_420 import FloodWait
from database import add_user, add_group, all_users, all_groups, users, remove_user
from configs import cfg
import random
import asyncio
from aiohttp import web


class Bot(Client):
    def __init__(self):
        super().__init__(
            "approver",
            api_id=cfg.API_ID,
            api_hash=cfg.API_HASH,
            bot_token=cfg.BOT_TOKEN
        )

    async def start(self):
        await super().start()
        print("Bot is started.")

        if cfg.WEB_SERVER:
            routes = web.RouteTableDef()

            @routes.get("/", allow_head=True)
            async def root_route_handler(request):
                res = {
                    "status": "running",
                }
                return web.json_response(res)

            async def web_server():
                web_app = web.Application(client_max_size=30000000)
                web_app.add_routes(routes)
                return web_app

            app = web.AppRunner(await web_server())
            await app.setup()
            await web.TCPSite(app, "0.0.0.0", cfg.PORT).start()

    async def stop(self, *args):
        await super().stop()
        print("Bot is stopped.")


app = Bot()

gif = [
    'https://telegra.ph/file/d9a923a70fe6061effa86.mp4',
    'https://telegra.ph/file/2f700d6e444d9995205bc.mp4'
]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Main process ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_chat_join_request(filters.group | filters.channel & ~filters.private)
async def approve(_, m: Message):
    op = m.chat
    kk = m.from_user
    try:
        add_group(m.chat.id)
        await app.approve_chat_join_request(op.id, kk.id)
        img = random.choice(gif)
        btn=[[InlineKeyboardButton('movies', url='https://t.me/')]]
        await app.send_video(kk.id, img, "**Hello {}😈💜!\nYour request to join🤩 channel {} has been approved✅.keeps sharing and support us🫠🥹\n\n__Powerd By : #TEAM_KC 😎🔥**".format(m.from_user.mention, m.chat.title), reply_markup=InlineKeyboardMarkup(btn))
        add_user(kk.id)
    except errors.PeerIdInvalid as e:
        print("user isn't start bot(means group)")
    except Exception as err:
        print(str(err))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Start ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@app.on_message(filters.command("start"))
async def op(_, m: Message):
    try:
        await app.get_chat_member(cfg.CHID, m.from_user.id)
        if m.chat.type == enums.ChatType.PRIVATE:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🗯 UPDATE", url="https://t.me/"),
                        InlineKeyboardButton(
                            "💬MOVIES CHANNEL", url="https://t.me/")
                    ], [
                        InlineKeyboardButton(
                            "➕ Add me to your group ➕", url="https://t.me/")
                    ], [
                        InlineKeyboardButton(
                            "➕ Add me to your channel ➕", url="https://t.me/")
                    ]
                ]
            )
            add_user(m.from_user.id)
            await m.reply_photo("https://telegra.ph/file/12a39eecaa3031e3c4409.png", caption="**👋 Hello {}!\nI'M AUTO JOIN REQUEST ACCEPT BOT\n━━━━━━━━━━━━━━━━━━━━━━━━━\n● ɪ ᴄᴀɴ ᴀᴜᴛᴏ ᴀᴘᴘʀᴏᴠᴇ ᴜꜱᴇʀꜱ ᴊᴏɪɴ ʀᴇQᴜᴇꜱᴛ ɪɴ ɢʀᴏᴜᴘꜱ ᴀɴᴅ ᴄʜᴀɴɴᴇʟꜱ.\n● ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴏʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴘᴇʀᴍɪꜱꜱɪᴏɴꜱ.😊\n\n__Powerd By: #TEAM_APZ**".format(m.from_user.mention, "https://t.me/telegram/153"), reply_markup=keyboard)

        elif m.chat.type == enums.ChatType.GROUP or enums.ChatType.SUPERGROUP:
            keyboar = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "💁‍♂️ Start me private 💁‍♂️", url="https://t.me/join_accept_bot?start=start")
                    ]
                ]
            )
            add_group(m.chat.id)
            await m.reply_text("** Hello {}!\nwrite me private for more details**".format(m.from_user.first_name), reply_markup=keyboar)
        print(m.from_user.first_name + " Is started Your Bot!")

    except UserNotParticipant:
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🍀 Check Again 🍀", "chk")
                ]
            ]
        )
        await m.reply_text("**⚠️Access Denied!⚠️\n\nPlease Join @{} to use me.If you joined click check again button to confirm.**".format(cfg.FSUB), reply_markup=key)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ callback ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@app.on_callback_query(filters.regex("chk"))
async def chk(_, cb: CallbackQuery):
    try:
        await app.get_chat_member(cfg.CHID, cb.from_user.id)
        if cb.message.chat.type == enums.ChatType.PRIVATE:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🗯 UPDATE", url="https://t.me/"),
                        InlineKeyboardButton(
                            "💬 MOVIES CHANNEL", url="https://t.me/")
                    ], [
                        InlineKeyboardButton(
                            "➕ Add me to your group ➕", url="https://t.me/")
                    ], [
                        InlineKeyboardButton(
                            "➕ Add me to your channel ➕", url="https://t.me/")
                    ]
                ]
            )
            add_user(cb.from_user.id)
            await cb.message.edit("**👋 Hello {}!\nI'M AUTO JOIN REQUEST ACCEPT BOT\n━━━━━━━━━━━━━━━━━━━━━━━━━\n● ɪ ᴄᴀɴ ᴀᴜᴛᴏ ᴀᴘᴘʀᴏᴠᴇ ᴜꜱᴇʀꜱ ᴊᴏɪɴ ʀᴇQᴜᴇꜱᴛ ɪɴ ɢʀᴏᴜᴘꜱ ᴀɴᴅ ᴄʜᴀɴɴᴇʟꜱ.\n● ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴏʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴘᴇʀᴍɪꜱꜱɪᴏɴꜱ.😊\n\n__Powerd By : #TEAM_APZ**".format(cb.from_user.mention, "https://t.me/telegram/153"), reply_markup=keyboard, disable_web_page_preview=True)
        print(cb.from_user.first_name + " Is started Your Bot!")
    except UserNotParticipant:
        await cb.answer("🙅‍♂️ You are not joined our update channel join and try again. 🙅‍♂️")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ info ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(_, m: Message):
    xx = all_users()
    x = all_groups()
    tot = int(xx + x)
    await m.reply_text(text=f"""
🍀 Chats Stats 🍀
🙋‍♂️ Users : `{xx}`
👥 Groups : `{x}`
🚧 Total users & groups : `{tot}` """)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m: Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            # print(int(userid))
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked += 1
        except Exception as e:
            print(e)
            failed += 1

    await lel.edit(f"✅Successfull to `{success}` users.\n❌ Faild to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast Forward ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@app.on_message(filters.command("fcast") & filters.user(cfg.SUDO))
async def fcast(_, m: Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            # print(int(userid))
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked += 1
        except Exception as e:
            print(e)
            failed += 1

    await lel.edit(f"✅Successfull to `{success}` users.\n❌ Faild to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")

print("I'm Alive Now!")
app.run()
