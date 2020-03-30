
function collapseSideNav() {
    document.getElementById("navigation-drawer-expanded").classList.add('collapsed');
    hideOverlay();
}

function expandSideNav() {
    document.getElementById("navigation-drawer-expanded").classList.remove('collapsed');
    showOverlay();
}

function toggleSideNavState() {
    
    expandedDrawer.classList.toggle('collapsed');   
}

function hideOverlay() {
    var drawerOverlay = document.getElementById("overlay");
    drawerOverlay.classList.add('d-none');
    drawerOverlay.classList.add('animate');
}

function showOverlay() {
    var drawerOverlay = document.getElementById("overlay");
    drawerOverlay.classList.remove('animate');
    drawerOverlay.classList.remove('d-none');
}

function create_dismissible_popup(message, dismissal_text, dismiss_function) {
    var popover_content = document.createElement("div");
    popover_content.className = "d-flex flex-column align-content-center align-items-center justify-content-center justify-items-center";
    
    var message_span = document.createElement("span");
    message_span.className = "w-100 text-center d-block";
    message_span.innerHTML = message;

    var dismiss_button = document.createElement("button");
    dismiss_button.className = "btn btn-warning text-dark";

    var dismiss_button_text = document.createElement("span");
    dismiss_button_text.innerHTML = "&nbsp;&nbsp;" + dismissal_text;

    var dismiss_button_icon = document.createElement("i");
    dismiss_button_icon.className = "fa fa-thumbs-up";

    dismiss_button.appendChild(dismiss_button_icon);
    dismiss_button.appendChild(dismiss_button_text);
    
    dismiss_button.addEventListener("click", function() {
        dismiss_function();
    });

    popover_content.appendChild(message_span);
    popover_content.appendChild(dismiss_button);

    return popover_content;
}

function notify_with_popup(element, message) {
    var id = "#" + element.id;
    
    var dismiss_function = function() {
        $(id).popover('hide');
    };

    var popover_content = create_dismissible_popup(message, "Ok, got it!", dismiss_function);

    $(id).popover({
        content: popover_content,
        html: true,
        trigger: "manual",
    });

    $(id).popover("show");
}

function lock_button_loading(button) {
    button.setAttribute("disabled", "disabled");
    button.classList.add("position-relative");

    var overlay = create_loading_overlay();
    button.appendChild(overlay);
}

function unlock_button_loading(button) {
    button.removeAttribute("disabled");

    var overlay = button.getElementsByClassName("input-overlay");
    var i = 0, l = overlay.length;

    for(; i < l; i++) {
        button.removeChild(overlay[i]);
    }
}

function lock_module_loading() {
    var element = document.getElementById("module_content");

    element.classList.add('position-relative');

    var overlay_parent = document.createElement('div');
    overlay_parent.id = 'module_lock';
    overlay_parent.className = 'module-lock';

    var overlay = create_loading_overlay();
    
    overlay_parent.appendChild(overlay);

    element.appendChild(overlay_parent);
}

function unlock_module_loading() {
    var module_lock = document.getElementById('module_lock');
    var parent = module_lock.parentNode;

    parent.removeChild(module_lock);
}

function create_loading_overlay() {
    var overlay = document.createElement("span");
    overlay.className = "input-overlay d-flex position-absolute align-items-center align-content-center justify-items-center justify-content-center w-100 h-100 position-absolute overlay-span bg-dark-faded";
    overlay.style = "z-index: 9999;";

    var loading = document.createElement("i");
    loading.className = "spinner spinner-border";

    overlay.appendChild(loading);

    return overlay;
}