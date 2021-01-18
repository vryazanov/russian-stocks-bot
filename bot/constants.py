"""Project contants."""
import enum


class Commands(str, enum.Enum):
    """Bot commands."""

    start_voting = '\U0001F4DD Участвовать в опросе'
    repeat_voting = '\U000021A9 Переголосовать'
    nothing_to_buy = '\U0000274C Ничего не покупать'
    nothing_more = '\U000027A1 Закончить выбор'
    rules = '\U0001F4DA Правила'
    to_menu = '\U0001F4F2 В главное меню'
