from typing import Any
import msgspec
from litestar.dto import MsgspecDTO, DTOConfig


class SuccessResponse(msgspec.Struct):
    success: bool = True
    data: list | None = None
    message: str | None = None

class ErrorResponse(msgspec.Struct):
    error_code: str
    message: str
    success: bool = False
    details: Any | None = None



class SuccessResponseDTO(MsgspecDTO[SuccessResponse]):
    config = DTOConfig()
    
    def data_to_encodable_type(self, data: SuccessResponse) -> dict[str, Any]:
        raw_dict = msgspec.to_builtins(data)
        return self._apply_camel_case_recursive(raw_dict)
    
    def _apply_camel_case_recursive(self, obj: Any) -> Any:
        if isinstance(obj, dict):
            return {
                self._to_camel_case(key): self._apply_camel_case_recursive(value)
                for key, value in obj.items()
            }
        elif isinstance(obj, list):
            return [self._apply_camel_case_recursive(item) for item in obj]
        else:
            return obj
    
    def _to_camel_case(self, snake_str: str) -> str:
        if '_' not in snake_str:
            return snake_str
        components = snake_str.split('_')
        return components[0] + ''.join(word.capitalize() for word in components[1:])