"""Voting related classed."""
import datetime
import typing
import uuid

from bot.entities import Voting
from bot.storage import VotingStorage, UserStorage


class VotingManager:
    """Voting manager."""

    def __init__(self, voting_storage: VotingStorage):
        """Primatry constructor."""
        self._voting_storage = voting_storage

    def current(self) -> typing.Optional[Voting]:
        """Check if any voting available."""
        for voting in self._voting_storage.all():
            if voting.finished_at is None:
                return voting

    def start(self, stocks: int, steaks: int):
        """Start a new voting."""
        self._voting_storage.persist(
            Voting(
                id=uuid.uuid4(),
                participants=[],
                max_stocks=stocks,
                max_steaks=steaks,
                voted_stocks=[],
                voted_steaks=[],
                started_at=datetime.datetime.now(),
                finished_at=None,
            ),
        )
