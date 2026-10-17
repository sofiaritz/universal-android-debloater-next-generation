#!/usr/bin/env python3

import json
import sys
from pathlib import Path


def build_uad_list(search_dir="lists", output_file="resources/assets/uad_lists.json"):
    search_path = Path(search_dir)
    if not search_path.exists():
        print(f"error: directory '{search_dir}' not found.")
        sys.exit(1)

    output_map = {}
    for json_path in search_path.rglob("*.json"):
        pkg_name = json_path.stem

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"error: failed to parse '{json_path}': {e}")
            sys.exit(1)

        if pkg_name != data["pkg_name"]:
            print(f"error: package name is mistmatched: path pkg_name '{pkg_name}' != defined pkg_name '{data['pkg_name']}'")
            sys.exit(1)

        output_map[pkg_name] = {
            "list": data["list"],
            "removal": data["removal"],
            "description": data["description"],

            "dependencies": [],
            "neededBy": [],
            "labels": [],
        }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_map, f, indent=2, sort_keys=True)

    print(f"successfully generated '{output_file}' with {len(output_map)} packages")

if __name__ == "__main__":
    build_uad_list()
