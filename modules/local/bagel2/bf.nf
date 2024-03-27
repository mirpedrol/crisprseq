process BAGEL2_BF {
    tag "${meta.treatment}_${meta.reference}"
    label 'process_single'


    conda "python=3.11.4 pandas=2.0.3 numpy=1.25.1 scikit-learn=1.3.0 click=8.1.6"
    container "${ workflow.containerEngine == 'singularity' && !task.ext.singularity_pull_docker_container ?
        'https://depot.galaxyproject.org/singularity/mulled-v2-1ec3f69e7819b1ab3e6f57d16594eb40ed7d6792:f94a27287a1921ce0dacd411d48acff738d3ca90-0':
        'biocontainers/mulled-v2-1ec3f69e7819b1ab3e6f57d16594eb40ed7d6792:f94a27287a1921ce0dacd411d48acff738d3ca90-0' }"


    input:
    tuple val(meta), path(foldchange)
    path(reference_essentials)
    path(reference_nonessentials)

    output:
    tuple val(meta), path("*.bf"), emit: bf
    path "versions.yml"          , emit: versions

    when:
    task.ext.when == null || task.ext.when

    script:
    def args = task.ext.args ?: ''
    def prefix = task.ext.prefix ?: "${meta.treatment}_vs_${meta.reference}"

    """
    BAGEL.py bf -i $foldchange -o '${meta.treatment}_vs_${meta.reference}.bf' $args -e $reference_essentials -n $reference_nonessentials -c ${meta.treatment}

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        python: \$(python --version | sed 's/Python //g')
        BAGEL2: \$( BAGEL.py version | grep -o 'Version: [0-9.]*' | awk '{print  \$2}' | grep -v '^\$')
    END_VERSIONS
    """

}
