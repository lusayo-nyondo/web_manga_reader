function load_visible_page_webtoon_format() {
    $('[data-action="view_manga_page"]').each(function(index, element) {
        load_page_webtoon_format(element);
    });
}

function load_page_webtoon_format(element) {
    var status = element.getAttribute('data-status');

    if (status == 'loaded') {
        return;
    } else if (status == 'unloaded') {
        if (is_element_in_view(element)) {
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
    }
}
