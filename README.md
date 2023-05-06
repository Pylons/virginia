# virginia

This package provides a Pyramid application that is willing to serve slightly dynamic file content from a disk directory.

## Running

    pserve <configuration>

## Building

To build the universal wheel, run the following in the project directory:

    pip wheel --wheel-dir=build --no-dependencies .

## Developing

Install virginia in development mode:

    pip install -e .

Run tests:

    pytest virginia

Launch virginia with development settings:

    pserve development.ini
