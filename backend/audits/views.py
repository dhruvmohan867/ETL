from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogListView(APIView):
    def get(self, request):
        qs = AuditLog.objects.all()

        action = request.query_params.get('action')
        if action:
            qs = qs.filter(action=action)

        target_type = request.query_params.get('target_type')
        if target_type:
            qs = qs.filter(target_type=target_type)

        serializer = AuditLogSerializer(qs, many=True)
        return Response(serializer.data)
