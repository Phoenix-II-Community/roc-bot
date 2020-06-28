#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from rapidfuzz import process
from pathlib import Path
import json
import re
import unicodedata
import random
import discord
import discord.ext.commands
from discord.ext import commands
from discord.utils import get
import settings

bot = commands.Bot(command_prefix="!")


# Open the required json files and assign it to a variable foo_data
home_dir = Path.home()

invaders_json = open(('{hd}/scripts/apex-bot/res/invaders.json').format(hd=home_dir))
invaders_data = json.load(invaders_json)
