import abc
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from cx_core.controller import Controller
from cx_core.feature_support import FeatureSupport

EntityType = TypeVar("EntityType", bound="Entity")


class Entity:
    name: str
    entities: List[str]

    def __init__(
        self, name: str, entities: Optional[List[str]] = None, **kwargs: Dict[str, Any]
    ) -> None:
        self.name = name
        self.set_entities(entities)

    @property
    def main(self) -> str:
        return self.entities[0]

    @property
    def is_group(self) -> bool:
        return self.entities[0] != self.name

    def set_entities(self, value: Optional[List[str]] = None) -> None:
        self.entities = value if value is not None else [self.name]

    @classmethod
    def instantiate(
        cls: Type[EntityType], name: str, entities: Optional[List[str]] = None, **params
    ) -> EntityType:
        return cls(name=name, entities=entities, **params)

    def __str__(self) -> str:
        return self.name if not self.is_group else f"{self.name}({self.entities})"


class TypeController(Controller, abc.ABC, Generic[EntityType]):

    domains: List[str]
    entity_arg: str
    entity: EntityType
    update_supported_features: bool
    feature_support: FeatureSupport

    async def init(self) -> None:
        if self.entity_arg not in self.args:
            raise ValueError(
                f"{self.__class__.__name__} class needs the `{self.entity_arg}` attribute"
            )
        self.entity = await self._get_entity(self.args[self.entity_arg])  # type: ignore
        self._check_domain(self.entity)
        self.update_supported_features = self.args.get(
            "update_supported_features", False
        )
        supported_features: Optional[int] = self.args.get("supported_features")
        self.feature_support = FeatureSupport(
            self, supported_features, self.update_supported_features
        )
        await super().init()

    @abc.abstractmethod
    def _get_entity_type(self) -> Type[Entity]:
        raise NotImplementedError

    async def _get_entities(self, entity_name: str) -> Optional[List[str]]:
        entities: Optional[Union[str, List[str]]] = await self.get_state(
            entity_name, attribute="entity_id"
        )
        self.log(
            f"Entities from `{entity_name}` (entity_id attribute): `{entities}`",
            level="DEBUG",
        )
        # If the entity groups other entities, this attribute will be a list
        if not isinstance(entities, (list, tuple)):
            return None
        if entities is not None and len(entities) == 0:
            raise ValueError(f"`{entity_name}` does not have any entities registered.")
        return entities

    async def _get_entity(self, entity: Union[str, dict]) -> Entity:
        entity_args: Dict
        entity_name: str
        if isinstance(entity, str):
            entity_name = entity
            entity_args = {}
        elif isinstance(entity, dict):
            entity_name = entity["name"]
            entity_args = {key: value for key, value in entity.items() if key != "name"}
        else:
            raise ValueError(
                f"Type {type(entity)} is not supported for `{self.entity_arg}` attribute"
            )
        entities = await self._get_entities(entity_name)
        return self._get_entity_type().instantiate(
            name=entity_name, entities=entities, **entity_args
        )

    def _check_domain(self, entity: Entity) -> None:
        if self.contains_templating(entity.name):
            return
        same_domain = all(
            (
                any(elem.startswith(domain + ".") for domain in self.domains)
                for elem in entity.entities
            )
        )
        if not same_domain:
            if entity.is_group:
                error_msg = (
                    f"All the subentities from {entity} must be from one "
                    f"of the following domains {self.domains} (e.g. {self.domains[0]}.bedroom)"
                )
            else:
                error_msg = (
                    f"'{entity}' must be from one "
                    f"of the following domains {self.domains} (e.g. {self.domains[0]}.bedroom)"
                )
            raise ValueError(error_msg)

    async def get_entity_state(self, attribute: Optional[str] = None) -> Any:
        entity = self.entity.main
        if self.update_supported_features:
            entities = await self._get_entities(self.entity.name)
            self.entity.set_entities(entities)
            entity = self.entity.entities[0]
        out = await self.get_state(entity, attribute=attribute)
        return out
