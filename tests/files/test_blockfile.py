from typing import IO, List

from cfi.components.block import Block
from cfi.components.defaultblock import DefaultBlock
from cfi.files.blockfile import BlockFile

from tests.mocks.mock_open import mock_open

from unittest.mock import MagicMock, patch


class DummyBlock(Block):
    BEGIN_PATTERN = "beg"
    END_PATTERN = "end"

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, self.__class__):
            return False
        else:
            return o.data == self.data

    def read(self, file: IO) -> bool:
        self.data: List[str] = []
        while True:
            line: str = file.readline()
            self.data.append(line)
            if self.ends(line):
                break
        return True

    def write(self, file: IO) -> bool:
        for line in self.data:
            file.write(line)
        return True


def test_blockfile_read():
    data = "Hello, world!"
    filedata = (
        "\n".join([DummyBlock.BEGIN_PATTERN, data, DummyBlock.END_PATTERN])
        + "\n"
    )
    f = BlockFile([DummyBlock])
    m: MagicMock = mock_open(read_data=filedata)
    with patch("builtins.open", m):
        f.read("", "")


def test_blockfile_write():
    data = "Hello, world!"
    filedata = (
        "\n".join([DummyBlock.BEGIN_PATTERN, data, DummyBlock.END_PATTERN])
        + "\n"
    )
    f = BlockFile([DummyBlock])
    m: MagicMock = mock_open(read_data=filedata)
    with patch("builtins.open", m):
        f.write("", "")
