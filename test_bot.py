from telethon import TelegramClient, events
from telethon import Button
from config import *
import logging
from db import cur, conn

logging.basicConfig(level=logging.WARNING)

bot = TelegramClient('test_bot', api_id, api_hash).start(bot_token=bot_token)

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
        text = event.raw_text.split('/note')[1]
        if text == '':
            await event.reply('Write name and note!\n\n/note <name_of_note> <note>')
        elif len(text.split(' ')) == 2:
            await event.reply('Write note!\n\n/note <name_of_note> <note>')
        else:
            name = text.split(' ')[1]
            note_text = text.split(name+' ')[1]
            cur.execute(f"""INSERT INTO notes (NAME, TEXT) VALUES('{name}', '{note_text}');""")
            conn.commit()
            await event.reply('Note has been saved')

@bot.on(events.NewMessage)
async def readNote(event):
    if '/read@best_open_bot' in event.raw_text or '/read' in event.raw_text:
        cur.execute("""SELECT NAME FROM notes;""")
        rows = cur.fetchall()
        if len(rows) == 0:
            await event.reply('There no notes')
        else:
            text = event.raw_text.split('/read')[1]
            print(rows)
            if text == '':
                await event.reply('Write name of note!\n\n/read <name_of_note>')
            elif len(text.split(' ')) == 2:
                name = text.split(' ')[1]
                if name in str(rows):
                    cur.execute(f"""SELECT TEXT FROM notes WHERE NAME = '{name}';""")
                    await event.reply(cur.fetchall()[0][0])
                else:
                    await event.reply('There no such note')
            else:
                await event.reply("What are you doing?\n\n/read <name_of_note>")

@bot.on(events.NewMessage)
async def removeNote(event):
    if '/remove@best_open_bot' in event.raw_text or '/remove' in event.raw_text:
        cur.execute("""SELECT NAME FROM notes;""")
        rows = cur.fetchall()
        if len(rows) == 0:
            await event.reply('There no notes')
        else:
            text = event.raw_text.split('/remove')[1]
            if text == '':
                await event.reply('Write name of note!\n\n/remove <name_of_note>')
            elif len(text.split(' ')) == 2:
                name = text.split(' ')[1]
                if name in str(rows):
                    cur.execute(f"""DELETE FROM notes WHERE NAME = '{name}';""")
                    await event.reply('Note has been removed')
                else:
                    await event.reply('There no such note')
            else:
                await event.reply("What are you doing?\n\n/remove <name_of_note>")

@bot.on(events.NewMessage)
async def lookForNotes(event):
    if '/look@best_open_bot' == event.raw_text or '/look' in event.raw_text:
        cur.execute("""SELECT NAME FROM notes;""")
        rows = cur.fetchall()
        look = ""
        for r in rows:
            look += f"{r[0]}\n"
        await event.respond('There are all notes\n\n' + look)

bot.start()
bot.run_until_disconnected()

conn.close()