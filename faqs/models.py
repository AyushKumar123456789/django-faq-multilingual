from django.db import models
from ckeditor.fields import RichTextField
import googletrans
from googletrans import Translator

class FAQ(models.Model):
    question = models.TextField()  # English by default
    answer = RichTextField()

    question_hi = models.TextField(blank=True, null=True)
    question_bn = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"FAQ: {self.question[:30]}"

    def save(self, *args, **kwargs):
        translator = Translator()

        # Auto-translate question to Hindi if not already set
        if not self.question_hi and self.question:
            try:
                self.question_hi = translator.translate(self.question, src='en', dest='hi').text
            except Exception:
                self.question_hi = None

        # Auto-translate question to Bengali if not already set
        if not self.question_bn and self.question:
            try:
                self.question_bn = translator.translate(self.question, src='en', dest='bn').text
            except Exception:
                self.question_bn = None

        super().save(*args, **kwargs)

    def get_question(self, lang='en'):
        """
        Returns question text in the requested language if available.
        Fallback to English if no translation found.
        """
        if lang == 'hi' and self.question_hi:
            return self.question_hi
        elif lang == 'bn' and self.question_bn:
            return self.question_bn
        return self.question
