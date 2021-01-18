"""Voting constants."""
import enum


class ActionEnum(str, enum.Enum):
    """Voting action."""

    ask_for_stocks = 'ask_for_stocks'
    ask_for_steaks = 'ask_for_steaks'
    vote_for_stock = 'vote_for_stock'
    vote_for_steak = 'vote_for_steak'
    finish = 'finish'
    repeat = 'repeat'


class StateEnum(str, enum.Enum):
    """Voting state."""

    initial = 'initial'
    revote = 'revote'
    waiting_for_stock = 'waiting_for_stock'
    stock = 'stock'
    nothing_more = 'nothing_more'
    waiting_for_steak = 'waiting_for_steak'
    steak = 'steak'
    finished = 'finished'
