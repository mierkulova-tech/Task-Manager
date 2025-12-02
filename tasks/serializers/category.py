from rest_framework import serializers
from tasks.models import Category


class CategoryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating Category instances.

    Ensures category names are unique (case-insensitive).
    """

    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        """
        Validate that the category name is unique (case-insensitive).

        Works for both create (instance=None) and update (instance exists).
        """
        qs = Category.objects.filter(name__iexact=value)

        # CREATE (no instance yet)
        if self.instance is None:
            if qs.exists():
                raise serializers.ValidationError(
                    f"Category with this name '{value}' already exists."
                )

        # UPDATE (exclude the current instance)
        else:
            if qs.exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError(
                    f"Category with this name '{value}' already exists."
                )

        return value

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)