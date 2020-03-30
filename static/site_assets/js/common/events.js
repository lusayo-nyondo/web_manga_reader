$(document).ready(function() {
    $('.back-button').on('click', function() {
        history.back();
    });
    
    $(window).scroll( function(event) {
        if(window.scrollY > 50) {
            document.getElementById('back-to-top-div').classList.remove('d-none');
        } else {
            document.getElementById('back-to-top-div').classList.add('d-none');
        }
    });
    
    var watchlist_toggler = $('[data-toggle="watchlist_state"]');
    
    if(watchlist_toggler)
        toggle_watchlist_state_button(watchlist_toggler);
    
    var bookmark_toggler = $('[data-toggle="bookmark_state"]');
    
    if (bookmark_toggler)
        toggle_bookmark_state_button(bookmark_toggler);
    
    $('[data-toggle="enable_inputs"]').on('click', function(event) {
        var button = event.currentTarget;
        var targets = button.getAttribute('data-targets');
        targets = targets.split(' ');
    
        enable_edit_user_details(button, targets);
    });
    
    $('[data-toggle="apply_filters"]').on('click', function(event) {
        var button = event.currentTarget;
    
        var filterable_section = button.getAttribute('data-filterable-section');
        var items_per_page = button.getAttribute('data-items-per-page');
    
        apply_active_filters(filterable_section, items_per_page);
    });

    $('[data-action="rate_manga"]').on('click', function(event) {
        var button = event.currentTarget;

        var manga_id = button.getAttribute('data-manga');
        var rating = button.getAttribute('data-value');

        submit_rating(button, manga_id, rating);
    });
    
    $.each($('[data-action="get_bookmarked"]'), function(index, element) {
        var manga_id = element.getAttribute('data-manga');

        get_bookmarked_chapter(element, manga_id);
    });

    $.each($('[data-action="get_last_read"]'), function(index, element) {
        var manga_id = element.getAttribute('data-manga');

        get_last_read_chapter(element, manga_id);
    });
});