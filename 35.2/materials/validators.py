import re
from rest_framework.serializers import ValidationError

class YoutubeValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = value.get(self.field)
        if tmp_val and 'youtube.com' not in tmp_val:
            raise ValidationError('Video link must be a YouTube link.')
