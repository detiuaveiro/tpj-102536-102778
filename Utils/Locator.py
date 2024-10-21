
class Locator:

    _map: dict[type, list[object]] = {}

    @staticmethod
    def add(interface: type, implementation: object) -> None:
        if interface not in Locator._map:
            Locator._map[interface] = []
        Locator._map[interface].append(implementation)


    @staticmethod
    def get(interface: type) -> list[object]:
        return Locator._map.get(interface, [])
    
    
    @staticmethod
    def get_all() -> list[object]:
        return list(Locator._map.values())