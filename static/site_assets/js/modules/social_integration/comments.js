function fetch_comments() {
    var comments_section = $('[data-toggle="fetch_comments"]')[0];
    var current_page = comments_section.getAttribute('data-current-page');
    var total_pages = comments_section.getAttribute('data-total-pages');

    if (current_page > 0 && current_page == total_pages) {
        return;
    }

    var new_page = (current_page * 1) + 1;

    if (new_page == total_pages) {
        hide_load_more_comments_button();
    }

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
            register_reply_and_like_events();
        },
        error: function(response) {
            console.log(response);
        }
    });
}

function update_comments_section(response, comments_section) {
    var comments_count = document.getElementById('comments_count');
    comments_count.innerHTML = response.count;

    if ((response.number_of_pages * 1) <= 1) {
        hide_load_more_comments_button();
    }

    comments_section.setAttribute('data-current-page', response.page_number);
    comments_section.setAttribute('data-total-pages', response.number_of_pages);
    comments_section.setAttribute('data-page-end-reached', 'False');
    
    var posts = response.posts;
    var i = 0, l = posts.length;

    for(; i < l; i++) {
        var post = posts[i];
        var post_html = build_post_html(post, false);

        comments_section.appendChild(post_html);
    }
}

function build_post_html(post, is_reply) {
    var user = post.user[0];

    var div = document.createElement('div');
    div.className = 'post_div';

    var post_wrapper = document.createElement('div');
    post_wrapper.className = 'post_wrapper d-flex';
    post_wrapper.id = 'post_wrapper_' + post.pk;

    var profile_image_div = document.createElement('div');
    profile_image_div.className = 'profile_image_div';

    var profile_image = document.createElement('img');
    profile_image.className = 'profile_image';
    profile_image.src = user.fields.image_url;

    profile_image_div.appendChild(profile_image);

    var content_div = document.createElement('div');
    content_div.className = 'ml-2 post_content_div flex-fill';

    var poster_details_div = document.createElement('div');
    poster_details_div.className = 'poster_details';

    var created_on = document.createElement('small');
    created_on.className = 'posted_on';
    created_on.innerHTML = post.fields.created_on;

    var posted_by = document.createElement('span');
    posted_by.className = 'posted_by';
    posted_by.innerHTML = user.fields.username;

    var poster_details_splitter_span = document.createElement('span');
    poster_details_splitter_span.className = 'poster_details_splitter_span';
    poster_details_splitter_span.innerHTML = ' - ';

    poster_details_div.appendChild(created_on);
    poster_details_div.appendChild(poster_details_splitter_span);
    poster_details_div.appendChild(posted_by);

    var p = document.createElement('p');
    p.className = 'post';
    p.innerHTML = post.fields.text;

    var actions_div = create_post_actions_div(post, user, is_reply);

    content_div.appendChild(poster_details_div);
    content_div.appendChild(p);
    content_div.appendChild(actions_div);

    var replies_div = create_replies_div(post, user);

    post_wrapper.appendChild(profile_image_div);
    post_wrapper.appendChild(content_div);
    
    div.appendChild(post_wrapper);
    div.appendChild(replies_div);

    return div;
}

function create_replies_div(post, user) {

    var div = document.createElement('div');
    div.className = 'replies_div ml-5';

    var replies = post.replies;

    if (post.replies) {
        var i = 0, l = replies.length;

        for(; i < l; i++) {
            var reply_html = build_post_html(replies[i], true);
            div.appendChild(reply_html);
        }
    }

    return div;
}

function create_post_actions_div(post, user, is_reply) {
    var actions_div = document.createElement('p');
    actions_div.className = 'post_actions';

    var counter_id = 'likes_count_post_' + post.pk;

    var like = document.createElement('button');
    like.id = 'btn_like_post_' + post.pk;
    like.className = 'btn btn-link';

    var like_message_span_id = 'btn_like_post_span_' + post.pk;

    var like_message_span = document.createElement('span');
    like_message_span.id = like_message_span_id;
    like_message_span.innerHTML = post.user_likes_post ==  true ? 'Unlike' : 'Like';

    like.setAttribute('data-action', 'like_post');
    like.setAttribute('data-post', post.pk);
    like.setAttribute('data-user', user.pk);
    like.setAttribute('data-counter', counter_id);
    like.setAttribute('data-like-message-span', like_message_span_id);

    var left_bracket = document.createElement('span');
    left_bracket.innerHTML = '(';

    var right_bracket = document.createElement('span');
    right_bracket.innerHTML = ')';

    like.appendChild(like_message_span);

    var likes = document.createElement('span');
    likes.className = 'btn btn-link';

    var count = document.createElement('span');
    count.innerHTML = post.likes.length;
    count.id = counter_id;

    likes.appendChild(left_bracket);
    likes.appendChild(count);
    likes.appendChild(right_bracket);

    if(!is_reply) {
        var reply = document.createElement('button');
        reply.className = 'btn btn-link';
        reply.innerHTML = 'Reply';

        reply.setAttribute('data-action', 'add_reply');
        reply.setAttribute('data-post', post.pk);
        reply.setAttribute('data-user', user.pk);
        reply.setAttribute('data-summernote-id', 'add_reply');
        
        actions_div.appendChild(reply);
    }

    actions_div.appendChild(like);
    actions_div.appendChild(likes);

    return actions_div;
}

function add_post(source_element) {
    var summer_note_id = source_element.getAttribute('data-source-element-id');
    var text = $('#' + summer_note_id).summernote('code');
    var csrf_token = source_element.getAttribute('data-csrf-token');

    var current_location = window.location.href.split('?')[0].split('#')[0];
    var url = current_location;

    var data = {
        'location': url,
        'post': text,
    };

    var headers = {
        'X-CSRFToken': csrf_token,
    }

    $.ajax({
        url: '/social_integration/post_comment',
        method: 'POST',
        headers: headers,
        data: data,
        success: function(response) {
            switch(response.status) {
                case 'success': {
                    reset_comment_section();
                    fetch_comments();
                    $('#' + summer_note_id).summernote('reset');
                    $('#add_comment_modal').modal('hide');
                } break;

                case 'failed': {
                    notify_with_popup(source_element, response.description);
                } break;
            }
        },
        error: function(response) {
            console.log(response);
        }
    });
}

function load_comments_on_demand() {
    var comments_section = document.getElementById('comments_section');

    if(!comments_section) {
        return;
    }
    
    var page_number = comments_section.getAttribute('data-current-page');

    var scroll_event_processed = comments_section.getAttribute('data-scroll-event-processed');

    if (scroll_event_processed == 'True') {
        return;
    }

    if (parseInt(page_number) == -1) {
        if (is_element_in_view(comments_section)) {
            clear_div(comments_section);
            comments_section.setAttribute('data-scroll-event-processed', 'True');
            fetch_comments();    
        }
    }
}

function reset_comment_section() {
    var comments_section = document.getElementById('comments_section');

    clear_div(comments_section);
    
    var current_page = comments_section.getAttribute('data-current-page') * 1;
    current_page -= 1;

    comments_section.setAttribute('data-current-page', current_page);
}

function hide_load_more_comments_button() {
    var div = document.getElementById('fetch_comments_div');
    div.classList.add('d-none');
}

function like_post(button) {
    var url = '/social_integration/submit_like';
    
    var post = button.getAttribute('data-post');
    var user = button.getAttribute('data-user');

    var data = {
        post: post,
        user: user,
    };

    $.ajax({
        url: url,
        method: 'GET',
        data: data,
        success: function(response) {
            switch(response.status) {
                case 'success': {
                    update_number_of_likes(button, response.likes);
                } break;

                case 'failed': {
                    notify_with_popup(button, response.description);
                } break;
            }
        },
        error: function(response) {
            console.log(response);
        }
    });
}

function update_number_of_likes(button, likes) {
    var counter = button.getAttribute('data-counter');

    var counter_el = document.getElementById(counter);
    counter_el.innerHTML = likes;

    var like_message_span = document.getElementById(button.getAttribute('data-like-message-span'));

    like_message_span.innerHTML = like_message_span.innerHTML == 'Like' ? 'Unlike' : 'Like';
}

function reply_to_post(button) {
    var reply_button = document.getElementById('btn_add_reply');
    
    var post = button.getAttribute('data-post');
    var user = button.getAttribute('data-user');

    reply_button.setAttribute('data-post', post);
    reply_button.setAttribute('data-user', user);

    $('#add_reply_modal').modal('show');
}

function submit_reply(source_element) {
    var summer_note_id = source_element.getAttribute('data-source-element-id');
    var text = $('#' + summer_note_id).summernote('code');
    var csrf_token = source_element.getAttribute('data-csrf-token');
    var post = source_element.getAttribute('data-post');
    var user = source_element.getAttribute('data-user');

    var current_location = window.location.href.split('?')[0].split('#')[0];
    var url = current_location;

    var data = {
        'location': url,
        'reply': text,
        'post': post,
        'user': user,
    };

    var headers = {
        'X-CSRFToken': csrf_token,
    }

    $.ajax({
        url: '/social_integration/submit_reply',
        method: 'POST',
        headers: headers,
        data: data,
        success: function(response) {
            switch(response.status) {
                case 'success': {
                    reset_comment_section();
                    fetch_comments();
                    $('#' + summer_note_id).summernote('reset');
                    $('#add_reply_modal').modal('hide');
                } break;

                case 'failed': {
                    notify_with_popup(source_element, response.description);
                } break;
            }
        },
        error: function(response) {
            console.log(response);
        }
    });   
}