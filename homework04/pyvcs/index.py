import hashlib
import operator
import os
import pathlib
import struct 
import typing as tp 

from pyvcs.objects import hash_object # type: ignore


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        return struct.pack(
            ">10I20sh" + str(len(self.name)) + "s" + str(8 - (62 + len(self.name)) % 8) + "x",
            self.ctime_s,
            self.ctime_n,
            self.mtime_s,
            self.mtime_n,
            self.dev,
            self.ino,
            self.mode,
            self.uid,
            self.gid,
            self.size,
            self.sha1,
            self.flags,
            self.name.encode(),
        )

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        index_unpacked_content = struct.unpack(">10I20sh" + str(len(data) - 62) + "s", data)
        return GitIndexEntry(
            *(
                list(index_unpacked_content[:-1])
                + [index_unpacked_content[-1].rstrip(b"\00").decode()]
            )
        )


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    index = "index"
    if not (gitdir / index).exists():
        return []
    with (gitdir / index).open("rb") as file:
        header = file.read(12)
        cont = file.read()
    result = []
    cont_copy = cont
    last_pos = 0
    for m in range(struct.unpack(">I", header[8:])[0]):
        last_pos = len(cont_copy) - 1
        for n in range(63, len(cont_copy), 8):
            if cont_copy[n] == 0:
                last_pos = n
                break
        result += [GitIndexEntry.unpack(cont_copy[: last_pos + 1])]
        if len(cont_copy) != last_pos - 1:
            cont_copy = cont_copy[last_pos + 1 :]
    return result


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    index = "index"
    with (gitdir / index).open("wb") as file:
        inf = b"DIRC\00\00\00\02"
        file.write(b"DIRC\00\00\00\02")
        inf += struct.pack(">I", len(entries))
        file.write(struct.pack(">I", len(entries)))
        for enrty in entries:
            inf += enrty.pack()
            file.write(enrty.pack())
        file.write(hashlib.sha1(inf).digest())


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    entries = read_index(gitdir)
    if details:
        for entry in entries:
            print(f"{entry.mode:o} {entry.sha1.hex()} 0\t{entry.name}")
    else:
        for entry in entries:
            print(entry.name)


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    entries = {entry.name: entry for entry in read_index(gitdir)}
    for path in paths:
        if str(path) in entries:
            del entries[str(path)]
        with path.open("rb") as f:
            data = f.read()
        stat = os.stat(path)
        sha1 = hash_object(data, "blob", write=True)
        entries.update(
            {
                str(path): GitIndexEntry(
                    ctime_s=int(stat.st_ctime),
                    ctime_n=stat.st_ctime_ns % len(str(int(stat.st_ctime))),
                    mtime_s=int(stat.st_mtime),
                    mtime_n=stat.st_mtime_ns % len(str(int(stat.st_mtime))),
                    dev=stat.st_dev,
                    ino=stat.st_ino,
                    mode=stat.st_mode,
                    uid=stat.st_uid,
                    gid=stat.st_gid,
                    size=stat.st_size,
                    sha1=bytes.fromhex(sha1),
                    flags=7,
                    name=str(path),
                )
            }
        )
    if write:
        entries_list = []
        for name in sorted(entries.keys()):
            entries_list.append(entries[name])
        write_index(gitdir, entries_list)
