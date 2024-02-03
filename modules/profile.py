# Ultroid - UserBot
# Copyright (C) 2021-2023 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Profile**

๏ **Perintah:** `setname` <first name/last name>
◉ **Keterangan:** Ubah nama anda.

๏ **Perintah:** `setbio` <balas pesan>
◉ **Keterangan:** Ubah bio anda.

๏ **Perintah:** `setfp` <balas pesan>
◉ **Keterangan:** Ubah foto profil anda.

๏ **Perintah:** `delfp` <jumlah>
◉ **Keterangan:** Hapus satu foto profil, jika tidak ada nilai yang diberikan atau hapus jumlah foto.
"""
import os

from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import (DeletePhotosRequest,
                                          UploadProfilePhotoRequest)

from . import ayra_cmd, eod, eor, get_string, mediainfo

TMP_DOWNLOAD_DIRECTORY = "resources/downloads/"

# bio changer


@ayra_cmd(pattern="[Ss]etbio( (.*)|$)", fullsudo=False)
async def _(ayra):
    ok = await ayra.eor("...")
    set = ayra.pattern_match.group(1).strip()
    try:
        await ayra.client(UpdateProfileRequest(about=set))
        await eod(ok, f"Bio profil diubah menjadi\n`{set}`")
    except Exception as ex:
        await eod(ok, f"Terjadi kesalahan.\n`{str(ex)}`")


# name changer


@ayra_cmd(pattern="[Ss]etname ?((.|//)*)", fullsudo=False)
async def _(ayra):
    ok = await ayra.eor("...")
    names = ayra.pattern_match.group(1).strip()
    first_name = names
    last_name = ""
    if "//" in names:
        first_name, last_name = names.split("//", 1)
    try:
        await ayra.client(
            UpdateProfileRequest(
                first_name=first_name,
                last_name=last_name,
            ),
        )
        await eod(ok, f"Nama diubah menjadi `{names}`")
    except Exception as ex:
        await eod(ok, f"Terjadi kesalahan.\n`{str(ex)}`")


# profile pic


@ayra_cmd(pattern="[sS]etfp$", fullsudo=False)
async def _(ayra):
    if not ayra.is_reply:
        return await ayra.eor("`Balas ke Media..`", time=5)
    reply_message = await ayra.get_reply_message()
    ok = await ayra.eor(get_string("com_1"))
    replfile = await reply_message.download_media()
    file = await ayra.client.upload_file(replfile)
    try:
        if "pic" in mediainfo(reply_message.media):
            await ayra.client(UploadProfilePhotoRequest(file))
        else:
            await ayra.client(UploadProfilePhotoRequest(video=file))
        await eod(ok, "`Foto Profil Berhasil Diubah !`")
    except Exception as ex:
        await eod(ok, f"Terjadi kesalahan.\n`{str(ex)}`")
    os.remove(replfile)


# delete profile pic(s)


@ayra_cmd(pattern="[dD]elfp( (.*)|$)", fullsudo=False)
async def remove_profilepic(delpfp):
    ok = await eor(delpfp, "`...`")
    group = delpfp.text[8:]
    if group == "all":
        lim = 0
    elif group.isdigit():
        lim = int(group)
    else:
        lim = 1
    pfplist = await delpfp.client.get_profile_photos("me", limit=lim)
    await delpfp.client(DeletePhotosRequest(pfplist))
    await eod(ok, f"`Berhasil dihapus {len(pfplist)} gambar profil(s).`")


@ayra_cmd(pattern="[pP]oto( (.*)|$)")
async def gpoto(e):
    ayra = e.pattern_match.group(1).strip()
    a = await e.eor(get_string("com_1"))
    just_dl = ayra in ["-dl", "--dl"]
    if just_dl:
        ayra = None
    if not ayra:
        if e.is_reply:
            gs = await e.get_reply_message()
            ayra = gs.sender_id
        else:
            ayra = e.chat_id
    okla = await e.client.download_profile_photo(ayra)
    if not okla:
        return await eor(a, "`Foto Profil Tidak Ditemukan...`")
    if not just_dl:
        await a.delete()
        await e.reply(file=okla)
        return os.remove(okla)
    await a.edit(f"Mengunduh pfp ke [ `{okla}` ].")
