import discord
import databaseExtensions as Extension
import datetime

from config import settings, SettingsEnum as Settings_enum

min_word_size = settings[Settings_enum.MIN_WORD_SIZE.value]
max_word_size = settings[Settings_enum.MAX_WORD_SIZE.value]
reputation_cooldown = settings[Settings_enum.REPUTATION_COOLDOWN.value]
reputation_cooldowns = {}


def add_reputation(member: discord.Member, amount: int):
    Extension.add_reputation_to_member(member, amount, settings[Settings_enum.THRESHOLD.value])


def subtract_reputation(member: discord.Member, amount: int):
    Extension.subtract_reputation_from_member(member, amount, settings[Settings_enum.THRESHOLD.value])


def add_reputation_by_word(member: discord.Member, content: str):
    if member.bot:
        return
    user_id = member.id
    now = datetime.datetime.now()
    words = content.split(' ')
    points = 0
    if user_id in reputation_cooldowns:
        if user_id in reputation_cooldowns:
            time_since_last_reputation = now - reputation_cooldowns[user_id]
            if time_since_last_reputation < datetime.timedelta(seconds=reputation_cooldown):
                return
    for word in words:
        len_word = len(word)
        if min_word_size <= len_word <= max_word_size:
            points += settings[Settings_enum.POINTS_BY_WORD.value]
    if points > 0:
        add_reputation(member, points)
