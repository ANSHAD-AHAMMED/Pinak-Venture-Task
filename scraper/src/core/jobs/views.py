import csv
import os
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import JobSerializer

CSV_PATH = getattr(settings, "CSV_PATH", "")

def read_jobs():
    if not os.path.exists(CSV_PATH):
        return []

    rows = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            row = {
                "id": i + 1,
                "Job Title": row.get("Job Title", ""),
                "Location": row.get("Location", ""),
                "Post/Publish Date": row.get("Post/Publish Date", ""),
                "Link": row.get("Link", ""),
            }
            rows.append(row)
    return rows

@api_view(["GET"])
def list_jobs(request):
    """
    GET /api/jobs/
    """
    jobs = read_jobs()
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def retrieve_job(request, job_id: int):
    """
    GET /api/jobs/<id>/
    """
    jobs = read_jobs()
    for j in jobs:
        if j["id"] == job_id:
            serializer = JobSerializer(j)
            return Response(serializer.data)
    return Response({"detail": "Not found"}, status=404)
