function get_next_manga_page(section_id, pager_id, page_counter_id, order_by, items_per_page) {
    var num_pages_id = section_id + '_num_pages';
    var num_pages = document.getElementById(num_pages_id);
    num_pages = num_pages.innerHTML.trim();
    var current_page_number = document.getElementById(pager_id).value.trim();

    if (num_pages == current_page_number) {
        return;
    }
    
    var request_parameters = {
        order_by: order_by,
        items_per_page: items_per_page,
        section_id: section_id,
    };

    current_page_number++;

    var parameters = {
        page_number: current_page_number,
        section_id: section_id,
        pager_id: pager_id,
        page_counter_id: page_counter_id,
        force_overwrite: true,
        apply_filters: true,
        apply_order: true,
    };

    get_manga_page(request_parameters, parameters);
}

function get_previous_manga_page(section_id, pager_id, page_counter_id, order_by, items_per_page) {
    var current_page_number = document.getElementById(pager_id).value.trim();

    if (current_page_number == '1') {
        return;
    }
    
    var request_parameters = {
        order_by: order_by,
        items_per_page: items_per_page,
        section_id: section_id,
    };

    current_page_number--;
    
    var parameters = {
        page_number: current_page_number,
        section_id: section_id,
        pager_id: pager_id,
        page_counter_id: page_counter_id,
        force_overwrite: true,
        apply_filters: true,
        apply_order: true,
    };

    get_manga_page(request_parameters, parameters);
}

function get_selected_manga_page(section_id, pager_id, page_counter_id, order_by, items_per_page) {
    var current_page_number = document.getElementById(pager_id).value.trim();

    var request_parameters = {
        order_by: order_by,
        items_per_page: items_per_page,
        section_id: section_id
    };

    var parameters = {
        page_number: current_page_number,
        section_id: section_id,
        pager_id: pager_id,
        page_counter_id: page_counter_id,
        force_overwrite: true,
        apply_filters: true,
        apply_order: true,
    };

    get_manga_page(request_parameters, parameters);
}

function get_manga_page(request_parameters, parameters) {
    
    if (parameters.apply_filters) {
        var filters = gather_active_filters();

        request_parameters.tags = JSON.stringify(filters.tags);
        request_parameters.authors = JSON.stringify(filters.authors);
    }

    if (parameters.apply_order) {
        request_parameters.order_by = get_ordering_rule();
    }

    var page_id = parameters.section_id + "_page_" + parameters.page_number; 
    var carousel_id = parameters.section_id + '_carousel';
    var pager = document.getElementById(parameters.pager_id);
    var page = document.getElementById(page_id);
    var last_page = document.getElementById(parameters.page_counter_id);
    var section = document.getElementById(parameters.section_id);
    var page_number = parameters.page_number;

    if (!parameters.force_overwrite) {
        if (page) {
            var offset = $('#' + carousel_id).offset();
            $('html, body').animate({
                scrollTop: offset.top - 60,
                scrollLeft: offset.left
            }, 1000);
    
            var index = Array.prototype.indexOf.call(section.children, page);
            $('#' + carousel_id).carousel(index);
    
            pager.selectedIndex = page_number - 1;
            
            return;
        }
    }

    lock_module_loading();
    
    $.ajax({
        type: "GET",
        url: "/manga_page_json/" + page_number,
        data: request_parameters,
        success: function(response) {
            unlock_module_loading();

            var num_pages = response.num_pages;
            var mangas = response.mangas;

            if (mangas.length > 0) {
                clear_div(section);
            } else {
                alert("No manga found by that criteria.");
                return;
            }

            var i = 0, l = mangas.length;
            
            page = document.createElement('div');
            page.className = 'carousel-item' + (parameters.force_overwrite ? ' active' : '');
            
            var page_inner = document.createElement('div');
            page_inner.className = 'page d-flex row w-100 mx-0';
            page.id = page_id;
            
            for(; i < l; i++) {
                
                var manga = mangas[i];
                var manga_div = create_manga_card(manga);
                
                page_inner.appendChild(manga_div);
            }
            
            page.appendChild(page_inner);
            section.appendChild(page);
            
            var offset = $('#' + carousel_id).offset();
            $('html, body').animate({
                scrollTop: offset.top - 60,
                scrollLeft: offset.left
            }, 1000);

            var index = Array.prototype.indexOf.call(section.children, page);
            $('#' + carousel_id).carousel(index);
            
            pager.selectedIndex = page_number - 1;
            last_page.innerHTML = num_pages;

            $.each($('[data-action="get_bookmarked"]'), function(index, element) {
                var manga_id = element.getAttribute('data-manga');

                get_bookmarked_chapter(element, manga_id);
            });

            $.each($('[data-action="get_last_read"]'), function(index, element) {
                var manga_id = element.getAttribute('data-manga');

                get_last_read_chapter(element, manga_id);
            });
        },
        error: function(response) {
            unlock_module_loading();
            alert(response);
        }
    });
}

function search_manga(input_element) {
    var search_term = input_element.value;
    
    if (search_term.length < 3) {
        return;
    }
    
    var data = {
        search_term: search_term
    };
    
    var func = function(response) {
        update_search_results(response);   
    };
    
    fetch_manga_json(data);
}

function fetch_manga_json(data, func) {
    $.ajax({
        type: "GET",
        url: "/manga_list_json",
        data: data,
        success: function(response) {
            var manga_list = JSON.parse(response);
            var results_div = document.getElementById("search_results");
            clear_div(results_div);
            var i = 0, l = manga_list.length;
            
            for(; i < l; i++) {
                var manga = manga_list[i];
                var div = document.createElement('div');
                var link = document.createElement('a');
                
                link.href = '/manga/manga/' + manga.pk;
                link.className = 'nav-link search_result bg-white';
                link.innerHTML = manga.fields.manga_name;
                
                div.appendChild(link);
                results_div.appendChild(div);
            }
        }
    });
}
