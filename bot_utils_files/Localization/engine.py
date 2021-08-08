# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUB > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import logging
import os
import yaml     
import pathlib
from database.localdb import check_lang
from main_startup.config_var import Config
from main_startup import (
    CMD_LIST,
    XTRA_CMD_LIST,
    Config,
    Friday,
    Friday2,
    Friday3,
    Friday4,
    bot
)

language_string = {}

class Engine:
    def __init__(self):
        self.path = "./bot_utils_files/Localization/strings/"
        
    def get_all_files_in_path(self, path):
        path = pathlib.Path(path)
        return [i.absolute() for i in path.glob("**/*")]

    def load_language(self):
        all_files = self.get_all_files_in_path(self.path)
        for filepath in all_files:
            with open(filepath) as f:
                data = yaml.safe_load(f)
                language_to_load = data.get("language")
                logging.debug(f"Loading : {language_to_load}")
                language_string[language_to_load] = data
        logging.debug("All language Loaded.")
        
    def get_string(self, string):
        lang_ = Friday.selected_lang
        return (
            language_string.get(lang_).get(string)
            or f"**404_STRING_NOT_FOUND :** `String {string} Not Found in {lang} String 	File. - Please Report It To @FridayChat`"
        )
