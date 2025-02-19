const resources = [];
let content;

const loadResources = () => {
    const resource_rows = document.querySelectorAll('.resource-row');

    resource_rows.forEach(row => {
        const fullImageUrl = row.dataset.fullUrl;
        const type = row.dataset.type;
        const tds = row.querySelectorAll('td');
        const imageUrl = tds[0].innerText;
        const altText = tds[1].innerText;
        resources.push({type, fullImageUrl, imageUrl, altText});
    });
}

const addDisplayButtonsListener = () => {
    const carrouselButton = document.querySelector('#carrousel');
    const galerieButton = document.querySelector('#galerie');

    carrouselButton.addEventListener('click', function() {
        console.log('Carrousel button clicked');
        createCarrousel();
    });

    galerieButton.addEventListener('click', function() {
        console.log('Galerie button clicked');
        createGalerie();
    });
}

const addBackButtonListener = () => {
    const backButton = document.querySelector('#back');

    backButton.addEventListener('click', function() {
        recreateResourcesTable();
    });
}

const addTableResourcesListener = () => {
    const popup = document.querySelector('.image-popup');
    const resource_rows = document.querySelectorAll('.resource-row');

    // Add click handlers to rows
    resource_rows.forEach(function(row) {
        row.addEventListener('mousedown', function(e) {
            // Get URL from dataset
            const imageUrl = this.dataset.fullUrl;
            const type = this.dataset.type;

            // Create and show resource in popup
            if (type === 'IMAGE') {
                popup.innerHTML = `<img src="${imageUrl}" alt="Preview">`;
            } else if (type === 'VIDEO') {
                popup.innerHTML = `<video src="${imageUrl}" autoplay controls></video>`;
            }

            // Make popup visible to calculate its dimensions
            popup.style.display = 'block';

            // Calculate positions
            const popupHeight = popup.offsetHeight;
            const popupWidth = popup.offsetWidth;
            const windowHeight = window.innerHeight;
            const windowWidth = window.innerWidth;

            // Calculate left position
            let leftPos = e.pageX + 10;
            if (leftPos + popupWidth > windowWidth) {
                leftPos = windowWidth - popupWidth - 10;
            }

            // Calculate top position
            let topPos = e.pageY + 10;
            if (topPos + popupHeight > windowHeight) {
                topPos = e.pageY - popupHeight - 10; // Show above cursor if not enough space below
            }

            // Apply calculated positions
            popup.style.left = `${leftPos}px`;
            popup.style.top = `${topPos}px`;
        });

        // Hide popup when mouse is released
        row.addEventListener('mouseup', function() {
            popup.style.display = 'none';
        });

        // Also hide popup if mouse leaves the row while held down
        row.addEventListener('mouseleave', function() {
            popup.style.display = 'none';
        });
    });

    // Prevent text selection while dragging
    resource_rows.forEach(row => {
        row.addEventListener('mousedown', e => e.preventDefault());
    });
}

const recreateResourcesTable = () => {
    let html = '' +
        '<table id="resource-table" class="table table-striped table-hover mx-auto">\n' +
        '            <colgroup>\n' +
        '                <col>\n' +
        '                <col>\n' +
        '            </colgroup>\n' +
        '            <thead>\n' +
        '                <tr>\n' +
        '                    <th scope="col">Ressource</th>\n' +
        '                    <th scope="col">Alt</th>\n' +
        '                </tr>\n' +
        '            </thead>\n' +
        '            <tbody>';

    resources.forEach(resource => {
        html += '' +
            '                <tr class="resource-row" data-full-url="' + resource.fullImageUrl + '" data-type="' + resource.type + '">\n' +
            '                    <td>' + resource.imageUrl + '</td>\n' +
            '                    <td>' + resource.altText + '</td>\n' +
            '                </tr>';
    });

    html += '' +
        '            </tbody>\n' +
        '        </table>';

    html += '' +
        '<div class="container">\n' +
        '            <div class="row">\n' +
        '                <div class="col text-center">\n' +
        '                    <button class="btn btn-primary" id="carrousel">Carrousel</button>\n' +
        '                </div>\n' +
        '                <div class="col text-center">\n' +
        '                    <button class="btn btn-primary" id="galerie">Galerie</button>\n' +
        '                </div>    \n' +
        '            </div>\n' +
        '        </div>';

    content.innerHTML = html;

    // Re-attach event listeners after recreating the table
    addTableResourcesListener();
    addDisplayButtonsListener();
}

const createCarrousel = () => {
    let html = '<div id="resource-carousel" class="carousel slide" data-bs-ride="carousel">\n';

    // Add carousel inner with items
    html += '<div class="carousel-inner">\n';

    // Add each resource as a carousel item
    resources.forEach((resource, index) => {
        const activeClass = index === 0 ? 'active' : '';
        html += `<div class="carousel-item ${activeClass}">\n`;

        if (resource.type === 'IMAGE') {
            html += `<img src="${resource.fullImageUrl}" class="d-block w-100" alt="${resource.altText}">\n`;
        } else if (resource.type === 'VIDEO') {
            html += `<video src="${resource.fullImageUrl}" class="d-block w-100" controls></video>\n`;
        }

        html += '</div>\n';
    });

    html += '</div>\n';

    // Add carousel controls
    html +=
        '<button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="prev">\n' +
        '    <span class="carousel-control-prev-icon" aria-hidden="true"></span>\n' +
        '    <span class="visually-hidden">Previous</span>\n' +
        '</button>\n' +
        '<button class="carousel-control-next" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="next">\n' +
        '    <span class="carousel-control-next-icon" aria-hidden="true"></span>\n' +
        '    <span class="visually-hidden">Next</span>\n' +
        '</button>\n' +
        '</div>';

    html +=
        '<div class="container mt-3">\n' +
        '    <div class="row">\n' +
        '        <div class="col text-center">\n' +
        '            <button class="btn btn-primary" id="back">Back</button>\n' +
        '        </div>\n' +
        '    </div>\n' +
        '</div>';

    content.innerHTML = html;

    // Re-attach event listeners after creating carousel
    addBackButtonListener();

    // Initialize Bootstrap carousel
    const carousel = new bootstrap.Carousel(document.querySelector('#resource-carousel'));
}

const createGalerie = () => {
    let html = '<div class="container">\n<div class="row">\n';

    // Create gallery grid
    resources.forEach(resource => {
        html += '<div class="col-md-4 mb-4">\n<div class="card">\n';

        if (resource.type === 'IMAGE') {
            html += `<img src="${resource.fullImageUrl}" class="card-img-top" alt="${resource.altText}">\n`;
        } else if (resource.type === 'VIDEO') {
            html += `<video src="${resource.fullImageUrl}" class="card-img-top" controls></video>\n`;
        }

        html +=
            `<div class="card-body">\n` +
            `<p class="card-text">${resource.altText}</p>\n` +
            `</div>\n` +
            `</div>\n` +
            `</div>\n`;
    });

    html += '</div>\n</div>\n';

    html +=
        '<div class="container mt-3">\n' +
        '    <div class="row">\n' +
        '        <div class="col text-center">\n' +
        '            <button class="btn btn-primary" id="back">Back</button>\n' +
        '        </div>\n' +
        '    </div>\n' +
        '</div>';

    content.innerHTML = html;

    // Re-attach event listeners after creating gallery
    addBackButtonListener();
}

window.onload = function() {
    content = document.querySelector('.content');

    loadResources();
    addTableResourcesListener();
    addDisplayButtonsListener();
};