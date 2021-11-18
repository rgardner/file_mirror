#!/usr/bin/env python

import datetime
import json
import pathlib
import subprocess
import sys


CONFIG_FILE = pathlib.Path.home() / "Desktop" / "sync_config.json"


def main() -> None:
    # Read the config file
    try:
        with open(CONFIG_FILE, encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError:
        sys.exit(f"Could not find {CONFIG_FILE}")

    # Print the last sync time for each directory
    for copy_spec in config["copy_specs"]:
        print("\t".join(copy_spec[key] for key in ["src", "dst", "last_sync_time"]))

    # Prompt to sync
    while True:
        response = input("Sync all? [y/n] ")
        if response.lower() in ("y", "yes"):
            break

        if response.lower() in ("n", "no"):
            print("Canceling", file=sys.stderr)
            sys.exit(0)
        else:
            print(
                f"Unrecognized response: '{response}'. Please reply yes/no",
                file=sys.stderr,
            )

    # If yes, run `rsync <src> <dst> --archive --delete --verbose`
    for copy_spec in config["copy_specs"]:
        src = copy_spec["src"]
        dst = copy_spec["dst"]
        print(f"Syncing {src} to {dst}")
        try:
            subprocess.run(
                ["rsync", src, dst, "--archive", "--delete", "--verbose"], check=True
            )
        except subprocess.CalledProcessError as exc:
            print(f"rynsc failed: {exc}", file=sys.stderr)
            sys.exit(1)

    # Update the last sync time for each directory
    now = datetime.datetime.now()
    for i, copy_spec in enumerate(config["copy_specs"]):
        config["copy_specs"][i]["last_sync_time"] = str(now)
    with open(CONFIG_FILE, "w", encoding="utf-8") as fp:
        json.dump(config, fp, indent=4)


if __name__ == "__main__":
    main()
