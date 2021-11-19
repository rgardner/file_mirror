# File Mirror

## Getting Started

Create a config file at `~/Desktop/sync_config.json` with the following
contents:

```json
{
    "copy_specs": [
        {
            "src": "~/foo/bar",
            "dst": "~/baz/bar",
            "last_sync_time": null
        },
        {
            "src": "/parent/dir",
            "dst": "~/other_dir",
            "last_sync_time": null
        }
    ]
}
```

Then, just run `file_mirror.py`! It will display the last sync time for each
folder and prompt you for confirmation before copying all the files in each of
the folders to the destination.

## Development

Run `script/setup.py` to install the development dependencies.
