#!/usr/bin/env python3
import sys
from urllib.parse import urlparse, urljoin


def get_absolute_url(base_url, relative_url):
    """Convert relative URL to absolute URL."""
    # Return the relative URL if it's already absolute
    if bool(urlparse(relative_url).netloc):
        return relative_url
    # Otherwise, join the base URL with the relative URL
    return urljoin(base_url, relative_url)


def get_resources_from_input():
    """Get the resources from the input."""
    lines = []
    try:
        # Read input line by line from stdin
        for line in sys.stdin:
            lines.append(line.rstrip())
    except KeyboardInterrupt:
        sys.exit(0)
    except BrokenPipeError:
        sys.stderr.close()
        sys.exit(0)

    if not lines:
        return []

    path = lines[0].split(' ', 1)[1] if lines[0].startswith('PATH ') else ''
    resources = []

    for i in range(1, len(lines)):
        parts = lines[i].split(' ', 2)  # Split into max 3 parts: type, url, and possibly alt

        if len(parts) >= 2:  # Must have at least type and URL
            resource_type = parts[0]
            url = parts[1]
            alt = parts[2].replace('"','') if len(parts) > 2 else "Client Image"  # Default alt text

            full_url = get_absolute_url(path, url)
            resources.append((resource_type, url, full_url, alt))

    return resources


def create_resource_tr(resource):
    return f"""
        <tr class="resource-row" data-full-url="{resource[2]}" data-type="{resource[0]}">
            <td>{resource[1]}</td>
            <td>{resource[3]}</td>
        </tr>
    """

def generate_html(resources):
    """Generate the HTML content based on the resources."""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <title>Visualisateur d'images/vidéos</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="styles.css">
    <!-- Bootstrap styling -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- Roboto font -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
</head>
<body>
    <h1 class="text-center m-4">Visualisateur</h1>
    <h2 class="text-center fs-5">d'images/vidéos</h2>

    <div class="container content m-5">
        <table id="resource-table" class="table table-striped table-hover mx-auto">
            <colgroup>
                <col>
                <col>
            </colgroup>
            <thead>
                <tr>
                    <th scope="col">Ressource</th>
                    <th scope="col">Alt</th>
                </tr>
            </thead>
            <tbody>
    """

    for resource in resources:
        html += create_resource_tr(resource)

    html += """
    </tbody>
        </table>

        <div class="container">
            <div class="row">
                <div class="col text-center">
                    <button class="btn btn-primary" id="carrousel">Carrousel</button>
                </div>
                <div class="col text-center">
                    <button class="btn btn-primary" id="galerie">Galerie</button>
                </div>    
            </div>
        </div>
    </div>

    <div class="image-popup"></div>

    <!-- Bootstrap script -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="script.js"></script>
</body>
</html>
    """

    return html

def main():
    resources = get_resources_from_input()
    html = generate_html(resources)
    sys.stdout.write(html)


if __name__ == '__main__':
    main()