from rest_framework import serializers

class IPResponseSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()
