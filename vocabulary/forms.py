from django import forms
from django.core.validators import FileExtensionValidator
from django.forms import ClearableFileInput

from boostingscore.models import UserProfile

from .models import CustomCard, CustomDeck

_MAX_IMAGE_BYTES = 2 * 1024 * 1024


class CustomCardForm(forms.ModelForm):
    deck = forms.ModelChoiceField(
        queryset=CustomDeck.objects.none(),
        required=False,
        empty_label="— Not in a named deck —",
        label="Named deck",
        widget=forms.Select(
            attrs={
                "class": "vcustom-input",
                "id": "id_deck",
                "form": "custom-card-form",
            }
        ),
    )

    definition_image = forms.ImageField(
        required=False,
        label="Picture for definition side (optional)",
        validators=[
            FileExtensionValidator(allowed_extensions=["png", "jpg", "jpeg", "gif", "webp"])
        ],
        widget=ClearableFileInput(
            attrs={
                "class": "vcustom-file-input",
                "accept": "image/png,image/jpeg,image/gif,image/webp",
            }
        ),
    )

    class Meta:
        model = CustomCard
        fields = (
            "word",
            "definition",
            "example_sentence",
            "topic",
            "deck",
            "definition_image",
        )
        widgets = {
            "word": forms.TextInput(
                attrs={"class": "vcustom-input", "autocomplete": "off"}
            ),
            "definition": forms.Textarea(
                attrs={"class": "vcustom-textarea", "rows": 5}
            ),
            "example_sentence": forms.Textarea(
                attrs={"class": "vcustom-textarea", "rows": 4}
            ),
            "topic": forms.Select(attrs={"class": "vcustom-hidden-select"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        self._user = user
        super().__init__(*args, **kwargs)
        if user is not None and user.is_authenticated:
            self.fields["deck"].queryset = CustomDeck.objects.filter(
                student=user
            ).order_by("name")
        else:
            self.fields["deck"].queryset = CustomDeck.objects.none()

    def clean(self):
        cleaned = super().clean()
        topic = cleaned.get("topic")
        deck = cleaned.get("deck")
        if topic != CustomCard.TOPIC_OTHER:
            cleaned["deck"] = None
        elif (
            deck
            and self._user is not None
            and getattr(self._user, "is_authenticated", False)
            and deck.student_id != self._user.id
        ):
            self.add_error("deck", "That deck does not belong to you.")
        return cleaned

    def clean_definition_image(self):
        f = self.cleaned_data.get("definition_image")
        if f and getattr(f, "size", 0) > _MAX_IMAGE_BYTES:
            raise forms.ValidationError("Image must be 2 MB or smaller.")
        return f

    def save(self, commit=True):
        inst = super().save(commit=False)
        if self._user is not None and getattr(self._user, "is_authenticated", False):
            row = UserProfile.objects.filter(user=self._user).values_list(
                "level", flat=True
            ).first()
            inst.level = int(row) if row is not None else 2
        if commit:
            inst.save()
        return inst
