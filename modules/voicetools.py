# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Voice Tools**

๏ **Perintah:** `tts id` <balas pesan>
◉ **Keterangan:** Buat teks ke Voice Google.

๏ **Perintah:** `stt id` <balas pesan>
◉ **Keterangan:** Convert voice ke teks.
"""

import os
import subprocess
from datetime import datetime

import speech_recognition as sr
from gtts import gTTS

from . import *

reco = sr.Recognizer()


@ayra_cmd(
    pattern=r"^[tT][tT][sS](?: |$)(.*)",
)
async def _(event):
    input_str = event.pattern_match.group(1)
    start = datetime.now()
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str
    elif "|" in input_str:
        lan, text = input_str.split("|")
    else:
        await event.eor(
            "Gunakan format : {HNDLR}tts <kode bahasa> <teks/balas ke pesan>."
        )
        return
    text = text.strip()
    lan = lan.strip()
    if not os.path.isdir("/downloads/"):
        os.makedirs("/downloads/")
    required_file_name = "/downloads/voice.mp3"
    try:
        tts = gTTS(text, lang=lan)
        tts.save(required_file_name)
        command_to_execute = [
            "ffmpeg",
            "-i",
            required_file_name,
            "-map",
            "0:a",
            "-codec:a",
            "libopus",
            "-b:a",
            "100k",
            "-vbr",
            "on",
            f"{required_file_name}.opus",
        ]
        try:
            subprocess.check_output(command_to_execute, stderr=subprocess.STDOUT)
        except (subprocess.CalledProcessError, NameError, FileNotFoundError) as exc:
            await event.eor(str(exc))
        else:
            os.remove(required_file_name)
            required_file_name += ".opus"
        end = datetime.now()
        ms = (end - start).seconds
        await event.reply(
            file=required_file_name,
        )
        os.remove(required_file_name)
        await eod(event, f"Diproses {text[:97]} ({lan}) di {ms} detik!")
    except Exception as e:
        await event.eor(str(e))


@ayra_cmd(pattern=r"^[sS][tT][tT](?: |$)(.*)")
async def speec_(e):
    reply = await e.get_reply_message()
    if not (reply and reply.media):
        return await eod(e, "`Balas ke Audio-File..`")
    # Not Hard Checking File Types
    re = await reply.download_media()
    file = "voice.wav"
    open(file, "w").close()
    await bash(f'ffmpeg -i "{re}" -vn "{file}"')
    with sr.AudioFile(file) as source:
        audio = reco.record(source)
    try:
        text = reco.recognize_google(audio, language="id-ID")
    except Exception as er:
        return await e.eor(str(er))
    out = "**Extracted Text :**\n `" + text + "`"
    await e.eor(out)
    os.remove(file)
    os.remove(re)
