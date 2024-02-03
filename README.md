<p align="center">
  <img src="./resources/extras/logo.jpg" alt="Ayra Logo">
</p>
<h1 align="center">
  <b>иᴀʏᴀ ꭙ ᴜꜱᴇʀʙᴏᴛ​</b>
</h1>

<b>A stable pluggable Telegram userbot + Voice & Video Call music bot, based on Telethon and Pyrogram</b>


[![Last Commit](https://img.shields.io/github/last-commit/naya1503/Naya-Userbot?color=red&logo=github&logoColor=blue&style=for-the-badge)](https://github.com/naya1503/Naya-Userbot/commits)
[![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.png?v=103)](https://github.com/naya1503/Naya-Userbot)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-Yes-blue)](https://GitHub.com/naya1503/Naya-Userbot/graphs/commit-activity)
[![CodeQuality](https://img.shields.io/codacy/grade/a723cb464d5a4d25be3152b5d71de82d?color=blue&logo=codacy)](https://app.codacy.com/gh/naya1503/Naya-Userbot/dashboard)
[![GitHub Forks](https://img.shields.io/github/forks/naya1503/Naya-Userbot?&logo=github)](https://github.com/naya1503/Naya-Userbot/fork)
[![GitHub Stars](https://img.shields.io/github/stars/naya1503/Naya-Userbot?&logo=github)](https://github.com/naya1503/Naya-Userbot/stargazers)
----

## Disclaimer

```
Saya tidak bertanggung jawab atas penyalahgunaan bot ini.
Bot ini dimaksudkan untuk bersenang-senang sekaligus membantu anda
mengelola grup secara efisien dan mengotomatiskan beberapa hal yang membosankan.
Gunakan bot ini dengan risiko Anda sendiri, dan gunakan userbot ini dengan bijak.
```

# DATABASE REQUIRETMENTS :
- MONGODB


<details>
<summary><b>🔗 Deploy Via Screen</b></summary>
<br>

• `sudo apt-get update && sudo apt-get upgrade -y`

• `sudo pip3 install -U pip`

• `sudo apt-get install python3-pip ffmpeg -y`

 • `git clone https://github.com/naya1503/Naya-Userbot`

 • `cd Naya-Userbot`

 • `bash installer.sh`

 • `nano .env`
  - isi vars .env API_ID, API_HASH, MONGO_URI SESSION
  - Jika sudah 
  - ketik ctrl + S
  - ctrl + X

 • `screen -S naya`

 • `bash start`

</details>

<details>
<summary><b>🔗 Deploy Via Docker</b></summary>
<br>

• `curl -sSL https://get.docker.com | sh`

 • `git clone https://github.com/naya1503/Naya-Userbot`

 • `cd Naya-Userbot`

 • `cp sample.env .env`

 • `nano .env`
  - isi vars .env API_ID, API_HASH, SESSION dan MONGO_URI
  - Jika sudah 
  - ketik ctrl + S
  - ctrl + X

 • `docker build . -t naya`

 • `docker run --name namalu --cpus 1.2 --memory 500m --env-file .env naya`

</details>

<details>
<summary><b>🔗 Deploy on Heroku</b></summary>
<br>
• Silakan isi vars yang diperlukan API_ID, API_HASH, SESSION, HEROKU_API dan HEROKU_APP_NAME

<h3 align="center">Click The Button</h3>
<a align="center" href="https://dashboard.heroku.com/new?template=https://github.com/naya1503/Naya-Userbot"><img src="https://www.herokucdn.com/deploy/button.svg"></a>
</div>

</details>



#### Special Thanks To
* [Everyone](https://github.com/mrismanaziz/Man-Userbot/graphs/contributors) Who Has Helped Make This Userbot Awesome!
* [AdekMaulana](https://github.com/adekmaulana) : ProjectBish
* [RaphielGang](https://github.com/RaphielGang) : Paperplane
* [TeamUltroid](https://github.com/TeamUltroid/Ultroid) :  UltroidUserbot
* [BianSepang](https://github.com/BianSepang/WeebProject) : WeebProject
* [Sandy1709](https://github.com/sandy1709/catuserbot) : CatUserbot
* [X_ImFine](https://github.com/ximfine) :  XBot-REMIX
* [Risman](https://github.com/mrismanaziz/Man-Userbot) :  Man-Userbot
* [Koala](https://github.com/ManusiaRakitan/Kampang-Bot) : Kampang-Bot
* [Alvin](https://github.com/Zora24/Lord-Userbot) : Lord-Userbot
* [AyiinXd](https://github.com/AyiinXd/Ayiin-Userbot) : Ayiin-Userbot

## © Credits
* [TeamUltroid](https://github.com/TeamUltroid) for [Ultroid](https://github.com/TeamUltroid/Ultroid)
* [Lonami](https://github.com/LonamiWebs/) for [Telethon](https://github.com/LonamiWebs/Telethon)
* [MarshalX](https://github.com/MarshalX) for [PyTgCalls](https://github.com/MarshalX/tgcalls)
* [Risman](https://github.com/mrismanaziz) for [Man-Userbot](https://github.com/mrismanaziz/Man-Userbot)
* [AyiinXd](https://github.com/AyiinXd) for [Ayiin-Userbot](https://github.com/AyiinXd/Ayiin-Userbot)
* [Kynan](https://github.com/naya1503) for [Naya-Userbot](https://github.com/naya1503/Naya-Userbot)

## Made By
* [![TeamUltroid-Devs](https://img.shields.io/static/v1?label=Teamultroid&message=devs&color=critical)](https://t.me/UltroidDevs)

## Remake By
* [![Kynan.](https://img.shields.io/static/v1?label=Ky&message=nan&color=critical)](https://t.me/kenapanan)



# License
[![License](https://www.gnu.org/graphics/agplv3-155x51.png)](LICENSE)   
Naya-Userbot is licensed under [GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.en.html) v3 or later.
