function get_last_read_chapter(button, manga_id) {
    $.ajax({
        url: '/manga_site/last_read_json',
        method: 'GET',
        data: {
            manga_id: manga_id,
        },
        success: function(response) {
            if (response.status == 'success') {
                update_last_read_chapter(button, manga_id, response.chapter);
            } else if (response.status == 'last_read_not_found') {
                remove_last_read_chapter_probe(button, manga_id);
            } else {
                notify_with_popup(button, response.status);
            }
        },
        error: function(response) {
            notify_with_popup(button, response);
        }
    });
}

function remove_last_read_chapter_probe(button, manga_id) {
    var last_read_chapter_probe_id = 'last_read_chapter_probe_' + manga_id;

    var last_read_chapter_probe = document.getElementById(last_read_chapter_probe_id);

    var parent = last_read_chapter_probe.parentNode;
    parent.removeChild(last_read_chapter_probe);
}

function update_last_read_chapter(button, manga_id, chapter) {
    var last_read_chapter_link = create_last_read_chapter_link(manga_id, chapter);

    var parent = button.parentNode;
    parent.removeChild(button);
    parent.appendChild(last_read_chapter_link);
}

function create_last_read_chapter_link(manga_id, chapter) {
    var link = document.createElement('a');
    link.href = "/manga/manga/" + manga_id + '/chapters/' + chapter.chapter_number;
    link.class = "current_chapter";

    var icon = document.createElement('i');
    icon.className = 'fa fa-history';

    var wrapper_span = document.createElement("span");
    
    var padding = document.createElement("span");
    padding.innerHTML = '&nbsp';

    var span = document.createElement('span');
    span.innerHTML = "You last read chapter " + chapter.chapter_number;

    wrapper_span.appendChild(padding);
    wrapper_span.appendChild(span);

    link.appendChild(icon);
    link.appendChild(wrapper_span);

    return link;
}