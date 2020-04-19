var manga_point_reading_mode = 'webtoon';

function switch_reading_mode(select) {
    var index = select.selectedIndex;
    var option = select.options[index];

    switch(option.value) {
        case 'webtoon': {
            manga_point_reading_mode = 'webtoon';
        } break;

        case 'single_page': {
            manga_point_reading_mode = 'single_page';
        } break;
    };
}

function get_next_page() {
    switch(manga_point_reading_mode) {
        case 'webtoon': {

        } break;

        case 'single_page': {

        } break;
    };
}


function get_previous_page() {
    switch(manga_point_reading_mode) {
        case 'webtoon': {

        } break;

        case 'single_page': {

        } break;
    };
}