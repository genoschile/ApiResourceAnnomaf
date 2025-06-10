#!/usr/bin/env nextflow

process sayHello {
    output:
        stdout

    """
    echo 'Hello World from Nextflow!'
    """
}

/*
voy a generar un output file format pdf /async
*/
