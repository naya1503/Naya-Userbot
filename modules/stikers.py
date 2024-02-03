# Ultroid - UserBot
# Copyright (C) 2021-2023 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Stikers**

๏ **Perintah:** `destroy` <balas stikers>
◉ **Keterangan:** Untuk menghancurkan stiker.

๏ **Perintah:** `tiny` <balas foto>
◉ **Keterangan:** Untuk membuat stiker Tiny.

๏ **Perintah:** `kang` <balas stiker>
◉ **Keterangan:** Kang stikernya (tambahkan ke paket Anda).

๏ **Perintah:** `packkang` <balas stiker <nama pack>
◉ **Keterangan:** Kang set sticker Lengkap (dengan nama kustom).

๏ **Perintah:** `round` <balas media>
◉ **Keterangan:** Untuk membuat stiker bulat.
"""
import glob
import io
import os
import random
from os import remove

try:
    import cv2
except ImportError:
    cv2 = None
try:
    import numpy as np
except ImportError:
    np = None
try:
    from PIL import Image, ImageDraw
except ImportError:
    pass

from telethon.errors import PeerIdInvalidError, YouBlockedUserError
from telethon.tl.functions.messages import UploadMediaRequest
from telethon.tl.types import (DocumentAttributeFilename,
                               DocumentAttributeSticker, InputPeerSelf)
from telethon.utils import get_input_document

from . import *


@ayra_cmd(pattern="[pP]ackkang")
async def pack_kangish(_):
    _e = await _.get_reply_message()
    ayra_bot = _.client
    local = None
    user = ayra_bot.me
    username = user.username
    username = f"@{username}" if username else user.first_name
    try:
        cmdtext = _.text.split(maxsplit=1)[1]
    except IndexError:
        cmdtext = None
    if cmdtext and os.path.isdir(cmdtext):
        local = True
    elif not (_e and _e.sticker and _e.file.mime_type == "image/webp"):
        return await _.eor(get_string("sts_4"))
    msg = await _.eor(get_string("com_1"))
    _packname = cmdtext or f"Kang Pack By {user.id}"
    typee = None
    if not local:
        _id = _e.media.document.attributes[1].stickerset.id
        _hash = _e.media.document.attributes[1].stickerset.access_hash
        _get_stiks = await _.client(
            functions.messages.GetStickerSetRequest(
                stickerset=types.InputStickerSetID(id=_id, access_hash=_hash), hash=0
            )
        )
        docs = _get_stiks.documents
    else:
        docs = []
        files = glob.glob(f"{cmdtext}/*")
        exte = files[-1]
        if exte.endswith(".tgs"):
            typee = "anim"
        elif exte.endswith(".webm"):
            typee = "vid"
        count = 0
        for file in files:
            if file.endswith((".tgs", ".webm")):
                count += 1
                upl = await asst.upload_file(file)
                docs.append(await asst(UploadMediaRequest(InputPeerSelf(), upl)))
                if count % 5 == 0:
                    await msg.edit(f"`Uploaded {count} files.`")

    stiks = []
    for i in docs:
        x = get_input_document(i)
        stiks.append(
            types.InputStickerSetItem(
                document=x,
                emoji=random.choice(["😐", "👍", "😂"])
                if local
                else (i.attributes[1]).alt,
            )
        )
    try:
        short_name = "ayra_" + _packname.replace(" ", "_") + str(_.id)
        _r_e_s = await asst(
            functions.stickers.CreateStickerSetRequest(
                user_id=_.sender_id,
                title=_packname,
                short_name=f"{short_name}_by_{asst.me.username}",
                animated=typee == "anim",
                videos=typee == "vid",
                stickers=stiks,
            )
        )
    except PeerIdInvalidError:
        return await msg.eor(
            f"Hey {inline_mention(_.sender)} Kirim `/start` to @{asst.me.username} dan kemudian coba perintah ini lagi.."
        )
    except BaseException as er:
        LOGS.exception(er)
        return await msg.eor(str(er))
    await msg.eor(
        get_string("sts_5").format(f"https://t.me/addstickers/{_r_e_s.set.short_name}"),
    )


@ayra_cmd(
    pattern="[kK]ang",
)
async def hehe(args):
    ayra_bot = args.client
    xx = await args.eor(get_string("com_1"))
    user = ayra_bot.me
    username = user.username
    username = f"@{username}" if username else user.first_name
    message = await args.get_reply_message()
    photo = None
    is_anim, is_vid = False, False
    emoji = None
    if not message:
        return await xx.eor(get_string("sts_6"))
    if message.photo:
        photo = io.BytesIO()
        photo = await ayra_bot.download_media(message.photo, photo)
    elif message.file and "image" in message.file.mime_type.split("/"):
        photo = io.BytesIO()
        await ayra_bot.download_file(message.media.document, photo)
        if (
            DocumentAttributeFilename(file_name="sticker.webp")
            in message.media.document.attributes
        ):
            emoji = message.media.document.attributes[1].alt

    elif message.file and "video" in message.file.mime_type.split("/"):
        xy = await message.download_media()
        if (message.file.duration or 0) <= 10:
            is_vid = True
            photo = await con.create_webm(xy)
        else:
            y = cv2.VideoCapture(xy)
            heh, lol = y.read()
            cv2.imwrite("ayra.webp", lol)
            photo = "ayra.webp"
    elif message.file and "tgsticker" in message.file.mime_type:
        await ayra_bot.download_file(
            message.media.document,
            "AnimatedSticker.tgs",
        )
        attributes = message.media.document.attributes
        for attribute in attributes:
            if isinstance(attribute, DocumentAttributeSticker):
                emoji = attribute.alt
        is_anim = True
        photo = 1
    elif message.message:
        photo = await quotly.create_quotly(message)
    else:
        return await xx.edit(get_string("com_4"))
    if not udB.get_key("language") or udB.get_key("language") == "id":
        ra = random.choice(KANGING_STR)
    else:
        ra = get_string("sts_11")
    await xx.edit(f"`{ra}`")
    if photo:
        splat = args.text.split()
        pack = 1
        if not emoji:
            emoji = "🗿"
        if len(splat) == 3:
            pack = splat[2]  # User sent ayra_both
            emoji = splat[1]
        elif len(splat) == 2:
            if splat[1].isnumeric():
                pack = int(splat[1])
            else:
                emoji = splat[1]

        packname = f"Sticker_u{user.id}_Ke{pack}"
        packnick = f"{username}'s Pack {pack}"
        cmd = "/newpack"
        file = io.BytesIO()

        if is_vid:
            packname += "_vid"
            packnick += " (Video)"
            cmd = "/newvideo"
        elif is_anim:
            packname += "_anim"
            packnick += " (Animated)"
            cmd = "/newanimated"
        else:
            image = con.resize_photo_sticker(photo)
            file.name = "sticker.png"
            image.save(file, "PNG")

        response = await async_searcher(f"http://t.me/addstickers/{packname}")
        htmlstr = response.split("\n")

        if (
            "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>."
            not in htmlstr
        ):
            async with ayra_bot.conversation("@Stickers") as conv:
                try:
                    await conv.send_message("/addsticker")
                except YouBlockedUserError:
                    LOGS.info("Unblocking @Stickers for kang...")
                    await ayra_bot(functions.contacts.UnblockRequest("stickers"))
                    await conv.send_message("/addsticker")
                await conv.get_response()
                await conv.send_message(packname)
                x = await conv.get_response()
                if x.text.startswith("Alright! Now send me the video sticker."):
                    await conv.send_file(photo, force_document=True)
                    x = await conv.get_response()
                t = "50" if (is_anim or is_vid) else "120"
                while t in x.message:
                    pack += 1
                    packname = f"Sticker_u{user.id}_Ke{pack}"
                    packnick = f"{username}'s Pack {pack}"
                    if is_anim:
                        packname += "_anim"
                        packnick += " (Animated)"
                    elif is_vid:
                        packnick += " (Video)"
                        packname += "_vid"
                    await xx.edit(get_string("sts_13").format(pack))
                    await conv.send_message("/addsticker")
                    await conv.get_response()
                    await conv.send_message(packname)
                    x = await conv.get_response()
                    if x.text.startswith("Alright! Now send me the video sticker."):
                        await conv.send_file(photo, force_document=True)
                        x = await conv.get_response()
                    if x.text in ["Invalid pack selected.", "Invalid set selected."]:
                        await conv.send_message(cmd)
                        await conv.get_response()
                        await conv.send_message(packnick)
                        await conv.get_response()
                        if is_anim:
                            await conv.send_file("AnimatedSticker.tgs")
                            remove("AnimatedSticker.tgs")
                        else:
                            if is_vid:
                                file = photo
                            else:
                                file.seek(0)
                            await conv.send_file(file, force_document=True)
                        await conv.get_response()
                        await conv.send_message(emoji)
                        await conv.get_response()
                        await conv.send_message("/publish")
                        if is_anim:
                            await conv.get_response()
                            await conv.send_message(f"<{packnick}>")
                        await conv.get_response()
                        await conv.send_message("/skip")
                        await conv.get_response()
                        await conv.send_message(packname)
                        await conv.get_response()
                        await xx.edit(
                            get_string("sts_7").format(packname),
                            parse_mode="md",
                        )
                        return
                if is_anim:
                    await conv.send_file("AnimatedSticker.tgs")
                    remove("AnimatedSticker.tgs")
                elif "send me an emoji" not in x.message:
                    if is_vid:
                        file = photo
                    else:
                        file.seek(0)
                    await conv.send_file(file, force_document=True)
                    rsp = await conv.get_response()
                    if "Sorry, the file type is invalid." in rsp.text:
                        await xx.edit(
                            get_string("sts_8"),
                        )
                        return
                await conv.send_message(emoji)
                await conv.get_response()
                await conv.send_message("/done")
                await conv.get_response()
                await ayra_bot.send_read_acknowledge(conv.chat_id)
        else:
            await xx.edit("`Brewing a new Pack...`")
            async with ayra_bot.conversation("Stickers") as conv:
                await conv.send_message(cmd)
                await conv.get_response()
                await conv.send_message(packnick)
                await conv.get_response()
                if is_anim:
                    await conv.send_file("AnimatedSticker.tgs")
                    remove("AnimatedSticker.tgs")
                else:
                    if is_vid:
                        file = photo
                    else:
                        file.seek(0)
                    await conv.send_file(file, force_document=True)
                rsp = await conv.get_response()
                if "Sorry, the file type is invalid." in rsp.text:
                    await xx.edit(
                        get_string("sts_8"),
                    )
                    return
                await conv.send_message(emoji)
                await conv.get_response()
                await conv.send_message("/publish")
                if is_anim:
                    await conv.get_response()
                    await conv.send_message(f"<{packnick}>")

                await conv.get_response()
                await conv.send_message("/skip")
                await conv.get_response()
                await conv.send_message(packname)
                await conv.get_response()
                await ayra_bot.send_read_acknowledge(conv.chat_id)
        await xx.edit(
            get_string("sts_12").format(emoji, packname),
            parse_mode="md",
        )
        try:
            os.remove(photo)
        except BaseException:
            pass


@ayra_cmd(
    pattern="[rR]ound$",
)
async def ayraround(event):
    ureply = await event.get_reply_message()
    xx = await event.eor(get_string("com_1"))
    if not (ureply and (ureply.media)):
        await xx.edit(get_string("sts_10"))
        return
    ayra = await ureply.download_media()
    file = await con.convert(
        ayra,
        convert_to="png",
        allowed_formats=["jpg", "jpeg", "png"],
        outname="round",
        remove_old=True,
    )
    img = Image.open(file).convert("RGB")
    npImage = np.array(img)
    h, w = img.size
    alpha = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0, 0, h, w], 0, 360, fill=255)
    npAlpha = np.array(alpha)
    npImage = np.dstack((npImage, npAlpha))
    Image.fromarray(npImage).save("ayra.webp")
    await event.client.send_file(
        event.chat_id,
        "ayra.webp",
        force_document=False,
        reply_to=event.reply_to_msg_id,
    )
    await xx.delete()
    os.remove(file)
    os.remove("ayra.webp")


@ayra_cmd(
    pattern="[Dd]estroy$",
)
async def ayradestroy(event):
    ayra = await event.get_reply_message()
    if not (ayra and ayra.media and "animated" in mediainfo(ayra.media)):
        return await event.eor(get_string("sts_2"))
    await event.client.download_media(ayra, "ayra.tgs")
    xx = await event.eor(get_string("com_1"))
    await bash("lottie_convert.py ayra.tgs json.json")
    with open("json.json") as json:
        jsn = json.read()
    jsn = (
        jsn.replace("[100]", "[200]")
        .replace("[10]", "[40]")
        .replace("[-1]", "[-10]")
        .replace("[0]", "[15]")
        .replace("[1]", "[20]")
        .replace("[2]", "[17]")
        .replace("[3]", "[40]")
        .replace("[4]", "[37]")
        .replace("[5]", "[60]")
        .replace("[6]", "[70]")
        .replace("[7]", "[40]")
        .replace("[8]", "[37]")
        .replace("[9]", "[110]")
    )
    open("json.json", "w").write(jsn)
    file = await con.animated_sticker("json.json", "ayra.tgs")
    if file:
        await event.client.send_file(
            event.chat_id,
            file="ayra.tgs",
            force_document=False,
            reply_to=event.reply_to_msg_id,
        )
    await xx.delete()
    os.remove("json.json")


@ayra_cmd(
    pattern="[Tt]iny$",
)
async def ayratiny(event):
    reply = await event.get_reply_message()
    if not (reply and (reply.media)):
        await event.eor(get_string("sts_10"))
        return
    xx = await event.eor(get_string("com_1"))
    ik = await reply.download_media()
    im1 = Image.open("resources/extras/blank.png")
    if ik.endswith(".tgs"):
        await con.animated_sticker(ik, "json.json")
        with open("json.json") as json:
            jsn = json.read()
        jsn = jsn.replace("512", "2000")
        open("json.json", "w").write(jsn)
        await con.animated_sticker("json.json", "ayra.tgs")
        file = "ayra.tgs"
        os.remove("json.json")
    elif ik.endswith((".gif", ".webm", ".mp4")):
        iik = cv2.VideoCapture(ik)
        dani, busy = iik.read()
        cv2.imwrite("i.png", busy)
        fil = "i.png"
        im = Image.open(fil)
        z, d = im.size
        if z == d:
            xxx, yyy = 200, 200
        else:
            t = z + d
            a = z / t
            b = d / t
            aa = (a * 100) - 50
            bb = (b * 100) - 50
            xxx = 200 + 5 * aa
            yyy = 200 + 5 * bb
        k = im.resize((int(xxx), int(yyy)))
        k.save("k.png", format="PNG", optimize=True)
        im2 = Image.open("k.png")
        back_im = im1.copy()
        back_im.paste(im2, (150, 0))
        back_im.save("o.webp", "WEBP", quality=95)
        file = "o.webp"
        os.remove(fil)
        os.remove("k.png")
    else:
        im = Image.open(ik)
        z, d = im.size
        if z == d:
            xxx, yyy = 200, 200
        else:
            t = z + d
            a = z / t
            b = d / t
            aa = (a * 100) - 50
            bb = (b * 100) - 50
            xxx = 200 + 5 * aa
            yyy = 200 + 5 * bb
        k = im.resize((int(xxx), int(yyy)))
        k.save("k.png", format="PNG", optimize=True)
        im2 = Image.open("k.png")
        back_im = im1.copy()
        back_im.paste(im2, (150, 0))
        back_im.save("o.webp", "WEBP", quality=95)
        file = "o.webp"
        os.remove("k.png")
    if os.path.exists(file):
        await event.client.send_file(
            event.chat_id, file, reply_to=event.reply_to_msg_id
        )
        os.remove(file)
    await xx.delete()
    os.remove(ik)
