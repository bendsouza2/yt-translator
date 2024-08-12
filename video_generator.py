from typing import List


class VideoGenerator:

    def __init__(self,
                 word: str,
                 sentences: List[str],
                 local_image_storage: bool = False,
                 image_path: str = None

                 ):
        self.word = word
        self.sentences = sentences
        self.local_image_storage = local_image_storage
        self.image_path = image_path

    @property
    def image_path(self):
        return self._image_path

    @image_path.setter
    def image_path(self, image_path: str):
        if image_path is not None:
            self._image_path = image_path
        elif self.local_image_storage is True and image_path is None:
            pass
        elif self.local_image_storage is False and image_path is None:
            pass

