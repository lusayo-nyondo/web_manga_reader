function toggle_bookmark_state_button(button) {
    var is_chapter_in_bookmarks = button.attr('data-value');

    var data = {
        manga_id: button.attr('data-manga'),
        chapter_id: button.attr('data-chapter'),
        user_id: button.attr('data-user')
    };

    if (is_chapter_in_bookmarks == "True") {
        set_button_state_remove_from_bookmarks(data);
    } else if (is_chapter_in_bookmarks == "False") {
        set_button_state_add_to_bookmarks(data);
    }
}

function lock_btn_toggle_bookmark_state() {
    var button = document.getElementById("btn_toggle_bookmark_state");
    lock_button_loading(button);
}

function unlock_btn_toggle_bookmark_state() {
    var button = document.getElementById("btn_toggle_bookmark_state");
    unlock_button_loading(button);
}

function set_button_state_add_to_bookmarks(data) {
    var button = document.getElementById("btn_toggle_bookmark_state");

    var btn_toggle_bookmark_state = create_btn_toggle_bookmark_state(data.user_id, data.manga_id, data.chapter_id, data.csrf_token, "add_to_bookmarks");
    var parent = button.parentNode;

    parent.removeChild(button);
    parent.appendChild(btn_toggle_bookmark_state);
}

function set_button_state_remove_from_bookmarks(data) {
    var button = document.getElementById("btn_toggle_bookmark_state");

    var btn_toggle_bookmark_state = create_btn_toggle_bookmark_state(data.user_id, data.manga_id, data.chapter_id, data.csrf_token, "remove_from_bookmarks");
    var parent = button.parentNode;

    parent.removeChild(button);
    parent.appendChild(btn_toggle_bookmark_state);
}

function create_btn_toggle_bookmark_state(user_id, manga_id, chapter_id, csrf_token, bookmark_state) {
    var button = document.createElement("button");

    button.id = "btn_toggle_bookmark_state";
    button.type = "button";
    button.tooltip = "Bookmark this chapter.";

    button.setAttribute('data-toggle', 'bookmark_state');
    button.setAttribute('data-user', user_id);
    button.setAttribute('data-manga', manga_id);
    button.setAttribute('data-chapter', chapter_id);

    var i = document.createElement("i");
    i.className = "fas fa-bookmark";

    button.appendChild(i);

    switch(bookmark_state) {
        case "add_to_bookmarks": {
            button.className = "btn btn-warning";
            button.setAttribute("data-is-chapter-bookmarked", "False");

            button.onclick = function() {
                add_manga_chapter_to_bookmarks(button, user_id, manga_id, chapter_id, csrf_token);
            };
        } break;

        case "remove_from_bookmarks": {
            button.className = "btn btn-danger";
            button.setAttribute("data-is-chapter-bookmarked", "True");

            button.onclick = function() {
                remove_manga_chapter_from_bookmarks(button, user_id, manga_id, chapter_id, csrf_token);
            };
        } break;
    }

    return button;
}

function notify_user_add_to_bookmarks_results(response, button, data) {
    var status = response.status;

    if (status == "success") {
        set_button_state_remove_from_bookmarks(data);
        notify_with_popup(button, response.description);
    } else {
        notify_with_popup(button, response.description);
    }
}

function notify_user_remove_from_bookmarks_results(response, button, data) {
    var status = response.status;

    if (status == "success") {
        set_button_state_add_to_bookmarks(data);
        notify_with_popup(button, response.description);
    } else {
        notify_with_popup(button, response.description);
    }
}

function notify_user_failed_update_bookmarks(response, button) {
    alert("An internal server error caused this action to fail. Contact the developers at developers@mangahive.com");
}

function add_manga_chapter_to_bookmarks(button, user_id, manga_id, chapter_id, csrf_token) {
    if(user_id == 'None') {
        notify_with_popup(button, "You need to login to get this functionality.");
        return;
    }

    var data = {
        user_id: user_id,
        manga_id: manga_id,
        chapter_id: chapter_id
    };

    lock_btn_toggle_bookmark_state();

    $.ajax({
        url:'/manga_site/add_chapter_to_bookmarks',
        method:'GET',
        headers: {
            'X-CSRFToken': csrf_token
        },
        data: data,
        success: function(response) {
            unlock_btn_toggle_bookmark_state();
            notify_user_add_to_bookmarks_results(response, button, data);
        },
        error: function(response) {
            unlock_btn_toggle_bookmark_state();
            alert("Error adding chapter to bookmarks. Debug for details.");
        }
    });
}

function remove_manga_chapter_from_bookmarks(button, user_id, manga_id, chapter_id, csrf_token) {
    if(user_id == 'None') {
        notify_with_popup(button, "You need to login to get this functionality.");
        return;
    }

    var data = {
        user_id: user_id,
        manga_id: manga_id,
        chapter_id: chapter_id
    };

    lock_btn_toggle_bookmark_state();

    $.ajax({
        url:'/manga_site/remove_chapter_from_bookmarks',
        method:'GET',
        headers: {
            'X-CSRFToken': csrf_token
        },
        data: data,
        success: function(response) {
            unlock_btn_toggle_bookmark_state();
            notify_user_remove_from_bookmarks_results(response, button, data);
        },
        error: function(response) {
            unlock_btn_toggle_bookmark_state();
            alert("Error adding chapter to bookmarks. Debug for details.");
        }
    });
}

function get_bookmarked_chapter(button, manga_id) {
    $.ajax({
        url: '/manga_site/bookmarked_json',
        method: 'GET',
        data: {
            manga_id: manga_id,
        },
        success: function(response) {
            if (response.status == 'success') {
                update_bookmarked_chapter(button, manga_id, response.chapter);
            } else if (response.status == 'bookmark_not_found') {
                remove_bookmarked_chapter_probe(button, manga_id);
            } else {
                notify_with_popup(button, response.status);
            }
        },
        error: function(response) {
            console.log(response);
            //notify_with_popup(button, response);
        }
    });
}

function remove_bookmarked_chapter_probe(button, manga_id) {
    var bookmarked_chapter_probe_id = 'bookmarked_chapter_probe_' + manga_id;

    var bookmarked_chapter_probe = document.getElementById(bookmarked_chapter_probe_id);

    var parent = bookmarked_chapter_probe.parentNode;
    parent.removeChild(bookmarked_chapter_probe);
}

function update_bookmarked_chapter(button, manga_id, chapter) {
    var bookmarked_chapter_link = create_bookmarked_chapter_link(manga_id, chapter);

    var parent = button.parentNode;
    parent.removeChild(button);
    parent.appendChild(bookmarked_chapter_link);
}

function create_bookmarked_chapter_link(manga_id, chapter) {
    var link = document.createElement('a');
    link.href = "/manga/manga/" + manga_id + '/chapters/' + chapter.chapter_number;
    link.class = "current_chapter";

    var icon = document.createElement('i');
    icon.className = 'fa fa-bookmark';

    var wrapper_span = document.createElement("span");

    var padding = document.createElement("span");
    padding.innerHTML = '&nbsp';

    var span = document.createElement('span');
    span.innerHTML = "You bookmarked chapter " + chapter.chapter_number;

    wrapper_span.appendChild(padding);
    wrapper_span.appendChild(span);

    link.appendChild(icon);
    link.appendChild(wrapper_span);

    return link;
}