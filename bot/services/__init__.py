"""Init for services."""
from bot.services.stocks import StockService
from bot.services.users import UserService
from bot.services.voting import VotingManager


__all__ = ('StockService', 'VotingManager', 'UserService')
