from api.models import Purchase


def purchases_processor(request):
    if request.user.is_authenticated:
        purchases_count = Purchase.objects.filter(
            user=request.user).count()
    else:
        purchases_count = 0
    return {'purchases_count': purchases_count}
