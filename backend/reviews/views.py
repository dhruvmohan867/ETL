from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from emissions.models import EmissionRecord
from audits.models import AuditLog
from .models import ReviewDecision
from .serializers import ReviewDecisionSerializer


class ReviewCreateView(APIView):
    def get(self, request):
        qs = ReviewDecision.objects.select_related('emission_record').all()
        serializer = ReviewDecisionSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewDecisionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        emission_record_id = serializer.validated_data['emission_record'].id
        decision = serializer.validated_data['decision']
        reviewer_name = serializer.validated_data.get('reviewer_name', 'anonymous')

        try:
            record = EmissionRecord.objects.get(id=emission_record_id)
        except EmissionRecord.DoesNotExist:
            return Response(
                {"error": "Emission record not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        review = serializer.save()

        record.status = decision
        record.save()

        AuditLog.objects.create(
            action=f'review_{decision}',
            target_type='emission_record',
            target_id=record.id,
            details={
                'reviewer': reviewer_name,
                'decision': decision,
                'notes': serializer.validated_data.get('notes', ''),
            },
            performed_by=reviewer_name,
        )

        return Response(ReviewDecisionSerializer(review).data, status=status.HTTP_201_CREATED)
