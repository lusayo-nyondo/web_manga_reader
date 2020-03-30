function submit_user_details(event, targets) {
    var data = {};

    var i = 0, l = targets.length;
    var button = event.currentTarget;

    for (; i < l; i++) {
        var target = targets[i];
        var element = document.getElementById(target);
        var value = element.value;

        data[target] = value;
    }

    $.ajax({
        url: '/account/edit',
        method: 'GET',
        data: data,
        success: function(response) {
            
            var enable_edit_user_details_button = create_enable_edit_user_details_button(targets);
            
            var parent = button.parentNode;
            parent.removeChild(button);
            parent.appendChild(enable_edit_user_details_button);

            var receive_notifications = response.user.receive_notifications;

            var receive_notifications_checkbox = document.getElementById('receive_notifications');

            if(receive_notifications) {
                receive_notifications_checkbox.setAttribute('checked', 'checked');
            } else {
                receive_notifications_checkbox.removeAttribute('checked');
            }

            if(response.status == "success") {
                notify_with_popup(enable_edit_user_details_button, response.summary);
            } else {
                notify_with_popup(enable_edit_user_details_button, response.summary);
            }

            var i = 0, l = targets.length;

            for (; i < l; i++) {
                var element = document.getElementById(targets[i]);
                element.setAttribute("disabled", "disabled");
            }
        },
        error: function(response) {
            notify_with_popup(button, response);
        }
    });
}

function enable_edit_user_details(source, targets) {
    var i = 0, l = targets.length;

    for(; i < l; i++) {
        var target_element = document.getElementById(targets[i]);
        target_element.removeAttribute('disabled');
    }

    var submit_user_details_button = create_submit_user_details_button(targets);
    
    var parent = source.parentNode;
    parent.removeChild(source);
    parent.appendChild(submit_user_details_button);

    return submit_user_details_button;
}

function create_submit_user_details_button(targets) {
    var button = document.createElement("button");
    button.setAttribute("type", "button");

    button.id = "btn_submit_user_details";
    button.className = "btn btn-outline-dark";

    var icon = document.createElement("i");
    icon.className = "fa fa-save";

    var padding = document.createElement("span");
    padding.innerHTML = "&nbsp;&nbsp;";

    var span = document.createElement("span");
    span.innerHTML = "Save Changes";

    button.appendChild(icon);
    button.appendChild(padding);
    button.appendChild(span);

    button.onclick = function(event) {
        submit_user_details(event, targets);
    };

    return button;
}

function create_enable_edit_user_details_button(targets) {
    var button = document.createElement("button");
    button.setAttribute("type", "button");
    button.setAttribute("data-toggle", "enable_inputs");
    button.setAttribute("data-targets", targets);

    button.id = "btn_edit_user_details";
    button.className = "btn btn-outline-dark";

    var icon = document.createElement("i");
    icon.className = "fa fa-unlock";

    var padding = document.createElement("span");
    padding.innerHTML = "&nbsp;&nbsp;";

    var span = document.createElement("span");
    span.innerHTML = "Edit";

    button.appendChild(icon);
    button.appendChild(padding);
    button.appendChild(span);

    button.onclick = function(event) {
        enable_edit_user_details(button, targets);
    };

    return button;
}
