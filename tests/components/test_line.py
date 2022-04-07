from cfi.components.line import Line
from cfi.components.literalfield import LiteralField


def test_line_read_no_fields():
    line = Line([])
    fileline = ""
    assert len(line.read(fileline)) == 0


def test_line_read_with_fields():
    fields = [LiteralField(6, 0), LiteralField(6, 7)]
    line = Line(fields)
    fileline = "hello, world!"
    values = line.read(fileline)
    assert values[0] == "hello,"
    assert values[1] == "world!"


def test_line_write_no_fields():
    line = Line([])
    fileline = ""
    assert len(line.write(fileline)) == 0


def test_line_write_with_fields():
    fields = [LiteralField(6, 0), LiteralField(6, 7)]
    values = ["hello,", "world!"]
    line = Line(fields, values)
    fileline = "hello, world!"
    outline = line.write(fileline)
    assert fileline == outline