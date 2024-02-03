import os
import sys
from glob import glob
from typing import Any, Dict, List, Union

from Ayra import *
from Ayra.fns.tools import translate

try:
    from yaml import safe_load
except ModuleNotFoundError:
    from Ayra.fns.tools import safe_load

AyConfig.lang = udB.get_key("language") or os.getenv("LANGUAGE", "id")

languages = {}

for file in glob("strings/strings/*yml"):
    if file.endswith(".yml"):
        code = file.split("/")[-1].split("\\")[-1][:-4]
        try:
            languages[code] = safe_load(
                open(file, encoding="UTF-8"),
            )
        except Exception as er:
            LOGS.info(f"Kesalahan {file[:-4]} bahasa")
            LOGS.exception(er)


def get_string(key: str, _res: bool = True) -> Any:
    lang = AyConfig.lang or "id"
    try:
        return languages[lang][key]
    except KeyError:
        try:
            id_ = languages["id"][key]
            tr = translate(id_, lang_tgt=lang).replace("\ N", "\n")
            if id_.count("{}") != tr.count("{}"):
                tr = id_
            if languages.get(lang):
                languages[lang][key] = tr
            else:
                languages.update({lang: {key: tr}})
            return tr
        except KeyError:
            if not _res:
                return
            return f"Peringatan: tidak dapat memuat string apa pun dengan kunci `{key}`"
        except TypeError:
            pass
        except Exception as er:
            LOGS.exception(er)
        if not _res:
            return None
        return languages["id"].get(key) or f"Gagal memuat string bahasa '{key}'"


def get_help(key):
    if doc := get_string(f"help_{key}", _res=False):
        return get_string("cmda") + doc


def get_languages() -> Dict[str, Union[str, List[str]]]:
    return {
        code: {
            "name": languages[code]["name"],
            "natively": languages[code]["natively"],
            "authors": languages[code]["authors"],
        }
        for code in languages
    }
