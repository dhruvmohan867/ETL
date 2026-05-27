from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from emissions.models import Company
from ingestion.models import Upload
from audits.models import AuditLog
from .services.sap_parser import SAPParserService
from .services.utility_parser import UtilityParserService
from .services.travel_parser import TravelParserService


PARSER_MAP = {
    'sap_fuel': SAPParserService,
    'utility': UtilityParserService,
    'travel': TravelParserService,
}


class FileUploadView(APIView):
    def post(self, request, source_type):
        if source_type not in PARSER_MAP:
            return Response(
                {"error": f"Invalid source type: {source_type}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response(
                {"error": "No file provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        company_id = request.data.get('company_id')
        if company_id:
            try:
                company = Company.objects.get(id=company_id)
            except Company.DoesNotExist:
                return Response(
                    {"error": "Company not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            company, _ = Company.objects.get_or_create(name="Default Company")

        file_hash = Upload.compute_file_hash(file_obj)

        upload = Upload.objects.create(
            company=company,
            source_type=source_type,
            file_name=file_obj.name,
            file_hash=file_hash,
            status='processing',
        )

        try:
            parser_class = PARSER_MAP[source_type]
            parser = parser_class(file_obj, upload)
            count = parser.process()

            AuditLog.objects.create(
                action='upload',
                target_type='upload',
                target_id=upload.id,
                details={
                    'file_name': file_obj.name,
                    'source_type': source_type,
                    'row_count': upload.row_count,
                    'suspicious_count': upload.suspicious_count,
                },
            )

            return Response({
                "upload_id": upload.id,
                "file_name": file_obj.name,
                "rows_processed": count,
                "suspicious_count": upload.suspicious_count,
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            upload.status = 'failed'
            upload.save()
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
