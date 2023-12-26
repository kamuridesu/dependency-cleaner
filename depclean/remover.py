import os
import shutil

from .progress import Progress, IndefiniteLoadingBar

def sizeof_fmt(num: int, suffix="B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


class Remover:
    def __init__(self, root_path: str = ".", auto_prune: bool = False):
        self.auto_prune = auto_prune
        self.root_path = root_path
        self.paths = []

    def map_all_paths(self):
        bar = IndefiniteLoadingBar()
        bar.start()
        for path in os.walk(self.root_path):
            path = path[0]
            if ("venv" in path or "node_modules" in path) and os.path.isdir(path):
                self.paths.append(path)
        bar.end()
        if self.auto_prune:
            self.remove()

    def remove(self):
        sizes = []
        if not self.paths: return
        progress = Progress()
        bar = IndefiniteLoadingBar()
        bar.start()
        for folder in self.paths:
            sizes.append(self.get_size(folder))
        bar.end()
        size = sizeof_fmt(sum(sizes))
        if not self.auto_prune:
            input(f"Are you sure you want to remove ALL the dependencies folder? {size} will be freed. Press ENTER to continue or CTRL+C to stop.")
        progress.start("Deleting files")
        for idx, folder in enumerate(self.paths):
            progress.progress(len(self.paths), idx + 1)
            shutil.rmtree(folder, True)
        progress.end()
        print(f"Freed: {size}")

    def get_size(self, start_path: str):
        total_size = 0
        for dirpath, _, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)

        return total_size