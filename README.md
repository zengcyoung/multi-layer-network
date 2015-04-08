# Multi-Layer Network

## Files

- **flatnet.py**: Read the files including the edge lists of two social network and the node mapping of them.

## Usage

```bash
flatnet.py splitter firstnet.csv secnet.csv node mapping.csv outfile.csv
```

## Known Issue

-   **2015/04/08**:

    -   **flatnet.py**:

        - The node acts as the target node may not be iterated.
        - `\t` will not be recognised as delimiter from command line input
