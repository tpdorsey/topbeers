# Topbeers

These are simple, probably very brittle scripts for compiling the Beer Advocate top 250 beers into a table, with some added logic to grab brewer-specific data.

topbeers.py is a classic Python script to compile the data into a markdown table.

topbeers-prefect.py is the same idea implemented as a [Prefect](https://prefect.io) flow run using a local [Dask](https://dask.org/) executor for parallel processing of mapped tasks.

There's probably a lot of room for further expansion and optimization here, so feel free to experiment.