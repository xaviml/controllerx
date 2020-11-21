from typing import TYPE_CHECKING, List, Optional, Set, Type, TypeVar

if TYPE_CHECKING:
    from cx_core.type_controller import TypeController

Features = List[int]
SupportedFeatures = Set[int]
FeatureSupportType = TypeVar("FeatureSupportType", bound="FeatureSupport")


class FeatureSupport:

    entity_id: str
    controller: "TypeController"
    features: Features = []
    update_supported_features: bool
    _supported_features: Optional[SupportedFeatures]

    @staticmethod
    def encode(supported_features: SupportedFeatures) -> int:
        number = 0
        for supported_feature in supported_features:
            number |= supported_feature
        return number

    @staticmethod
    def decode(number: int, features: Features) -> SupportedFeatures:
        return {number & feature for feature in features if number & feature != 0}

    def __init__(
        self,
        entity_id: str,
        controller: "TypeController",
        update_supported_features=False,
    ) -> None:
        self.entity_id = entity_id
        self.controller = controller
        self._supported_features = None
        self.update_supported_features = update_supported_features

    @classmethod
    def instantiate(
        cls: Type[FeatureSupportType],
        entity_id: str,
        controller: "TypeController",
        update_supported_features=False,
    ) -> FeatureSupportType:
        return cls(entity_id, controller, update_supported_features)

    @property
    async def supported_features(self) -> SupportedFeatures:
        if self._supported_features is None or self.update_supported_features:
            bitfield: str = await self.controller.get_entity_state(
                self.entity_id, attribute="supported_features"
            )
            if bitfield is not None:
                self._supported_features = FeatureSupport.decode(
                    int(bitfield), self.features
                )
            else:
                raise ValueError(
                    f"`supported_features` could not be read from `{self.entity_id}`. Entity might not be available."
                )
        return self._supported_features

    async def is_supported(self, feature: int) -> bool:
        return feature in await self.supported_features

    async def not_supported(self, feature: int) -> bool:
        return feature not in await self.supported_features
