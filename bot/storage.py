"""Data storage."""
import abc
import pathlib
import typing

from bot.entities import Purchase, User, Voting


EntityT = typing.TypeVar('EntityT')


class NoEntityFound(Exception):
    """Raise if entity is not found."""


class BaseStorage(typing.Generic[EntityT], metaclass=abc.ABCMeta):
    """Storage."""

    @abc.abstractmethod
    def get(self, entity_id: str) -> EntityT:
        """Return entity from storage."""

    @abc.abstractmethod
    def all(self) -> typing.List[EntityT]:
        """Fetch all available entities."""

    @abc.abstractmethod
    def persist(self, user: EntityT):
        """Save entity to storage."""


class BaseFileStorage(BaseStorage[EntityT]):
    """File system storage.

    NOTE: it's not thread-safe.
    """

    def __init__(self, path: pathlib.Path):
        """Primary constructor."""
        self._path = path

    @property
    @abc.abstractmethod
    def entity_cls(self) -> typing.Type[EntityT]:
        """Return entity class."""

    @property
    @abc.abstractmethod
    def prefix(self) -> str:
        """Return template of filename."""

    def get(self, entity_id: typing.Union[str, int]) -> EntityT:
        """Fetch entity from disk."""
        entity_path = self._path / f'{self.prefix}_{entity_id}.json'

        if not entity_path.exists():
            raise NoEntityFound

        return self.entity_cls.parse_file(entity_path)

    def all(self) -> typing.List[EntityT]:
        """Fetch all available entities."""
        entities = []
        for path in self._path.iterdir():
            if path.name.startswith(self.prefix):
                entities.append(self.entity_cls.parse_file(path))
        return entities

    def persist(self, entity: EntityT):
        """Save user to disk."""
        entity_path = self._path / f'{self.prefix}_{entity.pk}.json'
        entity_path.write_text(entity.json())


class UserStorage(BaseFileStorage[User]):
    """Persist users to files."""

    entity_cls = User
    prefix = 'user'


class VotingStorage(BaseFileStorage[Voting]):
    """Persist voting to files."""

    entity_cls = Voting
    prefix = 'voting'


class PurchaseStorage(BaseFileStorage[Purchase]):
    """Persist purchases to files."""

    entity_cls = Purchase
    prefix = 'purchase'
