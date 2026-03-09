import os

def get_project_root() -> str:
    current_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_path)
    return os.path.dirname(current_dir)


def get_abs_path(relative_path: str) -> str:
    project_root = get_project_root()
    return os.path.join(project_root, relative_path)








if __name__ == "__main__":
    print(get_project_root())
    print(get_abs_path("data/sample.txt"))


