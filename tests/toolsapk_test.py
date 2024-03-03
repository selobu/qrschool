from app.toolsapk import (
    Tb,
    TbContainer,
    map_name_to_table,
    Base,
    uuidgenerator,
    gethash,
    shell_decorated,
    map_name_to_shell,
    import_submodules,
)
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
import re
from pathlib import Path


def test_table_container():
    assert isinstance(Tb, TbContainer)


def test_map_name_to_table():
    @map_name_to_table
    class TableTest(Base):
        __tablename__ = "tabletest"
        id: Mapped[Optional[int]] = mapped_column(
            primary_key=True, nullable=False, autoincrement=True
        )

    assert hasattr(Tb, "TableTest")


def test_uuid_generator():
    uuid = uuidgenerator()
    assert (
        len(
            re.findall(
                r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
                uuid,
            )
        )
    ) == 1


def test_gethash():
    assert (
        gethash("hello worlds how are you")
    ) == "e19b1768182908dc491714b9511646eacc7901157ee0b0233a0733555ff91bc3"


def test_map_name_to_shell():
    @map_name_to_shell
    def test_func():
        return

    assert test_func.__name__ in shell_decorated


def test_import_submodules():
    path_to_seach = Path(__package__).parent.joinpath("module_test").absolute()
    modules = import_submodules(path_to_seach)
    assert "file_test" in modules
