import argparse
import yaml
import subprocess
from graphviz import Digraph
from PIL import Image
import io

def load_config(config_file):
    with open(config_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_commits_and_metadata(repo_path, file_name):
    command = ["git", "log", "--pretty=format:%H %P %ci", "--", file_name]
    result = subprocess.run(command, cwd=repo_path, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception("Ошибка при получении коммитов из репозитория")
    commit_metadata = []
    for line in result.stdout.splitlines():
        parts = line.split()
        commit = parts[0]
        parents = parts[1:-3]
        date = " ".join(parts[-3:])
        commit_metadata.append((commit, parents, date))
    return commit_metadata

def build_dependency_graph(commit_metadata):
    graph = Digraph(format='png')
    graph.attr(dpi='300', rankdir='TB')

    # Добавляем узлы и ребра
    for commit, parents, date in commit_metadata:
        label = f"{commit[:7]}\n{date}"
        graph.node(commit, label=label)
        for parent in parents:
            graph.edge(parent, commit)

    return graph

def show_graph(graph):
    output_file = graph.pipe(format='png')
    image = Image.open(io.BytesIO(output_file))
    image.show()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file")
    args = parser.parse_args()

    config = load_config(args.config_file)
    repo_path = config["repository_path"]
    file_name = config["file_name"]

    commit_metadata = get_commits_and_metadata(repo_path, file_name)
    graph = build_dependency_graph(commit_metadata)
    show_graph(graph)

if __name__ == "__main__":
    main()
