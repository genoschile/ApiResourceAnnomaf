#!/usr/bin/env nextflow

// Define a parameter for the delay time (defaulting to 90 seconds)
params.delay_seconds = 20
// Define the name of the existing PDF file
params.pdf_source_name = "MAF_translate.pdf"

// --- Simulate a delay ---
process simulateDelay {
    output:
    path "delay_completed.txt"

    script:
    """
    echo "Simulating a ${params.delay_seconds} second delay..."
    sleep ${params.delay_seconds}s
    echo "Delay completed" > delay_completed.txt
    """
}

// --- Copy the existing PDF ---
process copyExistingPdf {
    input:
    path delay_signal

    output:
    path "${params.pdf_source_name}"

    script:
    """
    echo "Copying existing PDF '${params.pdf_source_name}' now that delay is complete..."
    # Copy the existing PDF from the project root to the process's work directory
    # 'baseDir' refers to the directory where the Nextflow script is being run from
    cp ${baseDir}/${params.pdf_source_name} .
    echo "PDF '${params.pdf_source_name}' copied successfully."
    """
}

// --- Workflow Definition ---
workflow {
    // Check if the source PDF file exists before starting the workflow
    if (!file(params.pdf_source_name).exists()) {
        error("Error: The PDF file '${params.pdf_source_name}' was not found in the project root directory '${baseDir}'.")
    }

    // Run the delay simulation
    delay_output = simulateDelay()

    // Pass the output of simulateDelay to copyExistingPdf
    // This ensures the copy operation only runs after the delay is complete
    copyExistingPdf(delay_output)

    log.info("Workflow started. The existing PDF '${params.pdf_source_name}' will be copied after a ${params.delay_seconds} second delay.")
}
