function get_last_authors_page() {
    var last_page_id = 'last_authors_page';
    var last_page = document.getElementById(last_page_id).innerHTML.trim();

    var data = {
        page_number: last_page,
        items_per_page: 15
    };

    get_authors_page(data);
}

function get_last_tags_page() {
    var last_page_id = 'last_tags_page';
    var last_page = document.getElementById(last_page_id).innerHTML.trim();

    var data = {
        page_number: last_page,
        items_per_page: 15
    };

    get_tags_page(data);
}

function get_previous_authors_page(items_per_page) {
    var current_page_id = "current_authors_page";
    var current_page = document.getElementById(current_page_id).value.trim();

    if (current_page == '1') {
        return;
    }

    --current_page;

    var data = {
        page_number: current_page,
        items_per_page: items_per_page,
    };

    get_authors_page(data);
}

function get_next_authors_page(items_per_page) {
    var current_page_id = "current_authors_page";
    var current_page = document.getElementById(current_page_id).value.trim();
    var last_page_id = "last_authors_page";
    var last_page = document.getElementById(last_page_id).innerHTML.trim();

    if (current_page == last_page) {
        return;
    }

    ++current_page;

    var data = {
        page_number: current_page,
        items_per_page: items_per_page,
    };

    get_authors_page(data);
}

function get_authors_page(data) {
    var page_id = 'authors_page_' + data.page_number;
    var authors_section_id = 'author_filters_carousel';
    var authors_section = document.getElementById(authors_section_id);
    var carousel_item = document.getElementById(page_id);

    if (carousel_item) {
        var index = Array.prototype.indexOf.call(authors_section.children, carousel_item);
        $('#authors_carousel').carousel(index);
        document.getElementById('current_authors_page').value = data.page_number;

        return;
    }

    $.ajax({
        type: 'GET',
        url: '/author_page_json/' + data.page_number,
        data: data,
        success: function(response) {
            var i = 0, l = response.length;
            var carousel_item_div = document.createElement('div');
            carousel_item_div.className = 'carousel-item';
            carousel_item_div.id = page_id;

            var page_div = document.createElement('div');
            page_div.className = 'page row mx-0';

            for(; i < l; i++) {
                var author = response[i];
                var author_filter = create_filter_item('author', author.pk, author.fields.author_name);

                page_div.appendChild(author_filter);
            }

            carousel_item_div.appendChild(page_div);
            authors_section.appendChild(carousel_item_div);

            var index = Array.prototype.indexOf.call(authors_section.children, document.getElementById(page_id));
            $('#authors_carousel').carousel(index);
            document.getElementById('current_authors_page').selectedIndex = data.page_number - 1;
        }
    });
}

function get_previous_tags_page(items_per_page) {
    var current_page_id = "current_tags_page";
    var current_page = document.getElementById(current_page_id).value.trim();

    if (current_page == '1') {
        return;
    }

    --current_page;

    var data = {
        page_number: current_page,
        items_per_page: items_per_page,
    };

    get_tags_page(data);
}

function get_next_tags_page(items_per_page) {
    var current_page_id = "current_tags_page";
    var current_page = document.getElementById(current_page_id).value.trim();
    var last_page_id = "last_tags_page";
    var last_page = document.getElementById(last_page_id).innerHTML.trim();

    if (current_page == last_page) {
        return;
    }

    ++current_page;

    var data = {
        page_number: current_page,
        items_per_page: items_per_page,
    };

    get_tags_page(data);
}

function get_tags_page(data) {
    var page_id = 'tags_page_' + data.page_number;
    var tags_section_id = 'tag_filters_carousel';
    var tags_section = document.getElementById(tags_section_id);

    var carousel_item = document.getElementById(page_id);

    if (carousel_item) {
        var index = Array.prototype.indexOf.call(tags_section.children, document.getElementById(page_id));
        $('#tags_carousel').carousel(index);
        document.getElementById('current_tags_page').selectedIndex = data.page_number - 1;

        return;
    }

    $.ajax({
        type: 'GET',
        url: '/tag_page_json/' + data.page_number,
        data: data,
        success: function(response) {
            var i = 0, l = response.length;

            var carousel_item_div = document.createElement('div');
            carousel_item_div.className = 'carousel-item';
            carousel_item_div.id = page_id;

            var page_div = document.createElement('div');
            page_div.className = 'page row mx-0';

            for(; i < l; i++) {
                var tag = response[i];
                var tag_filter = create_filter_item('tag', tag.pk, tag.fields.tag_name);

                page_div.appendChild(tag_filter);
            }

            carousel_item_div.append(page_div);
            tags_section.appendChild(carousel_item_div);

            var index = Array.prototype.indexOf.call(tags_section.children, document.getElementById(page_id));
            $('#tags_carousel').carousel(index);
            document.getElementById('current_tags_page').selectedIndex = data.page_number - 1;
        }
    });
}

function set_carousel_child_visible(carousel, child) {
    var child_position = Array.indexOf.call(carousel.children, child);
    $('#' + carousel_id).carousel(child_position);
}

function get_selected_page(select, items_per_page, calling_function) {
    var data = {
        page_number: select.value.trim(),
        items_per_page: items_per_page,
    };

    calling_function(data);
}

function toggle_global_filter(checkbox) {

    var params = checkbox.name.split('_');

    if (params.length != 2) {
        return;
    }

    var filter_type = params[0];
    var filter_value = params[1];
    var display_name = checkbox.getAttribute('data-display-value');

    var data = {
        filter_state: checkbox.checked,
        filter_type: filter_type,
        filter_value: filter_value,
        display_name: display_name,
    };

    toggle_filter(data);
    update_active_filters_count();
}

function toggle_filter(data) {
    var filters_div_id = 'active_' + data.filter_type + '_filters_list';
    var filters_div = document.getElementById(filters_div_id);

    var item_id = 'active_' + data.filter_type + '_' + data.filter_value;
    var item_div = document.getElementById(item_id);

    var filter_state = data.filter_state;

    if (item_div) {
        // TODO: Change item state here for inclusive, and exclusive filters.
        if (filter_state == false) {
            filters_div.removeChild(item_div);
        }
    } else {
        add_active_filter(item_id, data, filters_div);
    }
}

function add_active_filter(filter_item_id, filter_item_data, parent_element) {
    var filter_item_span = document.createElement('span');

    filter_item_span.id = filter_item_id;
    filter_item_span.className = 'active-filter-item badge badge-dark p-2 m-2 d-inline-block ' + filter_item_data.filter_type;
    filter_item_span.name = filter_item_data.filter_value;
    filter_item_span.innerHTML = filter_item_data.display_name;

    parent_element.appendChild(filter_item_span);
}

function update_active_filters_count() {
    var filters_count = get_active_filters_count();

    if (filters_count > 0) {
        document.getElementById('active-filters-stub').classList.add('d-none');
        show_active_filters();
    } else {
        document.getElementById('active-filters-stub').classList.remove('d-none');
    }

    document.getElementById('active_filters').innerHTML = filters_count;
}

function get_active_filters_count() {
    var count = document.getElementById('active_tag_filters_list').getElementsByClassName('active-filter-item').length +
        document.getElementById('active_author_filters_list').getElementsByClassName('active-filter-item').length;

    return count;
}

function show_active_filters() {
    if (get_active_filters_count() > 0) {
        document.getElementById('active_filters_list').classList.add('show');
    }
}

function toggle_filters_menu(button) {
    button.classList.toggle('active');
    show_active_filters();
}

function apply_active_filters(section_id, items_per_page) {
    var filters = gather_active_filters();
    filter_manga_using_filters(filters.authors, filters.tags, section_id, items_per_page);
    close_filters_menu();
}

function close_filters_menu() {
    var filters_menu = document.getElementById('filters-menu');
    filters_menu.classList.remove('show');
}

function gather_active_filters() {
    var tag_elements = document.getElementById('active_tag_filters_list').getElementsByClassName('active-filter-item');
    var i = 0, l = tag_elements.length;
    var tags = {
        tags: [],
    };

    for (; i < l; i++) {
        tags.tags.push(tag_elements[i].id.split('_')[2]);
    }

    var author_elements = document.getElementById('active_author_filters_list').getElementsByClassName('active-filter-item');
    var authors = {
        authors: []
    };
    i = 0; l = author_elements.length;

    for (; i < l; i++) {
        authors.authors.push(author_elements[i].id.split('_')[2]);
    }

    var filters = {
        authors: authors,
        tags: tags
    };

    return filters;
}

function filter_manga_using_filters(authors, tags, section_id, items_per_page) {
    var order_by = get_ordering_rule();

    var data = {
        order_by: order_by,
        items_per_page: items_per_page,
        section_id: section_id,
    };

    var pager_id = section_id + '_current_page';
    var page_counter_id = section_id + '_num_pages';

    var parameters = {
        page_number: '1',
        section_id: section_id,
        pager_id: pager_id,
        page_counter_id: page_counter_id,
        force_overwrite: true,
        apply_filters: true,
        apply_order: true,
    };

    get_manga_page(data, parameters);
}

function get_ordering_rule() {
    var select = document.getElementById('select_ordering_rule');
    ordering_rule = select.value;

    return ordering_rule;
}

function apply_ordering_rule(section_id, items_per_page) {
    apply_active_filters(section_id, items_per_page);
}

function create_filter_item(item_type, item_id, item_text) {
    var filter_item = document.createElement('div');
    filter_item.className = 'custom-control custom-checkbox filter-item mx-0 col-6';

    var checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.className = 'custom-control-input';
    checkbox.id = item_type + '_' + item_id;
    checkbox.name = item_type + '_' + item_id;
    checkbox.setAttribute('data-display-value', item_text);

    checkbox.addEventListener('click', function(){
        toggle_global_filter(this);
    });

    var label = document.createElement('label');
    label.className = 'custom-control-label';
    label.setAttribute('for', item_type + '_' + item_id);

    var link = document.createElement('a');
    link.href = '/manga_list?' + item_type + '_id=' + item_id;
    link.class = 'd-inline-block';
    link.innerHTML = item_text;

    label.appendChild(link);

    filter_item.appendChild(checkbox);
    filter_item.appendChild(label);

    return filter_item;
}

function create_last_read_probing_element(manga_id) {
    var probe = document.createElement("p");
    probe.id = "last_read_chapter_probe_" + manga_id;
    probe.className = "card-text small my-0 manga-chapter mt-auto";

    var button = document.createElement("button");

    button.type = "button";
    button.id = "btn_manga_" + manga_id + "_last_read";
    button.className = "btn btn-link px-0 small manga-chapter";

    button.setAttribute('data-action', "get_last_read");
    button.setAttribute('data-manga', manga_id);

    var icon = document.createElement('i');
    icon.className = 'fa fa-history';

    var span = document.createElement('span');
    span.id = "span_manga_" + manga_id + "_last_read";

    var padding_left = document.createElement("span");
    padding_left.innerHTML = "&nbsp";

    var action = document.createElement("span");
    action.innerHTML = "Fetching your history";

    var padding_right = document.createElement("span");
    padding_right.innerHTML = "&nbsp";

    var spinner = document.createElement("i");
    spinner.className = "small spinner spinner-border spinner-border-sm";

    span.appendChild(padding_left);
    span.appendChild(action);
    span.appendChild(padding_right);
    span.appendChild(spinner);

    button.appendChild(icon);
    button.appendChild(span);

    probe.appendChild(button);

    return probe;
}

function create_bookmarked_probing_element(manga_id) {
    var probe = document.createElement("p");
    probe.id = "bookmarked_chapter_probe_" + manga_id;
    probe.className = "card-text small my-0 manga-chapter mt-auto";

    var button = document.createElement("button");

    button.type = "button";
    button.id = "btn_manga_" + manga_id + "_last_read";
    button.className = "btn btn-link px-0 small manga-chapter";

    button.setAttribute('data-action', "get_bookmarked");
    button.setAttribute('data-manga', manga_id);

    var icon = document.createElement('i');
    icon.className = 'fa fa-bookmark';

    var span = document.createElement('span');
    span.id = "span_manga_" + manga_id + "_bookmarked";

    var padding_left = document.createElement("span");
    padding_left.innerHTML = "&nbsp";

    var action = document.createElement("span");
    action.innerHTML = "Fetching bookmarks";

    var padding_right = document.createElement("span");
    padding_right.innerHTML = "&nbsp";

    var spinner = document.createElement("i");
    spinner.className = "small spinner spinner-border spinner-border-sm";

    span.appendChild(padding_left);
    span.appendChild(action);
    span.appendChild(padding_right);
    span.appendChild(spinner);

    button.appendChild(icon);
    button.appendChild(span);

    probe.appendChild(button);

    return probe;
}
