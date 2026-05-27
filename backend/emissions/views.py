from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from .models import EmissionRecord
from .serializers import EmissionRecordSerializer, UploadSerializer
from ingestion.models import Upload


class EmissionRecordListView(APIView):
    def get(self, request):
        qs = EmissionRecord.objects.select_related('company', 'upload').all()

        source_type = request.query_params.get('source_type')
        if source_type:
            qs = qs.filter(source_type=source_type)

        is_suspicious = request.query_params.get('is_suspicious')
        if is_suspicious is not None:
            qs = qs.filter(is_suspicious=is_suspicious.lower() == 'true')

        record_status = request.query_params.get('status')
        if record_status:
            qs = qs.filter(status=record_status)

        company_id = request.query_params.get('company_id')
        if company_id:
            qs = qs.filter(company_id=company_id)

        serializer = EmissionRecordSerializer(qs, many=True)
        return Response(serializer.data)


class DashboardStatsView(APIView):
    def get(self, request):
        records = EmissionRecord.objects.all()

        total = records.count()
        suspicious = records.filter(is_suspicious=True).count()
        approved = records.filter(status='approved').count()
        rejected = records.filter(status='rejected').count()
        pending = records.filter(status='pending').count()

        by_source = list(
            records.values('source_type')
            .annotate(
                total=Count('id'),
                suspicious=Count('id', filter=Q(is_suspicious=True)),
            )
            .order_by('source_type')
        )

        recent_uploads = Upload.objects.select_related('company').order_by('-created_at')[:10]
        uploads_data = UploadSerializer(recent_uploads, many=True).data

        return Response({
            'total_records': total,
            'suspicious_count': suspicious,
            'approved_count': approved,
            'rejected_count': rejected,
            'pending_count': pending,
            'by_source_type': by_source,
            'recent_uploads': uploads_data,
        })
