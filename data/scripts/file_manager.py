import json
import os


def read_json(path, is_json=False):
    """
    Reads a file and optionally parses it as JSON.

    Args:
        path (str): The relative path to the file (from the `data` folder).
        is_json (bool): If True, parses the file content as JSON.

    Returns:
        str or dict: File content as a string, or parsed JSON as a dictionary.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not valid JSON when `is_json` is True.
    """
    full_path = os.path.join("data", path)

    try:
        with open(full_path, 'r') as file:
            content = file.read()
            return json.loads(content) if is_json else content
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {full_path} does not exist.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON in file {full_path}: {e}")


def write_json(path, data, is_json=False):
    full_path = os.path.join("data", path)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    try:
        with open(full_path, 'w') as file:
            if is_json:
                json.dump(data, file, indent=4)
            else:
                file.write(data)
        return True
    except TypeError as e:
        raise TypeError(f"Data is not JSON serializable: {e}")
    except OSError as e:
        raise OSError(f"Error writing to file {full_path}: {e}")
