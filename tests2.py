import unittest
from unittest.mock import patch, MagicMock
import subprocess
from PIL import Image
import io
import os
from visualizer import load_config, get_commits_for_file, build_dependency_graph, show_graph

class TestVisualizer(unittest.TestCase):

    @patch("builtins.open", create=True)
    def test_load_config_success(self, mock_open):
        """Тестируем успешную загрузку конфигурации."""
        mock_open.return_value.__enter__.return_value.read.return_value = """
        graphviz_path: 'C:/Program Files/Graphviz/bin/dot.exe'
        repository_path: 'C:/Users/User/PycharmProjects/PythonProject1/repo'
        file_name: "test.txt"
"""
        config = load_config("config.yaml")
        self.assertEqual(config["graphviz_path"], 'C:/Program Files/Graphviz/bin/dot.exe')
        self.assertEqual(config["repository_path"], "C:/Users/User/PycharmProjects/PythonProject1/repo")
        self.assertEqual(config["file_name"], "test.txt")

    @patch("builtins.open", create=True)
    def test_load_config_failure(self, mock_open):
        """Тестируем ошибку при загрузке конфигурации (если файл не существует)."""
        mock_open.side_effect = FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            load_config("non_existent.yaml")

    @patch("subprocess.run")
    def test_get_commits_for_file_success(self, mock_run):
        """Тестируем успешное получение коммитов для файла."""
        mock_run.return_value = MagicMock(returncode=0, stdout="commit1\ncommit2\ncommit3\n")
        commits = get_commits_for_file("C:/Users/User/PycharmProjects/PythonProject1/repo", "test.txt")
        self.assertEqual(commits, ["commit1", "commit2", "commit3"])

    @patch("subprocess.run")
    def test_get_commits_for_file_failure(self, mock_run):
        """Тестируем ошибку при получении коммитов для файла."""
        mock_run.return_value = MagicMock(returncode=1, stderr="Error")
        with self.assertRaises(Exception):
            get_commits_for_file("C:/Users/User/PycharmProjects/PythonProject1/repo", "test.txt")

    def test_build_dependency_graph(self):
        """Тестируем создание графа зависимостей из списка коммитов."""
        commits = ["commit1", "commit2", "commit3"]
        graph = build_dependency_graph(commits)
        self.assertEqual(len(graph.body), 5)  # 3 коммита + 2 рёбер (для связи)
        self.assertIn("commit1", graph.body[0])  # Проверяем наличие коммитов в графе
        self.assertIn("commit2", graph.body[0])
        self.assertIn("commit3", graph.body[0])

    @patch("PIL.Image.open")
    @patch("graphviz.backend.execute")
    def test_show_graph(self, mock_execute, mock_image_open):
        """Тестируем функцию отображения графа."""
        mock_execute.return_value = b"graph_image_data"
        mock_image_open.return_value = MagicMock(spec=Image)
        graph = MagicMock()
        graph.pipe.return_value = b"graph_image_data"
        show_graph(graph)
        mock_image_open.assert_called_once_with(io.BytesIO(b"graph_image_data"))

    @patch("PIL.Image.open")
    def test_show_graph_failure(self, mock_image_open):
        """Тестируем ошибку при отображении графа (если изображение не может быть открыто)."""
        graph = MagicMock()
        graph.pipe.return_value = b"graph_image_data"
        mock_image_open.side_effect = IOError("Cannot open image")
        with self.assertRaises(IOError):
            show_graph(graph)


if __name__ == "__main__":
    unittest.main()
