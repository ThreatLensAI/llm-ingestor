def format_cve_data(cve_data):
    cve_id = cve_data["cveMetadata"].get("cveId", "N/A")
    date_published = cve_data["cveMetadata"].get("datePublished", "N/A")
    date_updated = cve_data["cveMetadata"].get("dateUpdated", "N/A")
    state = cve_data["cveMetadata"].get("state", "N/A")
    
    cna_container = cve_data["containers"].get("cna", {})
    
    title = cna_container.get("title", "N/A")
    
    # Descriptions
    descriptions = cna_container.get("descriptions", [{}])
    description_texts = [desc.get("value", "N/A") for desc in descriptions]
    
    # Affected products
    affected_products = cna_container.get("affected", [])
    affected_info = []
    for product in affected_products:
        for version in product.get("versions", []):
            product_info = "Product: {0} | Vendor: {1} | Version: {2} | Status: {3}".format(
                product.get('product', 'n/a'),
                product.get('vendor', 'n/a'),
                version.get('version', 'n/a'),
                version.get('status', 'n/a')
            )
            affected_info.append(product_info)
    
    # Impacts
    impacts = cna_container.get("impacts", [])
    impacts_info = []
    for impact in impacts:
        for description in impact.get("descriptions", [{}]):
            impacts_info.append(description.get("value", "N/A"))
    
    # Metrics
    metrics = cna_container.get("metrics", [])
    metrics_info = []
    for metric in metrics:
        if 'cvssV4_0' in metric:
            cvss = metric['cvssV4_0']
            metrics_info.append(
                "CVSS V4.0 Base Score: {0} | Severity: {1} | Vector: {2}".format(
                    cvss.get('baseScore', 'N/A'),
                    cvss.get('baseSeverity', 'N/A'),
                    cvss.get('vectorString', 'N/A')
                )
            )
    
    # Problem Types
    problem_types = cna_container.get("problemTypes", [{}])
    problem_type_info = []
    for problem_type in problem_types:
        for description in problem_type.get("descriptions", [{}]):
            problem_type_info.append(
                "Description: {0} | CWE ID: {1} | Type: {2}".format(
                    description.get('description', 'n/a'),
                    description.get('cweId', 'n/a'),
                    description.get('type', 'n/a')
                )
            )
    
    # References
    references = cna_container.get("references", [])
    references_info = []
    for ref in references:
        ref_info = "[{0} ({1})]({2})".format(
            ref.get('tags', ['n/a'])[0],
            ref.get('tags', ['n/a'])[0],
            ref.get('url', '#')
        )
        references_info.append(ref_info)
    
    # Source
    source = cna_container.get("source", {})
    source_info = "Defect: {0} | Discovery: {1}".format(
        ", ".join(source.get('defect', ['N/A'])),
        source.get('discovery', 'N/A')
    )
    
    output = (
        "The cve id of this document is : {0}. This document is also known as {0}."
        "{0} was published on {1} and was last Updated on {2}. The state of this cve {0} is {3}."
        "The title of this cve {0} is {4}."
        "The description of {0} cve is as follows: {5}.\n"
        "These are the products affected by vulnerability of {0}: {6}."
        "These are the impacts of this cve id {0}'s vulnerability: {7}."
        "These are the metrics of this cve: {8}."
        "These are the problem types of this cve: {9}."
        "These are the references of this {0}'s vulnerability: {10}."
        "This cve id {0} vulnerability's source is {11}."
    ).format(
        cve_id,
        date_published,
        date_updated,
        state,
        title,
        ",".join(description_texts),
        ",".join(affected_info),
        ",".join(impacts_info),
        ",".join(metrics_info),
        ",".join(problem_type_info),
        ",".join(references_info),
        source_info
    )
    
    return output.strip()
