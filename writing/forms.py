from django import forms

from .models import WritingQuestion


class CoachingDraftForm(forms.Form):
    coach_step = forms.IntegerField(min_value=1, max_value=3, widget=forms.HiddenInput())
    session_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    question_id = forms.IntegerField(widget=forms.HiddenInput())
    level = forms.IntegerField(min_value=1, max_value=3, widget=forms.HiddenInput())
    question_type = forms.ChoiceField(
        choices=WritingQuestion.TYPE_CHOICES,
        widget=forms.HiddenInput(),
    )
    answer = forms.CharField(
        label="Your writing",
        widget=forms.Textarea(
            attrs={
                "rows": 14,
                "class": "input input--textarea",
                "id": "essay-answer",
                "spellcheck": "true",
            }
        ),
        strip=True,
    )

    def __init__(self, *args, min_answer_len: int = 40, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["answer"].min_length = min_answer_len


class ParaphraseForm(forms.Form):
    text = forms.CharField(
        label="Your sentences or paragraph",
        widget=forms.Textarea(
            attrs={
                "rows": 10,
                "class": "input input--textarea",
                "id": "paraphrase-text",
                "spellcheck": "true",
            }
        ),
        min_length=15,
        strip=True,
    )
