$(document).ready(function() {
    trigger_document_level_events();
    trigger_search_manga_events();
    trigger_navigation_events();
    trigger_quick_scrolling_events();
    trigger_bookmark_events();
    trigger_watchlist_events();
    trigger_apply_ordering_rule_events();
    trigger_apply_filters_events();
    trigger_enable_inputs_events();
    trigger_get_last_read_events();
    trigger_get_bookmarked_events();
    trigger_image_stub_events();
    trigger_rate_manga_events();
});

function trigger_document_level_events() {
    document.onclick = function(event) {
        hide_search_results();
    };
}

function trigger_search_manga_events() {
    $('[data-action="search_manga"]').on('keyup', function(event){
        var input = event.currentTarget;
        search_manga(input);
    });
}

function trigger_navigation_events() {
    $('.back-button').on('click', function() {
        history.back();
    });
}

function trigger_quick_scrolling_events() {
    $(window).scroll( function(event) {
        if(window.scrollY > 50) {
            document.getElementById('back-to-top-div').classList.remove('d-none');
        } else {
            document.getElementById('back-to-top-div').classList.add('d-none');
        }
    });
}

function trigger_bookmark_events() {
    var bookmark_toggler = $('[data-toggle="bookmark_state"]');

    if (bookmark_toggler)
        toggle_bookmark_state_button(bookmark_toggler);
}

function trigger_watchlist_events() {
    var watchlist_toggler = $('[data-toggle="watchlist_state"]');

    if(watchlist_toggler)
        toggle_watchlist_state_button(watchlist_toggler); 
}

function trigger_enable_inputs_events() {
    $('[data-toggle="enable_inputs"]').on('click', function(event) {
        var button = event.currentTarget;
        var targets = button.getAttribute('data-targets');
        targets = targets.split(' ');

        enable_edit_user_details(button, targets);
    });
}

function trigger_apply_filters_events() {
    $('[data-toggle="apply_filters"]').on('click', function(event) {
        var button = event.currentTarget;

        var filterable_section = button.getAttribute('data-filterable-section');
        var items_per_page = button.getAttribute('data-items-per-page');

        apply_active_filters(filterable_section, items_per_page);
    });
}

function trigger_apply_ordering_rule_events() {
    $('[data-toggle="apply_ordering_rule"]').on('change', function(event) {
       var select = event.currentTarget;

       var filterable_section = select.getAttribute('data-filterable-section');
       var items_per_page = select.getAttribute('data-items-per-page');

       apply_ordering_rule(filterable_section, items_per_page);
    });
}

function trigger_rate_manga_events() {
    $('[data-action="rate_manga"]').on('click', function(event) {
        var button = event.currentTarget;

        var manga_id = button.getAttribute('data-manga');
        var rating = button.getAttribute('data-value');

        submit_rating(button, manga_id, rating);
    });
}

function trigger_get_last_read_events() {
    $.each($('[data-action="get_last_read"]'), function(index, element) {
        var manga_id = element.getAttribute('data-manga');

        get_last_read_chapter(element, manga_id);
    });
}

function trigger_get_bookmarked_events() {
    $.each($('[data-action="get_bookmarked"]'), function(index, element) {
        var manga_id = element.getAttribute('data-manga');

        get_bookmarked_chapter(element, manga_id);
    });
}

function trigger_image_stub_events() {        
    $('[data-toggle="image_stub"]').each(function(index, element) {
        var el = document.getElementById(element.id);
        fetch_image(el);
    });
}