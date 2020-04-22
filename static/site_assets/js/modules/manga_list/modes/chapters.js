function fetch_selected_chapter(manga_id, select_input) {
    location.assign('/manga/' + manga_id + '/chapters/' + select_input.options[select_input.selectedIndex].value);
}

function fetch_previous_chapter(manga_id) {
    var select = document.getElementById('chapter-select-bottom');
    current_chapter = select.selectedIndex;

    if(current_chapter < select.length - 1) {
        index_to = parseInt(current_chapter) + 1;
        chapter_to = select.options[index_to].value;
        window.location.assign('/manga/' + manga_id + '/chapters/' + chapter_to);
    }
}

function fetch_next_chapter(manga_id) {
    var select = document.getElementById('chapter-select-bottom');
    current_chapter = select.selectedIndex;

    if(current_chapter > 0) {
        index_to = parseInt(current_chapter) - 1;
        chapter_to = select.options[index_to].value;
        window.location.assign('/manga/' + manga_id + '/chapters/' + chapter_to);
    }
}