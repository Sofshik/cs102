import datetime
import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index  # type: ignore
from pyvcs.objects import hash_object  # type: ignore
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref  # type: ignore


def write_tree(
    gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = ""
) -> str:
    files_list = [x.absolute() for x in (gitdir.parent / dirname).glob("*")]
    to_add_dirs: tp.Dict[str, tp.List[GitIndexEntry]]
    to_add_dirs = dict()
    enties_to_format = []
    for entry in index:
        if pathlib.Path(entry.name).absolute() in files_list:
            enties_to_format.append(entry)
        else:
            subdir_name = entry.name.lstrip(dirname).split("/", 1)[0]
            if subdir_name not in to_add_dirs:
                to_add_dirs[subdir_name] = []
            to_add_dirs[subdir_name].append(entry)
    for subdir_name in to_add_dirs:
        st = (pathlib.Path(gitdir.parent) / dirname / subdir_name).stat()
        sha = write_tree(gitdir, to_add_dirs[subdir_name], dirname + "/" + subdir_name)
        enties_to_format.append(
            GitIndexEntry(
                ctime_s=int(st.st_ctime),
                ctime_n=st.st_ctime_ns % len(str(int(st.st_ctime))),
                mtime_s=int(st.st_mtime),
                mtime_n=st.st_mtime_ns % len(str(int(st.st_mtime))),
                dev=st.st_dev,
                ino=st.st_ino,
                mode=0o40000,
                uid=st.st_uid,
                gid=st.st_gid,
                size=st.st_size,
                sha1=bytes.fromhex(sha),
                flags=7,
                name=str(pathlib.Path(gitdir.parent) / dirname / subdir_name),
            )
        )
    preformatted_data = b"".join(
        oct(entry.mode)[2:].encode()
        + b" "
        + pathlib.Path(entry.name).name.encode()
        + b"\00"
        + entry.sha1
        for entry in sorted(enties_to_format, key=lambda x: x.name)
    )
    return hash_object(preformatted_data, "tree", write=True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
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
