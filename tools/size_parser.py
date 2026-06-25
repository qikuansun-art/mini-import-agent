import re


class SizeParser:
    _SEPARATOR_PATTERN = re.compile(r"[xX*脳]")

    def parse_size(self, value: str) -> dict:
        if not isinstance(value, str):
            return {}

        parts = self._SEPARATOR_PATTERN.split(value.strip())
        if len(parts) != 3:
            return {}

        try:
            length, width, thickness = [int(part.strip()) for part in parts]
        except ValueError:
            return {}

        return {
            "length": length,
            "width": width,
            "thickness": thickness,
        }
