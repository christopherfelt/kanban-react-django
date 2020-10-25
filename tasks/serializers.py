from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.board_id = validated_data.get("board_id", instance.board_id)
        instance.list_id = validated_data.get("list_id", instance.list_id)
        instance.body = validated_data.get("body", instance.body)
        instance.creatorEmail = validated_data.get(
            "creatorEmail", instance.creatorEmail
        )
        instance.save()

        return instance
