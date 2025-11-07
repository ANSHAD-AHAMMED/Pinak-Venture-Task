from rest_framework import serializers

class JobSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(source="Job Title")
    location = serializers.CharField(source="Location")
    post_date = serializers.CharField(source="Post/Publish Date")
    link = serializers.CharField(source="Link")
