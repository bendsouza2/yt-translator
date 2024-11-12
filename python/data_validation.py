from typing import Literal

from pydantic import BaseModel


class WordEffects:
    styles: Literal["bounce", "fade"]
