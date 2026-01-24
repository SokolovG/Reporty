from typing import Callable, Type, TypeVar

from adaptix.conversion import get_converter

SourceT = TypeVar("SourceT")
TargetT = TypeVar("TargetT")


class Converter:
    def __init__(self):
        self._converters: dict[tuple[Type, Type], Callable] = {}

    def convert(self, source_obj: SourceT, target_type: Type[TargetT]) -> TargetT:
        source_type = type(source_obj)
        cache_key = (source_type, target_type)

        if cache_key not in self._converters:
            try:
                self._converters[cache_key] = get_converter(source_type, target_type)
            except Exception as e:
                raise ValueError(
                    f"Cannot create converter from {source_type.__name__} "
                    f"to {target_type.__name__}: {e}"
                ) from e

        converter_func = self._converters[cache_key]
        try:
            return converter_func(source_obj)
        except Exception as e:
            raise ValueError(
                f"Conversion failed from {source_type.__name__} to {target_type.__name__}: {e}"
            ) from e

    def convert_list(self, source_list: list[SourceT], target_type: Type[TargetT]) -> list[TargetT]:
        return [self.convert(item, target_type) for item in source_list]
