from user_manga_integration.models import UserMangaRating

def submit_rating(user, manga, rating):
    try:
        rating_obj = UserMangaRating.objects.get(
            user=user,
            manga=manga,
        )

        raise EnvironmentError('You have already rated this manga.')
    except UserMangaRating.DoesNotExist:    
        rating_obj = UserMangaRating.objects.get_or_create(
            user=user,
            manga=manga,
        )[0]

        rating_obj.rating = rating
        
        rating_obj.save()

