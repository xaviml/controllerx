import abc
from typing import Any, Generic, List, Optional, Type, TypeVar, Union

from cx_core.controller import Controller
from cx_core.feature_support import FeatureSupport

EntityType = TypeVar("EntityType", bound="Entity")


class Entity:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    @classmethod
    def instantiate(cls: Type[EntityType], **params) -> EntityType:
        return cls(**params)


class TypeController(Controller, abc.ABC, Generic[EntityType]):

    domains: List[str]
    entity_arg: str
    entity: EntityType
    feature_support: FeatureSupport

    async def init(self) -> None:
        if self.entity_arg not in self.args:
            raise ValueError(
                f"{self.__class__.__name__} class needs the `{self.entity_arg}` attribute"
            )
        self.entity = self.get_entity(self.args[self.entity_arg])  # type: ignore
        await self.check_domain(self.entity.name)
        update_supported_features = self.args.get("update_supported_features", False)
        self.feature_support = FeatureSupport(
            self.entity.name, self, update_supported_features
        )
        await super().init()

    @abc.abstractmethod
    def _get_entity_type(self) -> Type[Entity]:
        raise NotImplementedError

    def get_entity(self, entity: Union[str, dict]) -> Entity:
        if isinstance(entity, str):
            return self._get_entity_type().instantiate(name=entity)
        elif isinstance(entity, dict):
            return self._get_entity_type().instantiate(**entity)
        else:
            raise ValueError(
                f"Type {type(entity)} is not supported for `{self.entity_arg}` attribute"
            )

    async def check_domain(self, entity_name: str) -> None:
        if entity_name.startswith("group."):
            entities = await self.get_state(entity_name, attribute="entity_id")  # type: ignore
            same_domain = all(
                (
                    any(elem.startswith(domain + ".") for domain in self.domains)
                    for elem in entities
                )
            )
            if not same_domain:
                raise ValueError(
                    f"All entities from '{entity_name}' must be from one "
                    f"of the following domains {self.domains} (e.g. {self.domains[0]}.bedroom)"
                )
        elif not any(entity_name.startswith(domain + ".") for domain in self.domains):
            raise ValueError(
                f"'{entity_name}' must be from one of the following domains "
                f"{self.domains} (e.g. {self.domains[0]}.bedroom)"
            )

    async def get_entity_state(
        self, entity: str, attribute: Optional[str] = None
    ) -> Any:
        if entity.startswith("group."):
            entities = await self.get_state(entity, attribute="entity_id")  # type: ignore
            if len(entities) == 0:
                raise ValueError(
                    f"The group `{entity}` does not have any entities registered."
                )
            entity = entities[0]
        out = await self.get_state(entity, attribute=attribute)  # type: ignore
        return out
