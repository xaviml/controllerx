from typing import List, Optional, Set, Union

from cx_core.controller import Controller

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
        entity: Optional[str],
        controller: Optional[Controller],
        features: Features,
    ) -> None:
        self.entity = entity
        self.controller = controller
        self._supported_features = None
        self.features = features

    async def supported_features(self):
        if self._supported_features is None:
            bitfield = await self.controller.get_entity_state(
                self.entity, attribute="supported_features"
            )
            if bitfield is not None:
                bitfield = int(bitfield)
                self._supported_features = FeatureSupport.decode(
                    bitfield, self.features
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
