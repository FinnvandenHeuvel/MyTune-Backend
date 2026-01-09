from core.domain import repositories, selectors


def get_reviews(*, artist_id=None, album_id=None):
    return selectors.list_reviews(artist_id=artist_id, album_id=album_id)


def create_new_review(*, user, validated_data):
    return repositories.create_review(user=user, data=validated_data)


def delete_review_as_admin(*, user, pk):
    if not (user.is_staff or user.is_superuser):
        return (None, "Not allowed")

    review = selectors.get_review_by_pk(pk=pk)
    if not review:
        return (None, "Not found")

    repositories.delete_review(review=review)
    return (True, None)
