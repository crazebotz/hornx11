from funcs import *
from pyrogram import Client, filters
from pyrogram.errors import MediaCaptionTooLong
import asyncio,os

url_ptrn = r'https?://[^\s]+'

# Configs
TOKEN=os.environ.get("BOT_TOKEN", ' ')
API_ID = int(os.environ.get("API_ID",'1234'))
API_HASH= os.environ.get("API_HASH", ' ')


# Running bot
xbot = Client(
    'Hornx11_bot',
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN
)


@xbot.on_message(filters.incoming & filters.regex(url_ptrn) & filters.private & filters.text)
async def get_post_info(_, m):
    if "pornx11.com" not in m.text:
        return
    dele = await m.reply_text("Getting Post Info...", disable_web_page_preview=True)
    query = extract_first_three_words(m.text)
    URL = s_url+query
    
    try:title, image_url, post_url, dl_links = search_one_post(URL, m.text)
    except BaseException as ex: return await dele.edit_text(f"Error [34]: {ex}")   

    captioN = f'**Name:** `{title}`\n\n**Original Url:** {post_url}\n\n**Download Links:**\n{dl_links}'
    try:
        await m.reply_photo(image_url, caption=captioN)
    except MediaCaptionTooLong:
        await dele.edit_text(f"{captioN}")
        return
    await dele.delete()

@xbot.on_message(filters.command(['start']) & filters.private & filters.incoming)
async def start_bot(_, m):
    dele = await m.reply_text("Alive !!!")
    await asyncio.sleep(2)
    await dele.delete()


@xbot.on_message(filters.command(['px11', 'get']) & filters.private & filters.incoming)
async def get_posts(_, m):
    dele = await m.reply_text("Getting Latest Posts...", disable_web_page_preview=True)

    URL = 'https://www.pornx11.com/'
    data = extract_multi_posts(URL)
    await asyncio.sleep(3)

    all_data = group_names(data)
    await dele.delete()

    for x in all_data:
        await m.reply_text(str(x), disable_web_page_preview=True)


@xbot.on_message(filters.command(['s', 'search']) & filters.private & filters.incoming)
async def search_posts(_, m):
    dele = await m.reply_text("Searching...", disable_web_page_preview=True)
    msg_list = m.text.split(" ")
    indx = 0
    m_list = []
    if len(msg_list)<2:
        await dele.edit_text("Invalid Format")
        return

    for i in msg_list:
        if indx == 0:
            pass
        elif indx < 4:
            m_list.append(i)
        else:
            pass
        indx += 1

    query = "+".join(m_list)

    URL = s_url+query
    data = search_multi_posts(URL)
    await asyncio.sleep(3)

    all_data = group_names(data)
    await dele.delete()
    list_no = 1
    for x in all_data:
        await asyncio.sleep(2)
        if list_no == 3:
            break
        await m.reply_text(str(x), disable_web_page_preview=True)
        list_no += 1


print("RUnning Client...")
xbot.run()
