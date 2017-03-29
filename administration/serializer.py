from core.models import Course, CourseAuthor, Lesson, Unit
from core.serializers import VideoSerializer
from activities.serializers import ActivityImportExportSerializer
from course_material.serializers import CourseMaterialImportExportSerializer
from rest_framework import serializers


class CourseAuthorsExportSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='get_name')
    biography = serializers.ReadOnlyField(source='get_biography')
    picture = serializers.ReadOnlyField(source='get_picture_url')

    class Meta:
        model = CourseAuthor
        exclude = ('id', 'user', 'course',)


class CourseAuthorsImportSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseAuthor
        exclude = ('id', 'user', 'course',)


class UnitImportExportSerializer(serializers.ModelSerializer):
    video = VideoSerializer()
    activities = ActivityImportExportSerializer(many=True)

    class Meta:
        model = Unit
        exclude = ('id', 'lesson',)


class LessonImportExportSerializer(serializers.ModelSerializer):
    # units = UnitImportExportSerializer(many=True)

    class Meta:
        model = Lesson
        exclude = ('id', )


class CourseExportSerializer(serializers.ModelSerializer):
    lessons = LessonImportExportSerializer(many=True)
    course_authors = CourseAuthorsExportSerializer(many=True, read_only=True)
    intro_video = VideoSerializer()
    course_material = CourseMaterialImportExportSerializer()

    class Meta:
        model = Course
        fields = ('slug', 'name', 'intro_video', 'application', 'requirement', 'abstract', 'structure',
                  'workload', 'pronatec', 'status', 'thumbnail', 'home_thumbnail', 'home_position',
                  'start_date', 'home_published', 'course_authors', 'lessons', 'course_material',)


class CourseImportSerializer(serializers.ModelSerializer):
    lessons = LessonImportExportSerializer(many=True)
    # course_authors = CourseAuthorsImportSerializer(many=True)
    # intro_video = VideoSerializer()
    # # course_material = CourseMaterialImportExportSerializer()

    class Meta:
        nested_pk_field = 'course'
        nested_items = (('lessons', LessonImportExportSerializer), ) # 'course_authors', 'intro_video')
        model = Course
        fields = ('slug', 'name', 'application', 'requirement', 'abstract', 'structure',
                  'workload', 'pronatec', 'status', 'thumbnail', 'home_thumbnail', 'home_position',
                  'start_date', 'home_published', 'lessons', # 'course_authors', 'intro_video',
                  )

    def create(self, validated_data):
        nested = {}
        for nested_item, CurrentSerializer in self.Meta.nested_items:
            data = validated_data.pop(nested_item)
            nested[nested_item] = data

        default_object = self.Meta.model.objects.create(**validated_data)
        for key, value in nested.items():

            if isinstance(value, list):
                value = [value]

            for position, data in enumerate(value):
                data[self.Meta.nested_pk_field] = default_object.id
                item = CurrentSerializer.Meta.model(**data)
                item.save()

                print value

            if items.is_valid():
                items.save()

            # CurrentSerializer = self.fields[key]
            # if isinstance(CurrentSerializer, serializers.ListSerializer):
            #     CurrentSerializer = CurrentSerializer.child
            #
            # print type(CurrentSerializer)
            # print dir(CurrentSerializer)


            # Serializer = getattr(self, key)

        return default_object


        #
        # lessons_data = validated_data.pop('lessons')
        # course_authors_data = validated_data.pop('course_authors')
        # intro_video_data = validated_data.pop('intro_video')
        #
        # course = Course.objects.create(**validated_data)
        #
        # for key, lesson_data in enumerate(lessons_data):
        #     lessons_data[key]['course'] = course.id
        # lessons = LessonImportExportSerializer(data=lesson_data)
        # if lessons.is_valid():
        #     lessons.save()
        #
        # return course
