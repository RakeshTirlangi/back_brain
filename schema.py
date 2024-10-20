from pydantic import BaseModel

class ImageInfo(BaseModel):
    image: str
    dict_of_vars: dict

    