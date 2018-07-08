from entrances.models import Entrance


def attach_entrance(request):
    filtered_entrance = None
    if 'entrance__id__exact' in request.GET:
        try:
            filtered_entrance = Entrance.objects.get(pk=request.GET.get('entrance__id__exact'))
        except:
            pass
    return {'filtered_entrance': filtered_entrance}
