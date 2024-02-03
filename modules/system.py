# Ultroid - UserBot
# Copyright (C) 2021-2023 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk System**

๏ **Perintah:** `usage`
◉ **Keterangan:** Dapatkan stats penggunaan.

๏ **Perintah:** `usage heroku`
◉ **Keterangan:** Dapatkan stats penggunaan heroku.

๏ **Perintah:** `usage db`
◉ **Keterangan:** Dapatkan stats penggunaan database.

๏ **Perintah:** `ls`
◉ **Keterangan:** Dapatkan semua File di dalam Direktori.

๏ **Perintah:** `restart`
◉ **Keterangan:** Restart Userbot.

๏ **Perintah:** `shutdown`
◉ **Keterangan:** Matikan Userbot.

๏ **Perintah:** `logs`
◉ **Keterangan:** Dapatkan Logs Userbot.
"""
import glob
import io
import os

from telethon.errors.rpcerrorlist import MessageTooLongError

try:
    import cv2
except ImportError:
    cv2 = None


import math
import shutil
from random import choice

from Ayra.fns import some_random_headers

from . import *
from . import humanbytes as hb

HEROKU_API = None
HEROKU_APP_NAME = None

if HOSTED_ON == "heroku":
    heroku_api, app_name = Var.HEROKU_API, Var.HEROKU_APP_NAME
    try:
        if heroku_api and app_name:
            import heroku3

            Heroku = heroku3.from_key(heroku_api)
            app = Heroku.app(app_name)
            HEROKU_API = heroku_api
            HEROKU_APP_NAME = app_name
    except BaseException as er:
        LOGS.exception(er)

FilesEMOJI = {
    "py": "🐍",
    "json": "🔮",
    ("sh", "bat"): "⌨️",
    (".mkv", ".mp4", ".avi", ".gif", "webm"): "🎥",
    (".mp3", ".ogg", ".m4a", ".opus"): "🔊",
    (".jpg", ".jpeg", ".png", ".webp", ".ico"): "🖼",
    (".txt", ".text", ".log"): "📄",
    (".apk", ".xapk"): "📲",
    (".pdf", ".epub"): "📗",
    (".zip", ".rar"): "🗜",
    (".exe", ".iso"): "⚙",
}


@ayra_cmd(pattern="[uU][s][a][g][e]")
async def usage_finder(event):
    x = await event.eor(get_string("com_1"))
    try:
        opt = event.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await x.edit(simple_usage())

    if opt == "db":
        await x.edit(db_usage())
    elif opt == "heroku":
        is_hk, hk = await heroku_usage()
        await x.edit(hk)
    else:
        await x.edit(await get_full_usage())


def simple_usage():
    try:
        import psutil
    except ImportError:
        return "Install 'psutil' to use this..."
    total, used, free = shutil.disk_usage(".")
    cpuUsage = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    upload = humanbytes(psutil.net_io_counters().bytes_sent)
    down = humanbytes(psutil.net_io_counters().bytes_recv)
    TOTAL = humanbytes(total)
    USED = humanbytes(used)
    FREE = humanbytes(free)
    return get_string("usage_simple").format(
        TOTAL,
        USED,
        FREE,
        upload,
        down,
        cpuUsage,
        memory,
        disk,
    )


async def heroku_usage():
    try:
        import psutil
    except ImportError:
        return (
            False,
            "'psutil' not installed!\nPlease Install it to use this.\n`pip3 install psutil`",
        )
    if not (HEROKU_API and HEROKU_APP_NAME):
        if HOSTED_ON == "heroku":
            return False, "Please fill `HEROKU_API` and `HEROKU_APP_NAME`"
        return (
            False,
            f"`This command is only for Heroku Users, You are using {HOSTED_ON}`",
        )
    user_id = Heroku.account().id
    headers = {
        "User-Agent": choice(some_random_headers),
        "Authorization": f"Bearer {heroku_api}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    her_url = f"https://api.heroku.com/accounts/{user_id}/actions/get-quota"
    try:
        result = await async_searcher(her_url, headers=headers, re_json=True)
    except Exception as er:
        return False, str(er)
    quota = result["account_quota"]
    quota_used = result["quota_used"]
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)
    total, used, free = shutil.disk_usage(".")
    _ = shutil.disk_usage("/")
    disk = _.used / _.total * 100
    cpuUsage = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    upload = humanbytes(psutil.net_io_counters().bytes_sent)
    down = humanbytes(psutil.net_io_counters().bytes_recv)
    TOTAL = humanbytes(total)
    USED = humanbytes(used)
    FREE = humanbytes(free)
    return True, get_string("usage").format(
        Var.HEROKU_APP_NAME,
        AppHours,
        AppMinutes,
        AppPercentage,
        hours,
        minutes,
        percentage,
        TOTAL,
        USED,
        FREE,
        upload,
        down,
        cpuUsage,
        memory,
        disk,
    )


def db_usage():
    if udB.name == "Mongo":
        total = 512
    elif udB.name == "Redis":
        total = 30
    elif udB.name == "SQL":
        total = 20
    total = total * (2**20)
    used = udB.usage
    a = f"{humanbytes(used)}/{humanbytes(total)}"
    b = f"{str(round((used / total) * 100, 2))}%"
    return f"**{udB.name}**\n\n**Storage Used**: `{a}`\n**Usage percentage**: **{b}**"


async def get_full_usage():
    is_hk, hk = await heroku_usage()
    her = hk if is_hk else ""
    rd = db_usage()
    return her + "\n\n" + rd


@ayra_cmd(
    pattern="[lL][sS]( (.*)|$)",
)
async def _(e):
    files = e.pattern_match.group(1).strip()
    if not files:
        files = "*"
    elif files.endswith("/"):
        files += "*"
    elif "*" not in files:
        files += "/*"
    files = glob.glob(files)
    if not files:
        return await e.eor("`Direktori Kosong atau Salah.`", time=5)
    allfiles = []
    folders = []
    for file in sorted(files):
        if os.path.isdir(file):
            folders.append(f"📂 {file}")
        else:
            for ext in FilesEMOJI.keys():
                if file.endswith(ext):
                    allfiles.append(f"{FilesEMOJI[ext]} {file}")
                    break
            else:
                if "." in str(file)[1:]:
                    allfiles.append(f"🏷 {file}")
                else:
                    allfiles.append(f"📒 {file}")
    omk = [*sorted(folders), *sorted(allfiles)]
    text = ""
    fls, fos = 0, 0
    flc, foc = 0, 0
    for i in omk:
        try:
            emoji = i.split()[0]
            name = i.split(maxsplit=1)[1]
            nam = name.split("/")[-1]
            if os.path.isdir(name):
                size = 0
                for path, dirs, files in os.walk(name):
                    for f in files:
                        fp = os.path.join(path, f)
                        size += os.path.getsize(fp)
                if hb(size):
                    text += f"{emoji} `{nam}`  `{hb(size)}" + "`\n"
                    fos += size
                else:
                    text += f"{emoji} `{nam}`" + "\n"
                foc += 1
            else:
                if hb(int(os.path.getsize(name))):
                    text += (
                        f"{emoji} `{nam}`  `{hb(int(os.path.getsize(name)))}" + "`\n"
                    )
                    fls += int(os.path.getsize(name))
                else:
                    text += f"{emoji} `{nam}`" + "\n"
                flc += 1
        except BaseException:
            pass
    tfos, tfls, ttol = hb(fos), hb(fls), hb(fos + fls)
    if not hb(fos):
        tfos = "0 B"
    if not hb(fls):
        tfls = "0 B"
    if not hb(fos + fls):
        ttol = "0 B"
    text += f"\n\n`Folders` :  `{foc}` :   `{tfos}`\n`Files` :       `{flc}` :   `{tfls}`\n`Total` :       `{flc+foc}` :   `{ttol}`"
    try:
        if (flc + foc) > 100:
            text = text.replace("`", "")
        await e.eor(text)
    except MessageTooLongError:
        with io.BytesIO(str.encode(text)) as out_file:
            out_file.name = "output.txt"
            await e.reply(f"`{e.text}`", file=out_file, thumb=AyConfig.thumb)
        await e.delete()
