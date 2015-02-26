from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from .models import Position, Event, Tag, Coffee, Review


class UserSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api-v1:user-detail')
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = get_user_model()
        fields = (User.USERNAME_FIELD, 'email', 'date_joined', 'password', 'last_login', 'is_active', 'url',)
        write_only_fields = ('password',)

    def create(self, validated_data):
        user = User(email=validated_data['email'], username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class TagSerializer(ModelSerializer):

    """
    Serializing all the Tags
    """

    url = HyperlinkedIdentityField(view_name='api-v1:tag-detail')
    user = UserSerializer(many=False, read_only=True)
    name = CharField(
        validators=[UniqueValidator(queryset=Tag.objects.all())]
    )

    class Meta:
        model = Tag
        fields = ('name', 'url', 'user')

    def validate_user(self):
        return self.context['request'].user


class EventSerializer(ModelSerializer):

    """
    Serializing all the Events
    """

    tags = TagSerializer(many=True, read_only=True)
    url = HyperlinkedIdentityField(view_name='api-v1:event-detail')

    class Meta:
        model = Event
        fields = ('name', 'url', 'tags')


class PositionSerializer(ModelSerializer):

    """
    Serializing all the Positions
    """

    #events = EventSerializer(many=True, read_only=True)
    url = HyperlinkedIdentityField(
        view_name='api-v1:position-detail')

    class Meta:
        model = Position
        fields = ('address', 'longitude', 'latitude', 'url', 'created_at',)


class ReviewSerializer(ModelSerializer):
    #coffee_id = serializers.PrimaryKeyRelatedField(read_only=True)
    #user = serializers.Field(source='user.username')
    #review = serializers.PrimaryKeyRelatedField()
    url = HyperlinkedIdentityField(view_name='api-v1:review-detail')
    user_url = HyperlinkedIdentityField(view_name='api-v1:user-detail')
    coffee_url = HyperlinkedIdentityField(view_name='api-v1:coffeehouses-detail')


    #owner = serializers.HiddenField(
     #   default=CurrentUserDefault()
    #)

    class Meta:
        model = Review
        fields = ('rating', 'description', 'url','coffee', 'coffee_url', 'user_url')

    def validate_user(self):
        return self.context['request'].user


class ReviewCoffee(ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Review
        fields = ('rating', 'description', 'created_at', 'user',)


class CoffeeSerializer(ModelSerializer):
    position = PositionSerializer(many=False, read_only=True)
    reviews = ReviewCoffee(many=True, read_only=True, source='review')
    url = HyperlinkedIdentityField(view_name='api-v1:coffeehouses-detail')
    tags = TagSerializer(many=True)

    class Meta:
        model = Coffee
        fields = ('name', 'rating', 'url', 'position', 'tags', 'reviews',)


class SimpleCoffeeSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api-v1:coffeehouses-detail')

    class Meta:
        model = Coffee
        fields = ('url',)


class NestedReviewSerializer(ModelSerializer):
    coffeehouse = SimpleCoffeeSerializer(source='coffee')
    url = HyperlinkedIdentityField(view_name='api-v1:review-detail')

    class Meta:
        model = Review
        fields = ('rating', 'description', 'url', 'coffeehouse', )


