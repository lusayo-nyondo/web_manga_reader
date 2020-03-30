function submit_rating(button, manga_id, rating) {
    //lock_rating_span(manga_id);

    $.ajax({
        url: '/manga_site/submit_rating',
        data: {
            manga_id: manga_id,
            rating: rating
        },
        success: function(response) {
            if (response.status == "success") {
                var rating = response.rating;
                var valid_ratings = response.valid_ratings;

                update_rating(manga_id, rating, valid_ratings);
            } else if (response.status == "failed") {
                notify_with_popup(button, response.description);
            } else {
                console.log(response);
            }
        },
        failure: function(response) {
            console.log(response);
        }
    });
}

function update_rating(manga_id, rating, valid_ratings) {
    var rating_span = create_rating_span(manga_id, rating, valid_ratings);
    var current_rating_span = document.getElementById('manga_' + manga_id + '_rating_span');

    var parent = current_rating_span.parentNode;
    parent.removeChild(current_rating_span);
    parent.appendChild(rating_span);
}

function create_rating_span(manga_id, rating, valid_ratings) {
    var rating_span = document.createElement("span");
    rating_span.id = "manga_" + manga_id + "_rating_span";
    rating_span.className = "text-warning position-relative";

    var i = 0, l = valid_ratings.length;

    for(; i < l; i++) {
        var rating_star = create_rating_star(manga_id, rating, valid_ratings[i]);
        rating_span.appendChild(rating_star);
    }

    return rating_span;
}

function create_rating_star(manga_id, rating, current_star) {
    var rating_star = document.createElement('span');
    rating_star.className = "rating_star";

    var button = document.createElement("button");
    button.type = "button";
    button.className = "btn text-warning";
    
    button.setAttribute("data-action", "rate_manga");
    button.setAttribute("data-manga", manga_id);
    button.setAttribute("data-value", current_star);

    var icon = document.createElement("i");
    icon.className = current_star <= rating ? "fas fa-star"  : "far fa-star";

    button.appendChild(icon);
    button.onclick = function(event) {
        submit_rating(event.currentTarget, manga_id, current_star);
    };

    rating_star.appendChild(button);

    return rating_star;
}

function lock_rating_span(manga_id) {
    var rating_span_id = "manga_" + manga_id + "_rating_span";
    var rating_span = document.getElementById(rating_span_id);

    var loading_overlay = create_loading_overlay();

    rating_span.appendChild(loading_overlay);
}