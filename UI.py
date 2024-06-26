import tkinter as tk
import asyncio
import traceback
import sys, os
from io import StringIO
from libraries.ai import ArtificialInteligence

class ConsoleWindow:
    def __init__(self, root):
        self.root = root
        self.create_widgets()
        self.root.title("[2501] // AiTerminal")
        self.text_to_display = ""
        self.index = 0
        self.commands = {
            "help": (self.display_help, "Displays available commands and their descriptions"),
            "ai": (self.ai_request, "Allows the user to send an AI request | Expect delays(lags) with response", "[prompt]"),
            "echo": (self.echo_text, "Prints text to the console", "[text]"),
            "cat": (self.display_file_content, "Displays the contents of a file", "[filename]"),
            "mkdir": (self.make_directory, "Creates a new directory", "[dirname]"),
            "rmdir": (self.remove_directory, "Removes an empty directory", "[dirname]"),
            "rm": (self.remove_file, "Removes a file", "[filename]"),
            "touch": (self.create_file, "Creates a new file", "[filename]"),
            "ls": (self.list_directory, "Lists files and directories in the current directory"),
            "cd": (self.change_directory, "Changes the current directory"),
            "python": (self.run_python_code, "Executes Python code/Compile Python files", "[code] or [-c file.py]"),
            "clear": (self.clear_console, "Clears the console (or use \"CTRL + X\" to clear)"),
            "exit": (self.exit_console, "Exits the console application"),
        }
        self.command_history = []
        self.history_index = -1

        
        self.display_welcome_message()

    def create_widgets(self):
        self.text_area = tk.Text(self.root, wrap="word", state="normal", height=25, width=120, bg="black", fg="white")
        self.text_area.pack(fill="both", expand=True)
        self.text_area.bind("<Key>", self.key_pressed)

        self.input_frame = tk.Frame(self.root, bg="black")
        self.input_frame.pack(fill="x")

        self.input_label = tk.Label(self.input_frame, text="Enter >", height=1, width=15, fg="white", bg="black")
        self.input_label.pack(side="left")

        self.input_entry = tk.Entry(self.input_frame, bg="black", fg="white", width=15, insertbackground="white")
        self.input_entry.pack(fill="x", expand=True)
        self.input_entry.focus_set()
        self.input_entry.bind("<Control-x>", self.clear_console)
        self.input_entry.bind("<Return>", self.execute_command)
        self.input_entry.bind("<Up>", self.history_up)
        self.input_entry.bind("<Down>", self.history_down)

    def write(self, msg):
        self.text_to_display += msg
        self.display_text()

    def display_welcome_message(self):
        self.print_to_console(f"""┌──────────────────┬────────────────────────────────────────────────────────────┐
│    AiTerminal                                                                 │
├──────────────────┴────────────────────────────────────────────────────────────┤
│                                                                               │
│                                                                               │
│              ░▒▓███████▓▒░░▒▓████████▓▒░▒▓████████▓▒░  ░▒▓█▓▒░                │
│                     ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓████▓▒░                │
│                     ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░                │
│               ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░                │
│              ░▒▓█▓▒░             ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░                │
│              ░▒▓█▓▒░             ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░                │
│              ░▒▓████████▓▒░▒▓███████▓▒░░▒▓████████▓▒░  ░▒▓█▓▒░                │
│                                                                               │
│                                                                               │
│  [•]   Welcome to the AiTerminal script!                                      │
│  [!]   Type "help" for more information...                                    │
│  [@]   You confirm that you have read and accept the MIT LICENSE.             │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘""")
        
    def display_text(self):
        self.text_area.configure(state="normal")
        if self.index < len(self.text_to_display):
            char = self.text_to_display[self.index]
            if self.text_to_display.startswith("[2501] >", self.index):
                delay = 0
                while self.index < len(self.text_to_display) and self.text_to_display[self.index] != "\n":
                    self.text_area.insert("end", self.text_to_display[self.index])
                    self.index += 1
            elif any(self.text_to_display.startswith(prefix, self.index) for prefix in ["┌", "│", "├", "└"]):
                delay = 0
                while self.index < len(self.text_to_display) and self.text_to_display[self.index] != "\n":
                    self.text_area.insert("end", self.text_to_display[self.index])
                    self.index += 1
            else:
                delay = 10
                self.text_area.insert("end", char)
                self.index += 1

            self.text_area.see("end")
            self.root.after(delay, self.display_text)

        self.text_area.configure(state="disabled")


    def print_to_console(self, message):
        self.write(message + "\n")

    def list_directory(self, path="."):
        try:
            files = os.listdir(path)
            return "\n".join(files) + "\n"
        except Exception as e:
            return f"Error: {str(e)}\n"

    def display_file_content(self, filename):
        try:
            with open(filename, "r") as file:
                content = file.read()
            return content + "\n"
        except Exception as e:
            return f"Error: {str(e)}\n"

    def echo_text(self, text):
        return f"{text}\n"

    def make_directory(self, dirname):
        try:
            os.mkdir(dirname)
            return ""
        except Exception as e:
            return f"Error: {str(e)}\n"

    def remove_directory(self, dirname):
        try:
            os.rmdir(dirname)
            return ""
        except Exception as e:
            return f"Error: {str(e)}\n"

    def remove_file(self, filename):
        try:
            os.remove(filename)
            return ""
        except Exception as e:
            return f"Error: {str(e)}\n"

    def create_file(self, filename):
        try:
            with open(filename, "w") as file:
                pass
            return ""
        except Exception as e:
            return f"Error: {str(e)}\n"


    def change_directory(self, path=None):
        try:
            if not path:
                return os.getcwd() + "\n"
            elif path == "..":
                os.chdir(os.path.dirname(os.getcwd()))
                return os.getcwd() + "\n"
            else:
                os.chdir(path)
                return os.getcwd() + "\n"
        except Exception as e:
            return f"Error: {str(e)}\n"

    def display_help(self):
        for command, (func, description, *args) in self.commands.items():
            args_str = ' '.join(args) if args else ''
            self.print_to_console(f"    {command} {args_str} :: {description}")
        return ""

    def run_python_code(self, code):
        try:
            if code.startswith("-c "):
                script_path = code[3:]
                with open(script_path, "r") as script_file:
                    script_content = script_file.read()
                stdout_backup = sys.stdout
                sys.stdout = StringIO()
                exec(script_content)
                result = sys.stdout.getvalue()
                return result
            else:
                stdout_backup = sys.stdout
                sys.stdout = StringIO()
                exec(code)
                result = sys.stdout.getvalue()
                return result
            return ""
        except Exception as e:
            return traceback.format_exc()
        finally:
            sys.stdout = stdout_backup

    def clear_console(self, event=None):
        self.text_area.configure(state="normal")
        self.text_area.delete(1.0, "end")
        self.text_area.configure(state="disabled")
        self.display_welcome_message()
        return ""
    
    def ai_request(self, command):
        asyncio.run(self.process_text(command))

    def exit_console(self):
        self.root.destroy()

    async def process_text(self, text):
        model = ArtificialInteligence()
        response = await model.generate_response(text)
        self.print_to_console("    " + response + "\n")

    def execute_command(self, event):
        command = self.input_entry.get()
        self.input_entry.delete(0, "end")
        self.print_to_console(f"[2501] > {command}\n")
        self.command_history.append(command)
        self.history_index = len(self.command_history)

        command_parts = command.split(" ", 1)
        if command_parts[0] in self.commands:
            if len(command_parts) > 1:
                result = self.commands[command_parts[0]][0](command_parts[1])
            else:
                result = self.commands[command_parts[0]][0]()
            if result is not None:
                self.print_to_console(result)
        else:
            self.print_to_console("Command is not found. Type \"help\" for more information...\n")

    def key_pressed(self, event):
        if event.keysym == "Up":
            self.history_up(event)
        elif event.keysym == "Down":
            self.history_down(event)

    def history_up(self, event):
        if self.history_index > 0:
            self.history_index -= 1
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.command_history[self.history_index])

    def history_down(self, event):
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.command_history[self.history_index])

if __name__ == "__main__":
    root = tk.Tk()
    console = ConsoleWindow(root)
    root.mainloop()