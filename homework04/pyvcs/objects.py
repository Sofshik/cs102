import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref  # type: ignore
from pyvcs.repo import repo_find  # type: ignore


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    objects = "objects"
    sha = hashlib.sha1((fmt + " " + str(len(data))).encode() + b"\00" + data).hexdigest()
    if write:
        gitdir = repo_find()
        if not (gitdir / objects / sha[:2]).exists():
            (gitdir / objects / sha[:2]).mkdir()
        with (gitdir / objects / sha[:2] / sha[2:]).open("wb") as file:
            file.write(zlib.compress((fmt + " " + str(len(data))).encode() + b"\00" + data))
    return sha


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    objects = "objects"
    if not 4 < len(obj_name) < 40:
        raise Exception(f"Not a valid object name {obj_name}")
    gitdir = repo_find()
    obj_list = []
    for dir in (gitdir / objects).glob("*"):
        if not dir.is_dir():
            continue
        for file in dir.glob("*"):
            cur_obj_name = file.parent.name + file.name
            if obj_name == cur_obj_name[: len(obj_name)]:
                obj_list.append(cur_obj_name)
    if not obj_list:
        raise Exception(f"Not a valid object name {obj_name}")
    return obj_list


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    dir_name = obj_name[:2]
    file_name = obj_name[:2]
    path = str(gitdir) + "/" + dir_name + "/" + file_name
    return path


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    objects = "objects"
    with (gitdir / objects / sha[:2] / sha[2:]).open("rb") as f:
        data = f.read()
    uncompressed = zlib.decompress(data)
    return (
        uncompressed.split(b"\00")[0].split(b" ")[0].decode(),
        uncompressed.split(b"\00", maxsplit=1)[1],
    )


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    tree = []
    while data:
        firstly = data.index(b"\00")
        mode, name = map(lambda x: x.decode(), data[:firstly].split(b" "))
        sha = data[firstly + 1 : firstly + 21]
        tree.append((int(mode), name, sha.hex()))
        data = data[firstly + 21 :]
    return tree


def cat_file(obj_name: str, pretty: bool = True) -> None:
    gitdir = repo_find()
    fmt, file_content = read_object(obj_name, gitdir)
    if fmt == "blob" or fmt == "commit":
        print(file_content.decode())
    else:
        for tree in read_tree(file_content):
            if tree[0] == 40000:
                print(f"{tree[0]:06}", "tree", tree[2] + "\t" + tree[1])
            else:
                print(f"{tree[0]:06}", "blob", tree[2] + "\t" + tree[1])


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    objects = {tree_sha}
    for mode, path, sha in read_tree(tree_sha):
        if stat.S_ISDIR(mode):
            objects.update(find_tree_files(sha, path))
        else:
            objects.add(sha)
    return objects


def commit_parse(raw: bytes, start: int = 0, dct=None):
    ret_val: tp.Dict[str, tp.Any]
    ret_val = {"message": []}
    for m in raw.decode().split("\n"):
        if m.startswith(("tree", "parent", "author", "committer")):
            name, val = m.split(" ", maxsplit=1)
            ret_val[name] = val
        else:
            ret_val["message"].append(m)
    return ret_val
