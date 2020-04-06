/** START WATCHLIST RELATED METHODS */
function toggle_watchlist_state_button(button) {
    var is_manga_in_watchlist = button.attr("data-value");

    var data = {
        manga_id: button.attr("data-manga"),
        user_id: button.attr("data-user")
    };

    if (is_manga_in_watchlist == "True") {
        set_button_state_remove_from_watchlist(data);
    } else if (is_manga_in_watchlist == "False") {
        set_button_state_add_to_watchlist(data);
    }
}

function set_button_state_remove_from_watchlist(data) {
    var button = document.getElementById("btn_toggle_watchlist_state");

    var btn_toggle_watchlist_state = create_btn_toggle_watchlist_state(data.user_id, data.manga_id, "remove_from_watchlist");
    var parent = button.parentNode;

    parent.removeChild(button);
    parent.appendChild(btn_toggle_watchlist_state);
}

function set_button_state_add_to_watchlist(data) {
    var button = document.getElementById("btn_toggle_watchlist_state");

    var btn_toggle_watchlist_state = create_btn_toggle_watchlist_state(data.user_id, data.manga_id, "add_to_watchlist");
    var parent = button.parentNode;

    parent.removeChild(button);
    parent.appendChild(btn_toggle_watchlist_state);
}

function create_btn_toggle_watchlist_state(user_id, manga_id, watchlist_state) {
    var button = document.createElement("button");
    button.id = "btn_toggle_watchlist_state";
    button.className = "btn";

    var icon = document.createElement("i");
    icon.classList.add("fas");

    var padding = document.createElement("span");
    padding.innerHTML = "&nbsp;&nbsp;";

    var text = document.createElement("span");
    text.classList.add("watchlist_state_text");

    switch(watchlist_state) {
        case "remove_from_watchlist": {
            icon.classList.add("fa-eye-slash");
            text.innerHTML = "Remove from library";
            button.classList.add("btn-danger");

            button.onclick = function() {
                remove_manga_from_watchlist(button, user_id, manga_id);
            };
        } break;

        case "add_to_watchlist": {
            icon.classList.add("fa-eye");
            text.innerHTML = "Add to library";
            button.classList.add("btn-warning");

            button.onclick = function() {
                add_manga_to_watchlist(button, user_id, manga_id);
            };
        } break;
    }

    button.type = "button";


    button.appendChild(icon);
    button.appendChild(padding);
    button.appendChild(text);

    return button;
}

function notify_user_remove_from_watchlist_results(response, button, data) {
    var status = response.status;

    if(status == "success") {
        set_button_state_add_to_watchlist(data);
        notify_with_popup(btn_toggle_watchlist_state, response.description);
    } else {
        notify_with_popup(button, response.description);
    }
}

function notify_user_add_to_watchlist_results(response, button, data) {
    var status = response.status;

    if (status == "success") {
        set_button_state_remove_from_watchlist(data);
        notify_with_popup(btn_toggle_watchlist_state, response.description);
    } else {
        notify_with_popup(button, response.description);
    }
}

function notify_user_failed_update_watchlist(response, button) {
    alert("An internal server error caused this action to fail. Contact the developers at developers@mangahive.com");
}

function lock_btn_toggle_watchlist_state() {
    var button = document.getElementById("btn_toggle_watchlist_state");
    lock_button_loading(button);
}

function unlock_btn_toggle_watchlist_state() {
    var button = document.getElementById("btn_toggle_watchlist_state");
    unlock_button_loading(button);
}

function add_manga_to_watchlist(button, user_id, manga_id) {
    if(user_id == 'None') {
        notify_with_popup(button, "You need to login to get this functionality.");
        return;
    }

    var data = {
        user_id: user_id,
        manga_id: manga_id,
    };

    lock_btn_toggle_watchlist_state();

    $.ajax({
        type:"GET",
        url:"/manga_site/add_manga_to_watchlist",
        data: data,
        success: function(response) {
            unlock_btn_toggle_watchlist_state();
            notify_user_add_to_watchlist_results(response, button, data);
        },
        error: function(response) {
            unlock_btn_toggle_watchlist_state();
            notify_user_failed_update_watchlist(response, button);
        }
    });
}

function remove_manga_from_watchlist(button, user_id, manga_id) {
    if(user_id == 'None') {
        notify_with_popup(button, "You need to login to get this functionality.");
        return;
    }

    var data = {
        user_id: user_id,
        manga_id: manga_id,
    };

    lock_btn_toggle_watchlist_state();

    $.ajax({
        type:"GET",
        url:"/manga_site/remove_manga_from_watchlist",
        data: data,
        success: function(response) {

            unlock_btn_toggle_watchlist_state();
            notify_user_remove_from_watchlist_results(response, button, data);
        },
        error: function(response) {
            unlock_btn_toggle_watchlist_state();
            notify_user_failed_update_watchlist(response, button);
        }
    });
}
/** END WATCHLIST RELATED METHODS */