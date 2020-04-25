function fetch_comments() {
    var comments_section = $('[data-toggle="fetch_comments"]')[0];
    var current_page = comments_section.getAttribute('data-current-page');

    var current_location = window.location.href.split('?')[0].split('#')[0];
    var url = current_location;
    
    var data = {
        url: url,
        current_page: current_page,
    };
    
    $.ajax({
        url: '/social_integration/fetch_comments',
        method: 'GET',
        data: data,
        success: function(response) {
            update_comments_section(response, comments_section);
        },
        error: function(response) {

        }
    });
}

function update_comments_section(response, comments_section) {
    clear_div(comments_section);
    var posts = response.posts;
    var i = 0, l = posts.length;

    for(; i < l; i++) {
        var post = posts[i];
        var post_html = build_post_html(post);

        comments_section.appendChild(post_html);
    }
}

function build_post_html(post) {
    var p = document.createElement('p');
    p.innerHTML = post.fields.text;
    return p;
}

function add_post(source_element) {
    var text_area_id = source_element.getAttribute('data-source-element-id');
    var text_area = document.getElementById(text_area_id);
    
    var text = text_area.value;

    var current_location = window.location.href.split('?')[0].split('#')[0];
    var url = current_location;

    var data = {
        'location': url,
        'post': text
    };

    $.ajax({
        url: '/social_integration/post_comment',
        method: 'GET',
        data: data,
        success: function(response) {
            fetch_comments();
            $('#add_comment_modal').modal('hide');
        },
        error: function(response) {
            console.log(response);
        }
    });
}

function load_comments_on_demand() {
    var comments_section = document.getElementById('comments_section');
    
    if (is_element_in_view(comments_section)) {
        fetch_comments();
    }
}