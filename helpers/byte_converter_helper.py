# byte_converter_helper.py - Helper functions to convert files to Base64 and restore them back.

import base64
import json
from pathlib import Path


# Convert file to Base64
# file_to_base64("./output/text_1/1_output.png", "payload.txt")

def file_to_base64(input_path: str, output_txt: str):
    path = Path(input_path)

    data = path.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")

    payload = {
        "extension": path.suffix,  # stores the extension
        "data": b64
    }

    Path(output_txt).write_text(json.dumps(payload))
    print("File converted to Base64 with extension saved.")


# Restore file from Base64
# base64_to_file("payload.txt", "arquivo_restaurado")

def base64_to_file(input_txt: str, output_name: str):
    payload = json.loads(Path(input_txt).read_text())

    extension = payload["extension"]
    b64 = payload["data"]

    file_bytes = base64.b64decode(b64)

    output_path = output_name + extension
    Path(output_path).write_bytes(file_bytes)

    print(f"File recreated: {output_path}")


# EXAMPLE USAGE



