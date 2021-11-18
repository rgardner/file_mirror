#!/usr/bin/env python

import argparse
import datetime
import json
import pathlib
import subprocess
import sys
from typing import List


CONFIG_FILE = "~/.config/file_mirror/config.json"


def parse_args(args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default=CONFIG_FILE,
        help=f"config file location, defaults to {CONFIG_FILE}",
    )
    return parser.parse_args(args)


def main(raw_args: List[str]) -> None:
    args = parse_args(raw_args)
    print(f"Reading config from {args.config}")

    # Read the config file
    config_path = pathlib.Path(args.config).expanduser()
    try:
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError:
        sys.exit(f"Could not find {config_path}")

    # Print the last sync time for each directory
    print("src\t\t\tdst\t\t\tlast sync time")
    for spec in config["copy_specs"]:
        src = spec["src"]
        dst = spec["dst"]
        last_sync_time = spec.get("last_sync_time") or "never"
        print("\t".join((src, dst, last_sync_time)))

    # Confirm sync
    while True:
        try:
            response = input("Sync all? [y/n] ")
        except (EOFError, KeyboardInterrupt):
            print("\nCanceling", file=sys.stderr)
            sys.exit(0)

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

    # If yes, run `rsync <src>/ <dst> --archive --delete --verbose`
    for copy_spec in config["copy_specs"]:
        src = pathlib.Path(copy_spec["src"]).expanduser()
        dst = pathlib.Path(copy_spec["dst"]).expanduser()
        print(f"Syncing {src} to {dst}")
        # Create the destination parent directory if it doesn't exist (rsync
        # doesn't do this automatically)
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            # Append '/' to avoid creating an extra directory at the
            # destination.
            src_arg = f"{str(src)}/"
            # Use --archive to preserve permissions and timestamps
            # Use --delete to delete files that are no longer in the source
            subprocess.run(
                ["rsync", src_arg, dst, "--archive", "--delete", "--verbose"],
                check=True,
            )
        except subprocess.CalledProcessError as exc:
            print(f"rsync failed: {exc}", file=sys.stderr)
            sys.exit(1)

    # Update the last sync time for each directory. Just use the same time
    # for each directory
    now = datetime.datetime.now()
    for i in range(len(config["copy_specs"])):
        config["copy_specs"][i]["last_sync_time"] = now.isoformat()
    with open(config_path, "w", encoding="utf-8") as fp:
        json.dump(config, fp, indent=4)


if __name__ == "__main__":
    main(sys.argv[1:])
