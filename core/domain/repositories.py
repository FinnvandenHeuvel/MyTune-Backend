from core.domain.models import Review


def create_review(*, user, data):
    return Review.objects.create(user=user, **data)


def delete_review(*, review):
    review.delete()
