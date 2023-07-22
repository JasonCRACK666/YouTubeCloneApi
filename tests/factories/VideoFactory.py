import factory

from apps.video.models import Video

from tests.factories.ChannelFactory import ChannelFactory


class VideoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Video

    title = factory.Faker('pystr', max_chars=45)
    video_url = factory.Faker('url')
    thumbnail = factory.Faker('image_url')
    description = factory.Faker('paragraph')
    channel = factory.SubFactory(ChannelFactory)