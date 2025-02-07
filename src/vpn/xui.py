from typing import List
from py3xui import AsyncApi, Inbound, Client
import vpn.models
from django.conf import settings
from asgiref.sync import sync_to_async
import base64

@sync_to_async
def save_collected_data(inbounds: List[Inbound]):
    try:
        for inbound in inbounds:
            sniffing, _ = vpn.models.Sniffing.objects.update_or_create(
                defaults={
                    'enabled': inbound.sniffing.enabled,
                    'dest_override': inbound.sniffing.dest_override,
                    'metadata_only': inbound.sniffing.metadata_only,
                    'route_only': inbound.sniffing.route_only,
                }
            )

            stream_settings, _ = vpn.models.StreamSettings.objects.update_or_create(
                security=inbound.stream_settings.security,
                network=inbound.stream_settings.network,
                defaults={
                    'tcp_settings': inbound.stream_settings.tcp_settings,
                    'kcp_settings': inbound.stream_settings.kcp_settings,
                    'external_proxy': inbound.stream_settings.external_proxy,
                    'reality_settings': inbound.stream_settings.reality_settings,
                    'xtls_settings': inbound.stream_settings.xtls_settings,
                    'tls_settings': inbound.stream_settings.tls_settings,
                }
            )

            settings, _ = vpn.models.Settings.objects.update_or_create(
                defaults={
                    'decryption': inbound.settings.decryption,
                    'fallbacks': inbound.settings.fallbacks,
                }
            )

            clients = []
            for client in inbound.settings.clients:
                client_obj, _ = vpn.models.Client.objects.update_or_create(
                    email=client.email,
                    defaults={
                        'enable': client.enable,
                        'password': client.password,
                        'method': client.method,
                        'sub_id': client.sub_id,
                        'tg_id': client.tg_id,
                        'total_gb': client.total_gb,
                    }
                )
                clients.append(client_obj)
            
            settings.clients.set(clients)

            vpn.models.Inbound.objects.update_or_create(
                port=inbound.port,
                defaults={
                    'enable': inbound.enable,
                    'protocol': inbound.protocol,
                    'settings': settings,
                    'stream_settings': stream_settings,
                    'sniffing': sniffing,
                    'remark': inbound.remark,
                    'up': inbound.up,
                    'down': inbound.down,
                    'total': inbound.total,
                    'expiry_time': inbound.expiry_time,
                    'tag': inbound.tag,
                }
            )
        return "Данные успешно собраны и обновлены"
    except Exception as e:
        return f"Ошибка: {e}"

async def auth():
    api = AsyncApi(f'https://{settings.IP}:{settings.PORT}/openssl/', settings.XUI_LOGIN, settings.XUI_PASS, use_tls_verify=False)
    
    await api.login()

    return api

async def get_inbounds():
    api = await auth()
    inbounds: List[Inbound] = await api.inbound.get_list()

    return inbounds


async def save_data():
    inbounds = await get_inbounds()
    result = await save_collected_data(inbounds)

    return result


def get_connection_string(inbound: vpn.models.Inbound, client: vpn.models.Client) -> str:
    """Формирует строку подключения для клиента."""
    
    if not inbound or not client:
        raise ValueError("Не переданы inbound или client")

    method = client.method
    password = client.password
    client_email = client.email

    method_password = f"{method}:{password}"
    method_password_base64 = base64.urlsafe_b64encode(method_password.encode()).decode().strip("=")

    connection_string = f"ss://{method_password_base64}@{settings.IP}:{inbound.port}"

    params = "?type=tcp"
    connection_string += f"{params}#{inbound.remark}:{client_email}"

    return connection_string
