from Utils import Entity

class Locator:

    _map: dict[type, list[Entity]] = {}
    _all: list[Entity] = []

    @staticmethod
    def add(interface: type, entity: Entity) -> None:
        if interface not in Locator._map:
            Locator._map[interface] = []
        Locator._map[interface].append(entity)
        Locator._all.append(entity)


    @staticmethod
    def get(interface: type) -> list[Entity]:
        return Locator._map.get(interface, [])
    
    
    @staticmethod
    def get_all() -> list[Entity]:
        return Locator._all
    

    @staticmethod
    def remove(entity: Entity) -> None:
        for interface in Locator._map:
            if entity in Locator._map[interface]:
                Locator._map[interface].remove(entity)
        Locator._all.remove(entity)
    

    @staticmethod
    def get_collisions(entity: Entity) -> list[Entity]:
        collisions = []
        for other in Locator._all:
            if entity == other:
                continue
            if other.hitbox is None:
                continue
            if entity.hitbox.colliderect(other.hitbox):
                collisions.append(other)
        return collisions