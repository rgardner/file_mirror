# File Mirror

## Getting Started

Create a config file at `~/Desktop/sync_config.json` with the following
contents:

```json
{
    "copy_specs": [
        {
            "src": "input directory 1",
            "dst": "output directory 1",
            "last_sync_time": null
        },
        {
            "src": "input directory 1",
            "dst": "output directory 1",
            "last_sync_time": null
        }
    ]
}
```

Then, just run `sync.py`! It will display the last sync times for each folder
and prompt you for confirmation before copying all the files in each of the
folders to the destination.

## Development

Run `script/setup.py` to install the development dependencies.
