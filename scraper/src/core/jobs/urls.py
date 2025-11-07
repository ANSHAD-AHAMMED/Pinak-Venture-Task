from django.urls import path
from .views import list_jobs, retrieve_job

urlpatterns = [
    path("jobs/", list_jobs, name="jobs-list"),
    path("jobs/<int:job_id>/", retrieve_job, name="jobs-detail"),
]
