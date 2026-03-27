import os


def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(
            os.path.join(working_dir_abs, directory)
        )

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        record = []
        for i in os.listdir(target_dir):
            if i.startswith("."):
                continue
            size = os.path.getsize(target_dir + "/" + i)
            isdir = os.path.isdir(target_dir + "/" + i)
            res = f"- {i}: file_size={size} bytes, is_dir={isdir}"
            record.append(res)
        return "\n".join(record)

    except Exception as e:
        return f"Error: {e}"
