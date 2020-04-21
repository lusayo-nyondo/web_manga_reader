function load_first_page_single_page_format() {
    if ($('[data-is-active="true"]').length == 0) {
        $('[data-page-number="1"]').each(function(index, element) {
            load_page_single_page_format(element);
        });
    }
}

function load_page_single_page_format(element) {
    var status = element.getAttribute('data-status');

    hide_all_pages(); 

    if (status == 'loaded') {
        //return;
    } else if (status == 'unloaded') {
        var src = element.getAttribute('data-src');
        var class_name = element.getAttribute('data-resource-class');
        var alternate = element.getAttribute('data-resource-alternate');
        var id = element.getAttribute('data-resource-id');
        
        var image = document.createElement('img');
        
        image.src = src;
        image.className = class_name;
        image.alternate = alternate;
        image.id = id;

        clear_div(element);

        element.appendChild(image);

        element.setAttribute('data-status', 'loaded');
    }

    element.setAttribute('data-is-active', 'true');
    element.classList.remove('d-none');

    window.scrollTo(0, 0);
}

function hide_all_pages() {
    $('[data-action="view_manga_page"]').each(function(index, element) {
        element.classList.add('d-none');
        element.setAttribute('data-is-active', 'false');
    });
}

function fetch_next_page() {
    var current_page = $('[data-is-active="true"]')[0];
    var current_page_number = current_page.getAttribute('data-page-number');
    
    var next_page_number = (1 * current_page_number) + 1;
    var next_page = $('[data-page-number="' + next_page_number +'"]')[0];

    if (next_page) {
        load_page_single_page_format(next_page);
    }
}

function fetch_previous_page() {
    var current_page = $('[data-is-active="true"]')[0];
    var current_page_number = current_page.getAttribute('data-page-number');
    
    var previous_page_number = (1 * current_page_number) - 1;
    var previous_page = $('[data-page-number="' + previous_page_number +'"]')[0];

    if (previous_page) {
        load_page_single_page_format(previous_page);
    }   
}