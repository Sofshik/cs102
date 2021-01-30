def read_tasks(tasktxt: str = "/home/sofia/cs102/exam-winter-42/tasks.txt"):
    tasks = []
    with open(tasktxt, "r", encoding="utf-8") as f:
        data = f.read()
        lines = (a for a in data.split('\n') if a)
        current = 0
        for line in lines:
            if 'task' in line:
                task_count = int(line[4:]) - 1
                tasks.insert(task_count, [])
                current = tasks[task_count]
            else:
                node = line.split(' -> ')
                current.append(tuple(node))
    return tasks


def count_els(graph):
    els = [[el for el in line] for line in graph]
    unq = set([m for n in els for m in n])
    return len(unq)


def find_bug(graph):
    unq = count_els(graph)
    print(f"unique: {unq}, len(graph): {len(graph)}")

    els = {}
    broken = 0

    for link in graph:
        if link[0] == link[1]:
            broken += 1
        for el in link:
            if not el in els.keys():
                els[el] = 0
            els[el] += 1

    for i, count in enumerate(els.values()):
        if i == 0:
            continue
        if count > 2:
            broken += 1

    return broken


def main():
    tasks = read_tasks()
    print(tasks)
    broken = find_bug(tasks[2])
    print(broken)

main()