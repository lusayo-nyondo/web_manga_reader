function establish_reading_mode() {
    var select = document.getElementById('select_reading_mode');

    if (select) {
        var index = select.selectedIndex;
        var option = select.options[index];

        var reading_mode = option.value;

        switch(reading_mode) {
            case 'webtoon': {
                register_global_event_listener_for_reader();
                load_visible_page_webtoon_format();
            } break;

            case 'single_page': {
                unregister_global_event_listener_for_reader();
                load_first_page_single_page_format();
            } break;
        }
    }
}

function switch_reading_mode(select) {
    var index = select.selectedIndex;
    var option = select.options[index];

    var manga = select.getAttribute('data-manga');
    var user = select.getAttribute('data-user');
    var reading_mode = option.value;
    
    var location = window.location.href.split('?')[0];


    var data = {
        manga: manga,
        user: user,
        reading_mode: reading_mode
    };


    lock_module_loading();

    $.ajax({
        method: 'GET',
        url: '/manga_site/set_manga_reading_mode',
        data: data,
        success: function(response) {
            if(response.status == 'success') {
                window.location.assign(window.location.href);
            } else {
                unlock_module_loading();
                notify_with_popup(select, response.description);
            }
        },
        error: function(response) {
            unlock_module_loading();
            notify_with_popup(select, "Sorry we couldn't update your reading preference. Something went wrong. Reload the page and try again.");
        }
    });

    //var url = location + '?mode=' + reading_mode;

    //window.location.assign(url);
}