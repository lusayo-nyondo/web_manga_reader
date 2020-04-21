function is_element_in_view(element) {
    var docViewTop = $(window).scrollTop();
    var docViewBottom = docViewTop + $(window).height();
    var elemTop = $('#' + element.id).offset().top;
    return ((elemTop <= docViewBottom) && (elemTop >= docViewTop));
}

function is_user_authenticated() {
    var status_div = document.getElementById("user_authentication_status");

    var status_report = status_div.getAttribute('data-is-authenticated');

    if (status_report == 'True') {
        return true;
    } else if (status_report == 'False') {
        return false;
    }
}

function get_id_prefix(manga, section) {
    var id_prefix = null;

    var manga_id = manga.pk;
    var section_id = section.id;

    if (section.id == 'history') {
        var chapter_id = manga.history_entry[0].fields.chapter;
        var entry_id = manga.history_entry[0].pk;

        id_prefix = 'manga_' + manga_id + '_chapter_' + chapter_id + '_entry_' + section_id + '_entry_' + entry_id;
    } else {
        id_prefix = 'manga_' + manga_id + '_section_' + section_id + '_';
    }

    return id_prefix;
}

function clear_div(div) {
    while(div.childNodes.length != 0) {
        div.removeChild(div.childNodes[0]);
    }
}

function get_first_visible_child(container, children_class_selector) {
    var children = container.getElementsByClassName(children_class_selector);    

    var sorting_function = function(child_a, child_b){
        var child_a_offset_y = Math.abs(child_a.offsetTop - window.scrollY);
        var child_b_offset_y = Math.abs(child_b.offsetTop - window.scrollY);

        if (child_a_offset_y < child_b_offset_y) {
            return -1;
        } else if (child_a_offset_y > child_b_offset_y) {
            return 1;
        } else {
            return 0;
        }
    };

    children = Array.prototype.slice.call(children, 0);
    children = children.sort(sorting_function);

    alert(children[0].id);
    return children[0].id;
}