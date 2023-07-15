import requests
from rest_framework import viewsets,status
from rest_framework.response import Response
from .models import User, Department, Ticket
from .serializers import UserSerializer, DepartmentSerializer, TicketSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        subject = serializer.validated_data.get('subject')
        description = serializer.validated_data.get('body')

        # Integrate with Zendesk API
        zendesk_ticket_id = self.create_ticket_in_zendesk(subject, description)

        if zendesk_ticket_id:
            # Handle successful ticket creation in Zendesk
            serializer.save(zendesk_ticket_id=zendesk_ticket_id)
        else:
            # Handle error case for ticket creation in Zendesk
            error_message = 'Error creating ticket in Zendesk'
            return Response(
                {'error': error_message},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def create_ticket_in_zendesk(self, subject, description):
        zendesk_api_url = 'https://peerxp3621.zendesk.com/api/v2/tickets.json'
        zendesk_username = 'PeerXP'
        zendesk_token = 'ytAkYBfSpvJgEYoJ6WyUXutQeccmzLH8ENikzIm0G'

        payload = {
            'ticket': {
                'subject': subject,
                'description': description
            }
        }

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(
            zendesk_api_url,
            json=payload,
            auth=(zendesk_username, zendesk_token),
            headers=headers
        )

        if response.status_code == 201:
            ticket_data = response.json()
            ticket_id = ticket_data['ticket']['id']
            return ticket_id
        else:
            # Handle error case
            return None
