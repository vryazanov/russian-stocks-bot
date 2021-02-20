"""Logging initializers."""
import logging.config

import bot.settings


def setup_logging():
    """Prepare logging configuration."""
    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'detailed': {
                'class': 'logging.Formatter',
                'format': '%(asctime)s %(name)-15s %(levelname)-8s %(processName)-10s %(message)s',  # noqa
            },
            'telegram': {
                'class': 'telegram_handler.HtmlFormatter',
                'fmt': '%(levelname)s %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'detailed',
            },
            'telegram': {
                'class': 'telegram_handler.TelegramHandler',
                'formatter': 'telegram',
                'level': 'ERROR',
                'token': bot.settings.BOT_TOKEN,
                'chat_id': bot.settings.BOT_ADMIN_GROUP,
            },
        },
        'loggers': {
            '': {
                'handlers': ['console', 'telegram'],
                'level': 'INFO',
            },
        },
    })
