from uuid import UUID
from pygame.rect import Rect

from utils import Entity

class Locator:
    """
    Singleton class that manages the entities in the game.

    Static Attributes
    -----------------
    _map (dict[type, list[Entity]]): 
        Dictionary of entities by type.
    _interactables (list[tuple[UUID, Rect]]):
        List of interactable entities and their interaction area.
    _collidables (list[Entity]):
        List of collidable entities.
    """

    _map: dict[type, list[Entity]] = {}
    _interactables: list[tuple[UUID, Rect]] = []
    _collidables: list[Entity] = []


    def __new__(cls) -> None:
        raise Exception("This class is a singleton.")
    

    @staticmethod
    def add(entity: Entity) -> None:
        """
        Add an entity to the locator.

        Parameters
        ----------
        entity (Entity):
            Entity to be added to the locator.
        """
        type_ = entity.__class__
        if type_ not in Locator._map:
            Locator._map[type_] = []
        Locator._map[type_].append(entity)


    @staticmethod
    def get(interface: type) -> list[Entity]:
        """
        Get entities that implement the interface.

        Parameters
        ----------
        interface (type):
            Interface to be implemented by the entities.

        Returns
        -------
        list[Entity]:
            List of entities that implement the interface.
        """
        return Locator._map.get(interface, [])
    

    @staticmethod
    def add_interactable(entity: Entity, rect: Rect) -> None:
        """
        Add an interactable entity to the locator.

        Parameters
        ----------
        entity (Entity):
            Interactable entity to be added to the locator.
        rect (Rect):
            Interaction area of the entity.
        """
        Locator._interactables.append((entity.id, rect))


    @staticmethod
    def add_collidable(entity: Entity) -> None:
        """
        Add a collidable entity to the locator.

        Parameters
        ----------
        entity (Entity):
            Collidable entity to be added to the locator.
        """
        Locator._collidables.append(entity)


    @staticmethod
    def get_interactables() -> list[tuple[UUID, Rect]]:
        """
        Get the interactable entities and their interaction areas.

        Returns
        -------
        list[tuple[UUID, Rect]]:
            List of interactable entities and their interaction areas.
        """
        return Locator._interactables
    

    @staticmethod
    def get_collidables():
        """
        Get the collidable entities.

        Yields
        ------
        rect (Rect):
            Interaction area of the entity.
        """
        for entity in Locator._collidables:
            for rect in entity.get_blocks():
                yield rect
    

    @staticmethod
    def clear() -> None:
        """
        Clear the locator interactables and collidables.
        """
        Locator._interactables.clear()
        Locator._collidables.clear()