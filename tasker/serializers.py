from rest_framework.serializers import ModelSerializer

from tasker.models import Task
# from habits.validators import (
#     RewardValidator,
#     RelatedHabitValidator,
#     DurationTimeValidator,
#     PleasantHabitValidator,
#     RegularityValidator,
# )


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        # validators = [
        #     RewardValidator(field1="reward", field2="related_habit"),
        #     RelatedHabitValidator(field="related_habit"),
        #     DurationTimeValidator(field="duration"),
        #     PleasantHabitValidator(field="is_pleasant"),
        #     RegularityValidator(field1="frequency_number", field2="frequency_unit"),
        # ]
