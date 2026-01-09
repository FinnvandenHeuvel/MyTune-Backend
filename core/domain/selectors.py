from core.domain.models import Review

def list_reviews(*, artist_id=None, album_id=None):
    qs = Review.objects.all().order_by("-created_at")
    if artist_id:
        qs = qs.filter(artist_id=artist_id)
    if album_id:
        qs = qs.filter(album_id=album_id)
    return qs

def list_my_reviews(*, user):
    return Review.objects.filter(user=user).order_by("-created_at")

def get_review_by_pk(*, pk):
    return Review.objects.filter(pk=pk).first()
