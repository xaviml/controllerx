from typing import List, Set, Union

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

    def __init__(self, number: SupportedFeatureNumber, features: Features) -> None:
        parsed_number = int(number)
        self.supported_features = FeatureSupport.decode(parsed_number, features)

    def is_supported(self, feature: int) -> bool:
        return feature in self.supported_features

    def not_supported(self, feature: int) -> bool:
        return feature not in self.supported_features
