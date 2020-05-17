import socks
from telethon import TelegramClient, events
from telethon import Button
from telethon.tl.types import ChannelParticipantsAdmins
from config import *
import logging
from db import cur, conn
import time

logging.basicConfig(level=logging.WARNING)

bot = TelegramClient('test_bot', api_id, api_hash, proxy=(socks.HTTP, '154.41.2.154', 13538)).start(bot_token=bot_token)

@bot.on(events.NewMessage)
async def start(event):
    if '/start' == event.raw_text:
        await event.reply("""Hey, I'm OpenBot. Save into me your notes and see its in any time

To write a note write\n/note <name_of_note> <note>

To read a note write\n/read <name_of_note>

To remove a note write\n/remove <name_of_note>

To look all notes write\n/look
""")

@bot.on(events.NewMessage)
async def writeNote(event):
    if '/note@best_open_bot' in event.raw_text or '/note' in event.raw_text:
        text = event.raw_text.strip()
        command = text.split()[0]
        users = await bot.get_participants(event.chat_id)
        admin_users = await bot.get_participants(event.chat_id, filter=ChannelParticipantsAdmins)
        admins = []
        for admin in admin_users:
            admins.append(admin.id)
        if '-' in str(event.chat_id):
            cur.execute(f"SELECT NAME FROM notes WHERE USER_ID = '{users[0].id}' AND CHAT_ID = '{event.chat_id}' AND CHAT_ID IS NOT NULL;")
            if len(cur.fetchall()) == 5 and users[0].id not in admins:
                await event.reply("If you not an admin, you can write only 5 notes in group. Please remove any notes or reconcile")
            elif len(text.split()) == 1:
                await event.reply('Write name and note!\n\n/note <name_of_note> <note>')
            elif len(text.split()) == 2:
                await event.reply('Write note!\n\n/note <name_of_note> <note>')
            else:
                name = text.split()[1]
                cur.execute(f"SELECT NAME FROM NOTES WHERE CHAT_ID = '{event.chat_id}';")
                messages = []
                for mess in cur.fetchall():
                    messages.append(mess[0])
                if name in messages:
                    await event.reply("This name if note is busy. Write another name")
                else:
                    note_text = text.split(command+' '+name+' ')[1]
                    cur.execute(f"INSERT INTO notes (CHAT_ID, USER_ID, NAME, TEXT) VALUES('{event.chat_id}', '{users[0].id}', '{name}', '{note_text}');")
                    conn.commit()
                    await event.reply("Note has been saved")
        elif len(text.split()) == 1:
                await event.reply('Write name and note!\n\n/note <name_of_note> <note>')
        elif len(text.split()) == 2:
            await event.reply('Write note!\n\n/note <name_of_note> <note>')
        elif len(text.split()) > 2:
            name = text.split()[1]
            cur.execute(f"SELECT NAME FROM NOTES WHERE USER_ID = '{event.chat_id}';")
            messages = []
            for mess in cur.fetchall():
                messages.append(mess[0])
            if name in messages:
                await event.reply("This name if note is busy. Write another name")
            else:
                note_text = text.split(command+' '+name+' ')[1]
                cur.execute(f"INSERT INTO notes (USER_ID, NAME, TEXT) VALUES('{users[0].id}', '{name}', '{note_text}');")
                conn.commit()
                await event.reply("Note has been saved")
        else:
            await event.reply('What are you doing!?\n\n/note <name_of_note> <note>')

@bot.on(events.NewMessage)
async def readNote(event):
    if '/read@best_open_bot' in event.raw_text or '/read' in event.raw_text:
        users = await bot.get_participants(event.chat_id)
        if len(event.raw_text.split()) != 2:
            await event.reply("Write name of note!\n\n/read <name_of_note>")
        elif len(event.raw_text.split()) == 2:
            name = event.raw_text.split()[1]
            if '-' in str(event.chat_id):
                try:
                    cur.execute(f"SELECT TEXT FROM notes WHERE CHAT_ID = '{event.chat_id}' AND CHAT_ID IS NOT NULL AND NAME = '{name}';")
                    await event.reply(cur.fetchone()[0])
                except:
                    await event.reply('There are no such notes')
            else:
                try:
                    cur.execute(f"SELECT TEXT FROM notes WHERE USER_ID = '{users[0].id}' AND CHAT_ID IS NULL AND NAME = '{name}';")
                    await event.reply(cur.fetchone()[0])
                except:
                    await event.reply('There are no such notes')
        else:
            await event.reply('There are no notes')

@bot.on(events.NewMessage)
async def removeNote(event):
    if '/remove@best_open_bot' in event.raw_text or '/remove' in event.raw_text:
        cur.execute("""SELECT NAME FROM notes;""")
        rows = cur.fetchall()
        if len(rows) == 0:
            await event.reply('There no notes')
        else:
            text = event.raw_text.split('/remove')[1]
            if len(text.split(' ')) == 2:
                name = text.split(' ')[1]
                if name in str(rows):
                    cur.execute(f"""DELETE FROM notes WHERE NAME = '{name}';""")
                    await event.reply('Note has been removed')
                else:
                    await event.reply('There no such note')
            else:
                await event.reply("Write name of note!\n\n/remove <name_of_note>")

@bot.on(events.NewMessage)
async def lookForNotes(event):
    if '/look@best_open_bot' == event.raw_text or '/look' in event.raw_text:
        if '-' in str(event.chat_id):
            cur.execute(f"SELECT NAME FROM notes WHERE CHAT_ID = '{event.chat_id}';")
            look = ""
            for r in cur.fetchall():
                look += f"{r[0]}\n"
            await event.respond('There are all notes of this group\n\n' + look)
        else:
            users = await bot.get_participants(event.chat_id)
            cur.execute(f"SELECT NAME FROM notes WHERE USER_ID = '{users[0].id}' AND CHAT_ID IS NULL;")
            look = ""
            for r in cur.fetchall():
                look += f"{r[0]}\n"
            await event.respond('There are all your notes\n\n' + look)

@bot.on(events.NewMessage)
async def botTrigger(event):
    if 'openbot' in event.raw_text.lower() or 'open' == event.raw_text.lower():
        await bot.send_file(event.chat_id, '/home/austin/Desktop/Petuhon/telethon/openBot/audio/blood_and_concrete.mp3', voice_note=True)
    elif 'опенбот' in event.raw_text.lower() or 'опен бот' in event.raw_text.lower() or 'опен' in event.raw_text.lower() or 'пизда' in event.raw_text.lower():
        await bot.send_file(event.chat_id, '/home/austin/Desktop/Petuhon/telethon/openBot/audio/кровь_и_бетон.mp3', voice_note=True)
    elif 'god ' in event.raw_text.lower() or ' god ' in event.raw_text.lower() or 'god' == event.raw_text.lower():
        await bot.send_file(event.chat_id, '/home/austin/Desktop/Petuhon/telethon/openBot/audio/pupl_fiction.mp3', voice_note=True)

#This is test hadler for testing new features
@bot.on(events.NewMessage)
async def test(event):
    if '/test' == event.raw_text or '/test@best_open_bot' == event.raw_text:
        await bot.send_file(event.chat_id, '/home/austin/Desktop/Petuhon/telethon/openBot/audio/blood_and_concrete.mp3', voice_note=True)

@bot.on(events.NewMessage)
async def lookMyGovnoCode(event):
    if '/code@best_open_bot' == event.raw_text or '/code' in event.raw_text:
        await event.reply('https://github.com/Austin-Bluethy/open-bot')

bot.start()
bot.run_until_disconnected()

conn.close()