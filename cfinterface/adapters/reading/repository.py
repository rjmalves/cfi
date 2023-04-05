from typing import IO, BinaryIO, TextIO, Union, Type, Dict
from abc import ABC, abstractmethod
from io import BytesIO, StringIO


class Repository(ABC):
    def __init__(
        self, content: Union[str, bytes], wrap_io: bool = False, *args
    ) -> None:
        self._content = content
        self._wrap_io = wrap_io

    def __enter__(self) -> "Repository":
        return self

    def __exit__(self, *args):
        pass

    @abstractmethod
    def read(self, n: int) -> Union[str, bytes]:
        """
        Reads a line for extracting information following
        the given fields.

        :param n: The number of bytes to be read
        :type n: int
        :return: The extracted data
        :rtype: str | bytes
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def file(self) -> IO:
        raise NotImplementedError


class BinaryRepository(Repository):
    def __init__(
        self, content: Union[str, bytes], wrap_io: bool = False, *args
    ) -> None:
        super().__init__(content, wrap_io)
        self._filepointer: BinaryIO = None  # type: ignore

    def __enter__(self):
        io = BytesIO(self._content) if self._wrap_io else self._content
        self._filepointer = open(io, "rb")
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self._filepointer.close()

    def read(self, n: int) -> bytes:
        """
        Reads a line for extracting information following
        the given fields.

        :param n: The number of bytes to be read
        :type n: int
        :return: The extracted data
        :rtype: bytes
        """
        return self._filepointer.read(n)

    @property
    def file(self) -> BinaryIO:
        return self._filepointer


class TextualRepository(Repository):
    def __init__(
        self, content: str, encoding: str, wrap_io: bool = False
    ) -> None:
        super().__init__(content, wrap_io)
        self._encoding = encoding
        self._filepointer: TextIO = None  # type: ignore

    def __enter__(self):
        io = StringIO(self._content) if self._wrap_io else self._content
        self._filepointer = open(io, "r", encoding=self._encoding)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self._filepointer.close()

    def read(self, n: int) -> str:
        """
        Reads a line for extracting information following
        the given fields.

        :param n: The number of bytes to be read
        :type n: int
        :return: The extracted data
        :rtype: str
        """
        return self._filepointer.readline()

    @property
    def file(self) -> TextIO:
        return self._filepointer


def factory(kind: str) -> Type[Repository]:
    mappings: Dict[str, Type[Repository]] = {
        "TEXT": TextualRepository,
        "BINARY": BinaryRepository,
    }
    return mappings.get(kind, TextualRepository)
