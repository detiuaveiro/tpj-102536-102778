from uuid import uuid4, UUID

from utils import Observer


class Entity(Observer):
    """
    Base class for all entities that interact with the game.
    """

    def __init__(self):
        """
        Attributes
        ----------
        id (UUID): 
            Unique identifier for the entity.
        """
        super().__init__()
        self.id: UUID = uuid4()

    def __eq__(self, other):
        if isinstance(other, Entity):
            return self.id == other.id
        return False


    def __hash__(self):
        return self.id.int
    

    def __str__(self):
        return f"{self.__class__.__name__}({self.id})"
