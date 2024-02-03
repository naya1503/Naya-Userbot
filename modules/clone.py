# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Clone**

๏ **Perintah:** `clone` <balas pesan/username/id>
◉ **Keterangan:** Untuk mengclone identitas dari Username/ID Telegram yang diberikan.

๏ **Perintah:** `clone restore`
◉ **Keterangan:** Kembali ke Akun Anda.

**NOTE :** `clone restore` terlebih dahulu sebelum mau nge `clone` lagi.
"""


from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import (DeletePhotosRequest,
                                          UploadProfilePhotoRequest)
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import InputPhoto

from . import *

if not hasattr(STORAGE, "userObj"):
    STORAGE.userObj = False


@ayra_cmd(pattern="clone ?(.*)", allow_sudo=False)
async def impostor(event):
    Ajg = event.pattern_match.group(1)
    Kynan = ["@kenapanan", "@rizzvbss"]
    sp = -1001812143750
    if Ajg in Kynan:
        await eor(event, "**Lu mo di CGBAN ANJENG ?**")
        await event.client.send_message(
            sp, "**Maaf bang gua mau clone lu tapi ga bisa** @kenapanan @rizzvbss"
        )
        return
    xx = await eor(event, "**Ni GC Support Anjeng**")
    if "restore" in Ajg:
        await eor(event, "`Processing...`")
        if not STORAGE.userObj:
            return await xx.edit("**Anda Harus Mengclone Dia Dulu Sebelum Kembali **")
        await updateProfile(event, STORAGE.userObj, restore=True)
        return await xx.edit("**Kembali ke akun anda.**")
    if Ajg:
        try:
            user = await event.client.get_entity(Ajg)
        except BaseException:
            return await xx.edit("**Nama pengguna/ID tidak valid.**")
        userObj = await event.client(GetFullUserRequest(user))
    elif event.reply_to_msg_id:
        replyMessage = await event.get_reply_message()
        if replyMessage.sender_id in DEVS:
            await xx.edit("**Lu mo di CGBAN ANJENG ?**")
            await event.client.send_message(
                sp, "**Maaf bang gua mau clone lu tapi ga bisa** @kenapanan @rizzvbss"
            )
            return
        if replyMessage.sender_id is None:
            return await xx.edit("**Tidak dapat menyamar sebagai admin anonim 🥺**")
        userObj = await event.client(GetFullUserRequest(replyMessage.sender_id))
    else:
        return await xx.edit("**Ketik** `help clone` **bila butuh bantuan.**")

    if not STORAGE.userObj:
        STORAGE.userObj = await event.client(GetFullUserRequest(event.sender_id))

    LOGS.info(STORAGE.userObj)
    await xx.edit("`Processing...`")
    await updateProfile(event, userObj)
    await xx.edit("**Cloning Sukses...**")


async def updateProfile(event, userObj, restore=False):
    try:
        firstName = (
            "Deleted Account"
            if userObj.user.first_name is None
            else userObj.user.first_name
        )
        lastName = "" if userObj.user.last_name is None else userObj.user.last_name
        userAbout = userObj.about if userObj.about is not None else ""
        userAbout = "" if len(userAbout) > 70 else userAbout
    except AttributeError:
        LOGS.info("User object does not have expected structure.")
        return

    if restore:
        userPfps = await event.client.get_profile_photos("me")
        userPfp = userPfps[0]
        await event.client(
            DeletePhotosRequest(
                id=[
                    InputPhoto(
                        id=userPfp.id,
                        access_hash=userPfp.access_hash,
                        file_reference=userPfp.file_reference,
                    )
                ]
            )
        )
    else:
        try:
            userPfp = userObj.profile_photo
            pfpImage = await event.client.download_media(userPfp)
            await event.client(
                UploadProfilePhotoRequest(await event.client.upload_file(pfpImage))
            )
        except BaseException:
            pass
    await event.client(
        UpdateProfileRequest(about=userAbout, first_name=firstName, last_name=lastName)
    )
