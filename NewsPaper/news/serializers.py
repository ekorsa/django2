from .models import *
from rest_framework import serializers


class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    # post_category = PostCategorySerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'post_type', 'rating', 'creation_date', 'author', 'post_category']

# class SClassSerializer(serializers.HyperlinkedModelSerializer):
#    class Meta:
#        model = SClass
#        fields = ['id', 'grade', ]
#
#
# class StudentSerializer(serializers.HyperlinkedModelSerializer):
#    class Meta:
#        model = Student
#        fields = ['id', 'name', ]
