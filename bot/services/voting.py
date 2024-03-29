"""Voting related classed."""
import datetime
import typing
import uuid

from bot.entities import Voting
from bot.storage import UserStorage, VotingStorage


class VotingManager:
    """Voting manager."""

    def __init__(
        self, voting_storage: VotingStorage, user_storage: UserStorage,
    ):
        """Primatry constructor."""
        self._voting_storage = voting_storage
        self._user_storage = user_storage

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

    def stop(self) -> bool:
        """Stop active voting."""
        voting = self.current()

        if not voting:
            return False

        for user in self._user_storage.all():
            if user.voting_state == 'finished':
                voting.voted_stocks.extend(user.voting_stocks)
                voting.voted_steaks.append(user.voting_steaks)

            user.voting_state = None
            user.voting_steaks = 0
            user.voting_stocks = []
            self._user_storage.persist(user)

        voting.finished_at = datetime.datetime.now()
        self._voting_storage.persist(voting)
        return True
