import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        valid_target = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith("py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]

        if args != None:
            command.extend(args)

        msg = subprocess.run(
            command,
            capture_output=True,
            cwd=working_dir_abs,
            timeout=30,
            text=True
        )

        if msg.returncode != 0:
            return f"Process exited with code {msg.returncode}"

        if msg.stdout == "" and msg.stderr == "":
            return "No output produced"

        return f"STDOUT: {msg.stdout}\nSTDERR: {msg.stderr}"

    except Exception as e:
        return f"Error: executing Python file: {e}"
