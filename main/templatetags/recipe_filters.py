from django import template
from api.models import Subscribe

register = template.Library()


@register.filter(name='is_follower')
def is_follower(request, profile):
    """Определяет подписан ли пользователь на автора."""

    if Subscribe.objects.filter(
            user=request.user, author=profile
    ).exists():
        return True

    return False
