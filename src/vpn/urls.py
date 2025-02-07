from django.urls import path

from vpn.views import *

urlpatterns = [
   path('', index, name='vpn'),
   path('inbound/<int:id>/', inbound, name='inbound'),
   path('client/<int:id>/', client, name='client'),
   path('get-connection/<int:client_id>/', get_connection, name='get_connection'),
   path('collect/', collect),
   path('run-auth-and-save/', collect_vpn_data, name='collect_vpn_data'),
]