# Ultroid - UserBot
# Copyright (C) 2021-2023 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Image**

๏ **Perintah:** `border`
◉ **Keterangan:** Untuk membuat batas di sekitar media itu .

๏ **Perintah:** `grey`
◉ **Keterangan:** Untuk membuatnya hitam dan putih.

๏ **Perintah:** `color`
◉ **Keterangan:** Untuk membuatnya Berwarna-warni.

๏ **Perintah:** `toon`
◉ **Keterangan:** Untuk membuatnya toon.

๏ **Perintah:** `danger`
◉ **Keterangan:** Agar terlihat Bahaya.

๏ **Perintah:** `negative`
◉ **Keterangan:** Untuk membuat citra negatif.

๏ **Perintah:** `blur`
◉ **Keterangan:** Untuk membuatnya buram.

๏ **Perintah:** `quad`
◉ **Keterangan:**membuat Vortex.

๏ **Perintah:** `mirror`
◉ **Keterangan:** Untuk membuat gambar cermin.

๏ **Perintah:** `flip`
◉ **Keterangan:** Untuk membuatnya terbalik.

๏ **Perintah:** `sketch`
◉ **Keterangan:** Untuk menggambar sketsanya.

๏ **Perintah:** `pixelator`
◉ **Keterangan:** Buat Gambar Piksel..

๏ **Perintah:** `rmbg`
◉ **Keterangan:** Remove background from that picture.
"""
import os

from . import LOGS, con

try:
    import cv2
except ImportError:
    LOGS.error(f"{__file__}: OpenCv not Installed.")

import numpy as np

try:
    from PIL import Image
except ImportError:
    Image = None
    LOGS.info(f"{__file__}: PIL  not Installed.")
from telegraph import upload_file as upf
from telethon.errors.rpcerrorlist import (ChatSendMediaForbiddenError,
                                          MessageDeleteForbiddenError)

from . import *


@ayra_cmd(pattern="[Cc]olor$")
async def _(event):
    reply = await event.get_reply_message()
    if not (reply and reply.media):
        return await event.eor("`Balas ke Gambar Hitam Putih`")
    xx = await event.eor("`Mewarnai gambar 🎨🖌️...`")
    image = await reply.download_media()
    img = cv2.VideoCapture(image)
    ret, frame = img.read()
    cv2.imwrite("ayra.jpg", frame)
    if udB.get_key("DEEP_API"):
        key = Redis("DEEP_API")
    else:
        key = "quickstart-QUdJIGlzIGNvbWluZy4uLi4K"
    r = requests.post(
        "https://api.deepai.org/api/colorizer",
        files={"image": open("ayra.jpg", "rb")},
        headers={"api-key": key},
    )
    os.remove("ayra.jpg")
    os.remove(image)
    if "status" in r.json():
        return await event.edit(
            r.json()["status"] + "\nGet api nd set `{i}setdb DEEP_API key`"
        )
    r_json = r.json()["output_url"]
    await event.client.send_file(event.chat_id, r_json, reply_to=reply)
    await xx.delete()


@ayra_cmd(pattern="(grey|blur|negative|danger|mirror|quad|sketch|flip|toon)$")
async def ayra_tools(event):
    match = event.pattern_match.group(1)
    ureply = await event.get_reply_message()
    if not (ureply and (ureply.media)):
        await event.eor(get_string("cvt_3"))
        return
    ayra = await ureply.download_media()
    xx = await event.eor(get_string("com_1"))
    if ayra.endswith(".tgs"):
        xx = await xx.edit(get_string("sts_9"))
    file = await con.convert(ayra, convert_to="png", outname="ayra")
    ayra = cv2.imread(file)
    if match == "grey":
        ayra = cv2.cvtColor(ayra, cv2.COLOR_BGR2GRAY)
    elif match == "blur":
        ayra = cv2.GaussianBlur(ayra, (35, 35), 0)
    elif match == "negative":
        ayra = cv2.bitwise_not(ayra)
    elif match == "danger":
        dan = cv2.cvtColor(ayra, cv2.COLOR_BGR2RGB)
        ayra = cv2.cvtColor(dan, cv2.COLOR_HSV2BGR)
    elif match == "mirror":
        ish = cv2.flip(ayra, 1)
        ayra = cv2.hconcat([ayra, ish])
    elif match == "flip":
        trn = cv2.flip(ayra, 1)
        ish = cv2.rotate(trn, cv2.ROTATE_180)
        ayra = cv2.vconcat([ayra, ish])
    elif match == "quad":
        ayra = cv2.imread(file)
        roid = cv2.flip(ayra, 1)
        mici = cv2.hconcat([ayra, roid])
        fr = cv2.flip(mici, 1)
        trn = cv2.rotate(fr, cv2.ROTATE_180)
        ayra = cv2.vconcat([mici, trn])
    elif match == "sketch":
        gray_image = cv2.cvtColor(ayra, cv2.COLOR_BGR2GRAY)
        inverted_gray_image = 255 - gray_image
        blurred_img = cv2.GaussianBlur(inverted_gray_image, (21, 21), 0)
        inverted_blurred_img = 255 - blurred_img
        ayra = cv2.divide(gray_image, inverted_blurred_img, scale=256.0)
    elif match == "toon":
        height, width, _ = ayra.shape
        samples = np.zeros([height * width, 3], dtype=np.float32)
        count = 0
        for x in range(height):
            for y in range(width):
                samples[count] = ayra[x][y]
                count += 1
        _, labels, centers = cv2.kmeans(
            samples,
            12,
            None,
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001),
            5,
            cv2.KMEANS_PP_CENTERS,
        )
        centers = np.uint8(centers)
        ish = centers[labels.flatten()]
        ayra = ish.reshape(ayra.shape)
    cv2.imwrite("ayra.jpg", ayra)
    await event.client.send_file(
        event.chat_id,
        "ayra.jpg",
        force_document=False,
        reply_to=event.reply_to_msg_id,
    )
    await xx.delete()
    os.remove("ayra.jpg")
    os.remove(file)


@ayra_cmd(pattern="[Cc]sample (.*)")
async def sampl(ayra):
    if color := ayra.pattern_match.group(1).strip():
        img = Image.new("RGB", (200, 100), f"{color}")
        img.save("csample.png")
        try:
            try:
                await ayra.delete()
                await ayra.client.send_message(
                    ayra.chat_id, f"Contoh Warna untuk `{color}` !", file="csample.png"
                )
            except MessageDeleteForbiddenError:
                await ayra.reply(f"Contoh Warna untuk `{color}` !", file="csample.png")
        except ChatSendMediaForbiddenError:
            await ayra.eor("Hmm! Mengirim Media dinonaktifkan di sini!")

    else:
        await ayra.eor("Nama Warna/Kode Hex salah!")


@ayra_cmd(
    pattern="[Bb]lue$",
)
async def ayra(event):
    ureply = await event.get_reply_message()
    xx = await event.eor("`...`")
    if not (ureply and (ureply.media)):
        await xx.edit(get_string("cvt_3"))
        return
    ayra = await ureply.download_media()
    if ayra.endswith(".tgs"):
        await xx.edit(get_string("sts_9"))
    file = await con.convert(ayra, convert_to="png", outname="ayra")
    got = upf(file)
    lnk = f"https://graph.org{got[0]}"
    r = await async_searcher(
        f"https://nekobot.xyz/api/imagegen?type=blurpify&image={lnk}", re_json=True
    )
    ms = r.get("message")
    if not r["success"]:
        return await xx.edit(ms)
    await download_file(ms, "ayra.png")
    img = Image.open("ayra.png").convert("RGB")
    img.save("ayra.webp", "webp")
    await event.client.send_file(
        event.chat_id,
        "ayra.webp",
        force_document=False,
        reply_to=event.reply_to_msg_id,
    )
    await xx.delete()
    os.remove("ayra.png")
    os.remove("ayra.webp")
    os.remove(ayra)


@ayra_cmd(pattern="[bB]order( (.*)|$)")
async def ok(event):
    hm = await event.get_reply_message()
    if not (hm and (hm.photo or hm.sticker)):
        return await event.eor("`Balas ke Stiker atau Foto..`")
    col = event.pattern_match.group(1).strip()
    wh = 20
    if not col:
        col = [255, 255, 255]
    else:
        try:
            if ";" in col:
                col_ = col.split(";", maxsplit=1)
                wh = int(col_[1])
                col = col_[0]
            col = [int(col) for col in col.split(",")[:2]]
        except ValueError:
            return await event.eor("`Bukan Masukan yang Valid...`")
    okla = await hm.download_media()
    img1 = cv2.imread(okla)
    constant = cv2.copyMakeBorder(img1, wh, wh, wh, wh, cv2.BORDER_CONSTANT, value=col)
    cv2.imwrite("output.png", constant)
    await event.client.send_file(event.chat.id, "output.png")
    os.remove("output.png")
    os.remove(okla)
    await event.delete()


@ayra_cmd(pattern="[Pp]ixelator( (.*)|$)")
async def pixelator(event):
    reply_message = await event.get_reply_message()
    if not (reply_message and reply_message.photo):
        return await event.eor("`Membalas foto`")
    hw = 50
    try:
        hw = int(event.pattern_match.group(1).strip())
    except (ValueError, TypeError):
        pass
    msg = await event.eor(get_string("com_1"))
    image = await reply_message.download_media()
    input_ = cv2.imread(image)
    height, width = input_.shape[:2]
    w, h = (hw, hw)
    temp = cv2.resize(input_, (w, h), interpolation=cv2.INTER_LINEAR)
    output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
    cv2.imwrite("output.jpg", output)
    await msg.respond("Pixelated by Ayra", file="output.jpg")
    await msg.delete()
    os.remove("output.jpg")
    os.remove(image)


@ayra_cmd(
    pattern="[Rr]mbg($| (.*))",
)
async def abs_rmbg(event):
    RMBG_API = udB.get_key("RMBG_API")
    if not RMBG_API:
        return await event.eor(
            "Ambil RMBG_API Anda [Disini](https://www.remove.bg/) kemudian ketik setdb RMBG_API <api_key>.",
        )
    match = event.pattern_match.group(1).strip()
    reply = await event.get_reply_message()
    if match and os.path.exists(match):
        dl = match
    elif reply and reply.media:
        if reply.document and reply.document.thumbs:
            dl = await reply.download_media(thumb=-1)
        else:
            dl = await reply.download_media()
    else:
        return await eod(event, "Gunakan format : `rmbg` <balas ke foto>.")
    if not (dl and dl.endswith(("webp", "jpg", "png", "jpeg"))):
        os.remove(dl)
        return await event.eor(get_string("com_4"))
    if dl.endswith("webp"):
        file = f"{dl}.png"
        Image.open(dl).save(file)
        os.remove(dl)
        dl = file
    xx = await event.eor("`Sending to remove.bg`")
    dn, out = await ReTrieveFile(dl)
    os.remove(dl)
    if not dn:
        dr = out["errors"][0]
        de = dr.get("detail", "")
        return await xx.edit(
            f"**ERROR ~** `{dr['title']}`,\n`{de}`",
        )
    zz = Image.open(out)
    if zz.mode != "RGB":
        zz.convert("RGB")
    wbn = check_filename("ayra-rmbg.webp")
    zz.save(wbn, "webp")
    await event.client.send_file(
        event.chat_id,
        out,
        force_document=True,
        reply_to=reply,
    )
    await event.client.send_file(event.chat_id, wbn, reply_to=reply)
    os.remove(out)
    os.remove(wbn)
    await xx.delete()
