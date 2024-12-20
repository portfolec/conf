import tkinter as tk
from tkinter import scrolledtext, messagebox
import os
import tarfile
import sys
import argparse
import shutil

class ShellEmulator:
    def __init__(self, master, virtual_fs_path):
        self.master = master
        self.master.title("Shell Emulator")
        self.current_path = "/"
        self.history = []

        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD)
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.username = os.getlogin()  
        self.virtual_fs_path = virtual_fs_path

        self.label = tk.Label(master, text=f"{self.username}")
        self.label.pack(padx=10, pady=5)

        self.entry = tk.Entry(master)
        self.entry.pack(padx=10, pady=10, fill=tk.X)
        self.entry.bind("<Return>", self.execute_command)

        self.extract_virtual_fs()

    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(description='Запуск эмулятора командной строки vshell.')
        parser.add_argument('--script', type=str, help='Имя файла со скриптом команд.')
        parser.add_argument('virtual_fs', type=str, help='Путь к образу файловой системы (tar).')
        
        args = parser.parse_args()
        
        if not os.path.exists(args.virtual_fs):
            parser.error(f"Файл виртуальной файловой системы '{args.virtual_fs}' не найден.")
        
        return args

    def extract_virtual_fs(self):
        if not os.path.exists(self.virtual_fs_path):
            messagebox.showerror("Ошибка", "Файл виртуальной файловой системы не найден.")
            return

        with tarfile.open(self.virtual_fs_path) as tar:
            tar.extractall(path="virtual_fs")

    def load_script(self, script_file):
        try:
            with open(script_file, 'r') as file:
                for line in file:
                    command = line.strip()
                    if command:  
                        self.execute_command_from_script(command)
        except FileNotFoundError:
            messagebox.showerror("Ошибка", f"Файл скрипта {script_file} не найден.")

    def execute_command(self, event):
        command = self.entry.get()
        self.history.append(command)

        command_dict = {
            "ls": self.list_files,
            "cd": lambda: self.change_directory(command[3:]),
            "pwd": self.print_working_directory,
            "cat": lambda: self.cat_file(command[4:]),
            "exit": self.master.quit,
            "history": self.show_history,
            "mkdir": lambda: self.make_directory(command[6:]),
            "rm": lambda: self.remove_file(command[3:]),
            "chown": lambda: self.change_owner(command[6:])
        }

        cmd_func = command_dict.get(command.split()[0], None)

        if cmd_func:
            cmd_func()
        else:
            self.text_area.insert(tk.END, f"{self.username}: команда не найдена\n")

        self.entry.delete(0, tk.END)

    def execute_command_from_script(self, command):
        command_dict = {
            "ls": self.list_files,
            "cd": lambda: self.change_directory(command[3:]),
            "pwd": self.print_working_directory,
            "cat": lambda: self.cat_file(command[4:]),
            "exit": self.master.quit,
            "history": self.show_history,
            "mkdir": lambda: self.make_directory(command[6:]),
            "rm": lambda: self.remove_file(command[3:]),
            "chown": lambda: self.change_owner(command[6:])
        }

        cmd_func = command_dict.get(command.split()[0], None)

        if cmd_func:
            cmd_func()
        else:
            self.text_area.insert(tk.END, f"{self.username}: команда не найдена\n")

    def list_files(self):
        try:
            files = os.listdir(f"virtual_fs{self.current_path}")
            output = "\n".join(files) if files else "Пустая директория\n"
            self.text_area.insert(tk.END, f"{output}\n")
        except FileNotFoundError:
            self.text_area.insert(tk.END, "Директория не найдена\n")

    def change_directory(self, path):
        if path == "..":
            if self.current_path != "/":
                parts = self.current_path.split("/")
                parts.pop()  
                self.current_path = "/".join(parts) or "/"
                return
        
        new_path = os.path.join(f"virtual_fs{self.current_path}", path)
        
        if os.path.isdir(new_path):
            self.current_path = new_path.replace("virtual_fs", "")
            return
        else:
            self.text_area.insert(tk.END, "Директория не найдена\n")

    def print_working_directory(self):
        current_dir = f"{self.username}:{self.current_path}\n"
        self.text_area.insert(tk.END, current_dir)

    def cat_file(self, filename):
        try:
            with open(os.path.join(f"virtual_fs{self.current_path}", filename), 'r') as file:
                content = file.read()
                self.text_area.insert(tk.END, f"{content}\n")
        except FileNotFoundError:
            self.text_area.insert(tk.END, "Файл не найден\n")
    
    def make_directory(self, dirname):
        try:
            new_dir_path = os.path.join(f"virtual_fs{self.current_path}", dirname.strip())
            os.makedirs(new_dir_path)
            self.text_area.insert(tk.END, f"Директория '{dirname}' создана.\n")
        except Exception as e:
            self.text_area.insert(tk.END, f"Ошибка при создании директории '{dirname}': {str(e)}\n")

    def remove_file(self, filename):
        try:
            file_path = os.path.join(f"virtual_fs{self.current_path}", filename.strip())
            if os.path.isfile(file_path):
                os.remove(file_path)
                self.text_area.insert(tk.END, f"Файл '{filename}' удален.\n")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                self.text_area.insert(tk.END, f"Директория '{filename}' удалена.\n")
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            self.text_area.insert(tk.END, "Файл или директория не найдены\n")
    
    def change_owner(self, filename_and_user):
        try:
            filename, user = filename_and_user.split()
            file_path = os.path.join(f"virtual_fs{self.current_path}", filename.strip())
            
            # Здесь просто выводим сообщение
            message = f"Владелец файла '{filename}' изменен на пользователя '{user}'.\n"
            
            # Выводим результат
            self.text_area.insert(tk.END, message)
            
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат команды. Используйте 'chown <файл> <пользователь>'.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


    # Выводим результат
        self.text_area.insert(tk.END, message)

    def show_history(self):
        history_output = "\n".join(self.history) or "История пуста\n"
        self.text_area.insert(tk.END, f"История команд:\n{history_output}\n")

if __name__ == "__main__":
    args = ShellEmulator.parse_arguments()
    root = tk.Tk()
    app = ShellEmulator(root, args.virtual_fs)
    
    if args.script:
        app.load_script(args.script)

    root.mainloop()
