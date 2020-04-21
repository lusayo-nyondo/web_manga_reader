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
        };
    }
}