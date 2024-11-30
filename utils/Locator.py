from uuid import UUID
from pygame.rect import Rect

from utils import Entity

class Locator:

    _map: dict[type, list[Entity]] = {}
    _interactables: list[tuple[UUID, Rect]] = []

    @staticmethod
    def add(entity: Entity) -> None:
        type_ = entity.__class__
        if type_ not in Locator._map:
            Locator._map[type_] = []
        Locator._map[type_].append(entity)


    @staticmethod
    def get(interface: type) -> list[Entity]:
        return Locator._map.get(interface, [])
    

    @staticmethod
    def add_interactable(entity: Entity, rect: Rect) -> None:
        Locator._interactables.append((entity.id, rect))


    @staticmethod
    def get_interactables() -> list[tuple[UUID, Rect]]:
        return Locator._interactables
    

    @staticmethod
    def clear_interactables() -> None:
        Locator._interactables.clear()