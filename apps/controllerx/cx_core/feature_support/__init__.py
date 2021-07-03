from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from cx_core.type_controller import TypeController


class FeatureSupport:

    controller: "TypeController"
    update_supported_features: bool
    _supported_features: Optional[int]

    def __init__(
        self,
        controller: "TypeController",
        supported_features: Optional[int] = None,
        update_supported_features=False,
    ) -> None:
        self.controller = controller
        self._supported_features = supported_features
        self.update_supported_features = update_supported_features

    @property
    async def supported_features(self) -> int:
        if self._supported_features is None or self.update_supported_features:
            bitfield: str = await self.controller.get_entity_state(
                attribute="supported_features"
            )
            if bitfield is not None:
                self._supported_features = int(bitfield)
            else:
                raise ValueError(
                    f"`supported_features` could not be read from `{self.controller.entity}`. Entity might not be available."
                )
        return self._supported_features

    async def is_supported(self, feature: int) -> bool:
        return feature & await self.supported_features != 0

    async def not_supported(self, feature: int) -> bool:
        return not await self.is_supported(feature)
