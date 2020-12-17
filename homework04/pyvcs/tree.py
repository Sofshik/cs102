import datetime
import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index  # type: ignore
from pyvcs.objects import hash_object  # type: ignore
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref  # type: ignore


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    tree_ins = []
    for entry in index:
        _, title = os.path.split(entry.name)
        if dirname:
            titles = dirname.split("/")
        else:
            titles = entry.name.split("/")
        if len(titles) == 1:
            if dirname and entry.name.find(dirname) == -1:
                continue
            with open(entry.name, "rb") as file:
                info = file.read()
            mode = str(oct(entry.mode))[2:]
            tree_in = f"{mode} {title}\0".encode()
            tree_in += bytes.fromhex(hash_object(info, "blob", write=True))
            tree_ins.append(tree_in)
        else:
            prefix = titles[0]
            title = f"/".join(titles[1:])
            mode = "40000"
            tree_in = f"{mode} {prefix}\0".encode()
            tree_in += bytes.fromhex(write_tree(gitdir, index, title))
            tree_ins.append(tree_in)
    tree_binary = b"".join(tree_ins)
    return hash_object(tree_binary, "tree", write=True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    if "GIT_AUTHOR_NAME" in os.environ and "GIT_AUTHOR_EMAIL" in os.environ and author is None:
        author = author = f"{os.getenv('GIT_AUTHOR_NAME')} <{os.getenv('GIT_AUTHOR_EMAIL')}>"
    now = int(time.mktime(time.localtime()))
    timezone = time.timezone
    if timezone > 0:
        format_time = "-"
    else:
        format_time = "+"
    format_time += f"{abs(timezone) // 3600:02}{abs(timezone) // 60 % 60:02}"
    data_commit = []
    data_commit.append(f"tree {tree}")
    if parent is not None:
        data_commit.append(f"parent {parent}")
    data_commit.append(f"author {author} {now} {format_time}")
    data_commit.append(f"committer {author} {now} {format_time}")
    data_commit.append(f"\n{message}\n")
    data = "\n".join(data_commit).encode()
    return hash_object(data, "commit", write=True)
