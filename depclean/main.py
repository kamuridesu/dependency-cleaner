from .remover import Remover

def main():
    x = Remover()
    x.map_all_paths()
    for path in x.paths:
        print(path)
    x.remove()