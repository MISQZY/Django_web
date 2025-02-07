from django.shortcuts import render, get_object_or_404
from .models import Inbound, Client, UserClient
from django.http import HttpResponseForbidden
from .xui import save_data, get_connection_string
from django.http import JsonResponse


def index(request):
    if not request.user.has_perm('vpn.view_inbound'):
        return HttpResponseForbidden("У вас недостаточно прав для этой страницы.")
    
    if request.user.is_staff:
        inbounds = Inbound.objects.all()
    else:
        user_clients = UserClient.objects.filter(user=request.user).values_list('client_id', flat=True)

        inbounds = Inbound.objects.filter(settings__clients__id__in=user_clients).distinct()
    return render(request, 'vpn/index.html', {"inbounds": inbounds})


def inbound(request, id):
    if not request.user.has_perm('vpn.view_client'):
        return HttpResponseForbidden("У вас недостаточно прав для этой страницы.")
    
    inbound_instance = get_object_or_404(Inbound, id=id)

    if request.user.is_staff:
        clients = inbound_instance.settings.clients.all()
    else:
        user_clients = UserClient.objects.filter(user=request.user).values_list('client_id', flat=True)
        clients = inbound_instance.settings.clients.filter(id__in=user_clients)
    return render(request, 'vpn/inbound.html', {"clients": clients})


def client(request, id):
    if not request.user.has_perm('vpn.view_client'):
        return HttpResponseForbidden("У вас недостаточно прав для этой страницы.")

    client = get_object_or_404(Client, id=id)

    return render(request, 'vpn/client.html', {"client": client})

async def collect_vpn_data(request):
    if request.method == 'POST':
        result = await save_data()
        return JsonResponse({'message': result})
    return JsonResponse({'message': 'Invalid request'}, status=400)

def collect(request):
    return render(request, 'vpn/collect_data.html')


def get_connection(request, client_id: int):
    """Возвращает строку подключения для клиента"""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Вы не авторизованы"}, status=403)

    client: Client = get_object_or_404(Client, id=client_id)

    try:
        inbound = client.settings_set.first().inbound
    
        connection_string = get_connection_string(inbound=inbound, client=client)

        return JsonResponse({"connection_string": connection_string})

    except Client.DoesNotExist:
        return JsonResponse({"error": "Клиент не найден"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)