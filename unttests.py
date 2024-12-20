import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import tkinter as tk
from emulator import ShellEmulator
import random
class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.emulator = ShellEmulator(self.root, "virtual_fs.tar")

    @patch('os.listdir', return_value=['file1.txt', 'file2.txt'])
    def test_list_files(self, mock_listdir):
        self.emulator.list_files()
        self.assertIn("file1.txt", self.emulator.text_area.get("1.0", tk.END))
        self.assertIn("file2.txt", self.emulator.text_area.get("1.0", tk.END))

    @patch('os.path.isdir', return_value=True)
    def test_change_directory(self, mock_isdir):
        self.emulator.change_directory("subdir")
        self.assertEqual(self.emulator.current_path, "/subdir")

    @patch('os.path.isdir', return_value=False)
    def test_change_directory_not_found(self, mock_isdir):
        self.emulator.change_directory("nonexistent")
        self.assertIn("Директория не найдена", self.emulator.text_area.get("1.0", tk.END))

    def test_print_working_directory(self):
        self.emulator.print_working_directory()
        self.assertIn(f"{self.emulator.username}:/", self.emulator.text_area.get("1.0", tk.END))

    @patch('builtins.open', new_callable=mock_open, read_data="file content")
    def test_cat_file(self, mock_file):
        self.emulator.cat_file("file1.txt")
        self.assertIn("file content", self.emulator.text_area.get("1.0", tk.END))

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_cat_file_not_found(self, mock_file):
        self.emulator.cat_file("nonexistent.txt")
        self.assertIn("Файл не найден", self.emulator.text_area.get("1.0", tk.END))

    @patch('os.makedirs')
    def test_make_directory(self, mock_makedirs):
        dirname = "test_dir"
        self.emulator.make_directory(dirname)
        mock_makedirs.assert_called_once_with(os.path.join(f"virtual_fs{self.emulator.current_path}", dirname.strip()))

    @patch('os.remove')
    def test_remove_file(self, mock_remove):
        filename = "test_file.txt"
        
        # Создаем файл для удаления
        with open(os.path.join(f"virtual_fs{self.emulator.current_path}", filename), 'w') as f:
            f.write("Hello World")
        
        # Удаляем файл
        self.emulator.remove_file(filename)
        mock_remove.assert_called_once_with(os.path.join(f"virtual_fs{self.emulator.current_path}", filename.strip()))

    @patch('shutil.rmtree')
    def test_remove_directory(self, mock_rmtree):
        dirname = "test_dir".join(str(random.randint(1,100)))
        
        # Создаем директорию для удаления
        os.makedirs(os.path.join(f"virtual_fs{self.emulator.current_path}", dirname))
        
        # Удаляем директорию
        self.emulator.remove_file(dirname)
        mock_rmtree.assert_called_once_with(os.path.join(f"virtual_fs{self.emulator.current_path}", dirname.strip()))

    def test_show_history(self):
        self.emulator.history = ["ls", "pwd", "cd subdir"]
        self.emulator.show_history()
        history_output = "\n".join(self.emulator.history) + "\n"
        self.assertIn(history_output, self.emulator.text_area.get("1.0", tk.END))

    @patch('builtins.open', new_callable=mock_open)
    def test_change_owner(self, mock_file):
        # Проверка изменения владельца файла
        filename = "test_file.txt"
        
        # Создаем файл для изменения владельца
        with open(os.path.join(f"virtual_fs{self.emulator.current_path}", filename), 'w') as f:
            f.write("Hello World")

        user = "new_user"
        
        # Выполняем команду chown
        self.emulator.change_owner(f"{filename} {user}")
        
        expected_message = f"Владелец файла '{filename}' изменен на пользователя '{user}'.\n"
        
        # Проверяем вывод сообщения
        self.assertIn(expected_message, self.emulator.text_area.get("1.0", tk.END))

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()
