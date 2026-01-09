from core.domain import selectors

def get_my_reviews(*, user):
    return selectors.list_my_reviews(user=user)
