from pyrogram import Client, filters
from STORM.Database.pm import *
from STORM.powers import get_id
from config import PM_PIC
hl = "."
pm_watcher = 5
KEX = PM_PIC

TEXT = """**Hey, I am an advanced & superfast high quality userbot assistant with an upgraded version security system**.\n
╰• **Owner** » {}
➖➖➖➖➖➖➖➖➖➖➖ 
**My owner is offline now, please wait until my owner allows you**.\n 
 **Please don't spam here, because spamming will force me to block you from my owner id**\n
• **Warn Limits** » {}      
╰• **Your Warns** » {}
➖➖➖➖➖➖➖➖➖➖➖
•           
"""

@Client.on_message(filters.command("pmpermit", hl) & filters.me)
async def pmpermit(client, message):
    x = await is_pm_on()
    try:
        tg = message.text.split()[1].lower()
    except:
        return await message.edit(f"{hl}pmpermit [on | off]")
    if not tg in ["on", "off"]:
        return await message.edit(f"{hl}pmpermit [on | off]")
    if tg == "on":
        if x:
            return await message.edit("ᴘᴍᴘᴇʀᴍɪᴛ ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ....")
        await toggle_pm()
        if await limit() == 0:
            await update_warns(3)
        return await message.edit("ᴘᴍᴘᴇʀᴍɪᴛ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴇɴᴀʙʟᴇᴅ....")
    if not x:
        return await message.edit("ᴘᴍᴘᴇʀᴍɪᴛ ɪꜱ ɴᴏᴛ ᴇɴᴀʙʟᴇᴅ....")
    await toggle_pm()
    return await message.edit("ᴘᴍᴘᴇʀᴍɪᴛ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴅɪꜱᴀʙʟᴇᴅ....")

@Client.on_message(filters.command(["approve", "disapprove", "a", "da", "allow", "disallow"], hl) & filters.me)
async def appr_dis(client, message):
    if str(message.chat.id)[0] == "-":
        try:
            id = await get_id(_, message)
        except:
            return await message.edit("ꜰᴏʀ ᴀᴘᴘʀᴏᴠᴇ ᴜꜱᴇʀ ɪɴ ɢʀᴏᴜᴘ ᴜ ᴡᴀɴᴛ ᴛᴏ ɢɪᴠᴇ ᴍᴇ ɪ'ᴅ ᴏʀ ʀᴇᴘʟʏ ᴛʜᴀᴛ ᴜꜱᴇʀ..")
    else:
        id = message.chat.id
    tg = message.text.split()[0][1]
    x = await is_approved(id)
    if tg == "d":
        if not x:
            return await message.edit("ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ɴᴏᴛ ᴀᴘᴘʀᴏᴠᴇᴅ..")
        await disapprove(id)
        return await message.edit("ᴜꜱᴇʀ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴅɪꜱᴀᴘᴘʀᴏᴠᴇᴅ ᴛᴏ ᴘᴍ....")
    if x:
        return await message.edit("ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴍʏ ᴅᴀᴛᴀʙᴀꜱᴇ ᴜꜱᴇʀ ᴀʟʀᴇᴀᴅʏ ᴀᴘᴘʀᴏᴠᴇᴅ....")
    await approve(id) 
    await reset_warns(id)
    return await message.edit("ᴜꜱᴇʀ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴀᴘᴘʀᴏᴠᴇᴅ ᴛᴏ ᴘᴍ....")

@Client.on_message(filters.command("setwarns", hl) & filters.me)
async def setwarn(client, message):
    try:
        count = int(message.text.split()[1])
    except:
        return await message.edit(f"{hl}setwarns [ᴠᴀʟᴜᴇ]")
    # 0 allow చేశాం – first DM కి వెంటనే block
    await update_warns(count)
    await message.edit(f"ᴅᴍ ᴡᴀʀɴꜱ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ꜱᴇᴛ ᴛᴏ {count}..")
    
@Client.on_message(filters.private, group=pm_watcher)
async def wtch(client, message):
    user_ = message.from_user
    if message.from_user.id == client.me.id:
        return
    if not await is_pm_on():
        return
    if user_.is_bot:
        return
    if await is_approved(message.from_user.id):
        return
    await add_warn(message.from_user.id)
    if await limit() <= await get_warns(message.from_user.id):
        await message.reply("This account has DM Security Bot enabled. Anybody who sends me a message will automatically be blocked.")
        await reset_warns(message.from_user.id)
        return await client.block_user(message.from_user.id)
    await message.reply_photo(KEX, caption=TEXT.format((await client.get_me()).first_name, await limit(), await get_warns(message.from_user.id)))
