from typing import List, Set, Union

from cx_core.controller import TypeController

SupportedFeatureNumber = Union[int, str]
Features = List[int]
SupportedFeatures = Set[int]


class FeatureSupport:
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
        entity: str,
        controller: TypeController,
        features: Features,
        update_supported_features: bool,
    ) -> None:
        self.entity = entity
        self.controller = controller
        self._supported_features = None
        self.features = features
        self.update_supported_features = update_supported_features

    async def supported_features(self):
        if self._supported_features is None or self.update_supported_features:
            bitfield: str = await self.controller.get_entity_state(
                self.entity, attribute="supported_features"
            )
            if bitfield is not None:
                self._supported_features = FeatureSupport.decode(
                    int(bitfield), self.features
                )
            else:
                raise ValueError(
                    f"`supported_features` could not be read from `{self.entity}`. Entity might not be available."
                )
        return self._supported_features

    async def is_supported(self, feature: int) -> bool:
        return feature in await self.supported_features()

    async def not_supported(self, feature: int) -> bool:
        return feature not in await self.supported_features()
