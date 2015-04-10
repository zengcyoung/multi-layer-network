# Multi-Layer Network

## Files

- **Network.py**: Doing network-related algorithm.
- **MessageType.py**: Functions used to output different messages.
- **GUI.py**: Qt5 GUI (Not implemented)
- **main.py**: Main executable

## Usage

```bash
main.py splitter firstnet.csv secnet.csv nodemapping.csv outfile.csv
```

## Known Issue

-   **2015/04/08(Fixed)**:

    -   **Network.py**:

        - The node acts as the target node may not be iterated.
        - `\t` will not be recognised as delimiter from command line input
