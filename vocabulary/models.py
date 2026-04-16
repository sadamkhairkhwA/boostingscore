from django.conf import settings
from django.db import models
from django.db.models import Q


class Word(models.Model):
    TOPIC_ENVIRONMENT = "environment"
    TOPIC_HEALTH = "health"
    TOPIC_TECHNOLOGY = "technology"
    TOPIC_EDUCATION = "education"
    TOPIC_SOCIETY = "society"

    TOPIC_CHOICES = [
        (TOPIC_ENVIRONMENT, "Environment"),
        (TOPIC_HEALTH, "Health"),
        (TOPIC_TECHNOLOGY, "Technology"),
        (TOPIC_EDUCATION, "Education"),
        (TOPIC_SOCIETY, "Society"),
    ]

    word = models.CharField(max_length=255, unique=True)
    topic = models.CharField(max_length=32, choices=TOPIC_CHOICES)
    level = models.IntegerField(choices=[(1, "1"), (2, "2"), (3, "3")])
    definition = models.TextField(blank=True)
    example_sentence = models.TextField(blank=True)
    definition_image = models.ImageField(
        upload_to="vocab/words/",
        blank=True,
        null=True,
        help_text="Optional picture shown on the definition side of flashcards.",
    )
    part_of_speech = models.CharField(
        max_length=64,
        blank=True,
        help_text="e.g. noun, verb (shown on word list).",
    )
    synonyms = models.JSONField(blank=True, default=list)
    antonyms = models.JSONField(blank=True, default=list)
    collocations = models.JSONField(blank=True, default=list)

    class Meta:
        ordering = ["topic", "level", "word"]

    def __str__(self) -> str:
        return self.word


class CustomCard(models.Model):
    TOPIC_ENVIRONMENT = "environment"
    TOPIC_HEALTH = "health"
    TOPIC_TECHNOLOGY = "technology"
    TOPIC_EDUCATION = "education"
    TOPIC_SOCIETY = "society"
    TOPIC_OTHER = "other"

    TOPIC_CHOICES = [
        ("environment", "Environment"),
        ("health", "Health"),
        ("technology", "Technology"),
        ("education", "Education"),
        ("society", "Society"),
        ("other", "Select vocabulary"),
    ]

    word = models.CharField(max_length=255)
    definition = models.TextField(blank=True)
    example_sentence = models.TextField(blank=True)
    topic = models.CharField(max_length=32, choices=TOPIC_CHOICES)
    level = models.IntegerField(choices=[(1, "1"), (2, "2"), (3, "3")])
    is_mastered = models.BooleanField(default=False)
    review_count = models.PositiveIntegerField(default=0)
    next_review_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Due for spaced-repetition review when <= now (null = due now).",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="custom_cards",
    )
    definition_image = models.ImageField(
        upload_to="vocab/custom/",
        blank=True,
        null=True,
        help_text="Optional picture shown on the definition side when you study this card.",
    )
    deck = models.ForeignKey(
        "CustomDeck",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cards",
    )
    part_of_speech = models.CharField(max_length=64, blank=True)
    synonyms = models.JSONField(blank=True, default=list)
    antonyms = models.JSONField(blank=True, default=list)
    collocations = models.JSONField(blank=True, default=list)

    class Meta:
        ordering = ["topic", "level", "word"]
        constraints = [
            models.UniqueConstraint(
                fields=("student", "word", "topic"),
                name="vocabulary_unique_custom_word_per_topic",
            ),
        ]

    def __str__(self) -> str:
        return self.word


class CustomDeck(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="custom_decks",
    )

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=("student", "name"),
                name="vocab_unique_custom_deck_name_per_student",
            ),
        ]

    def __str__(self) -> str:
        return self.name


class VocabFavorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vocab_favorites",
    )
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="favorited_by",
    )
    custom_card = models.ForeignKey(
        CustomCard,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="favorited_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(custom_card__isnull=True, word__isnull=False)
                    | Q(custom_card__isnull=False, word__isnull=True)
                ),
                name="vocab_favorite_exactly_one_target",
            ),
            models.UniqueConstraint(
                fields=("user", "word"),
                condition=Q(word__isnull=False),
                name="uniq_vocab_fav_user_word",
            ),
            models.UniqueConstraint(
                fields=("user", "custom_card"),
                condition=Q(custom_card__isnull=False),
                name="uniq_vocab_fav_user_custom",
            ),
        ]


class VocabularyProgress(models.Model):
    times_seen = models.PositiveIntegerField(default=0)
    times_correct = models.PositiveIntegerField(default=0)
    times_wrong = models.PositiveIntegerField(default=0)
    times_marked_hard = models.PositiveIntegerField(default=0)
    sessions_seen = models.PositiveIntegerField(default=0)
    last_session_date = models.DateField(blank=True, null=True)
    mastery_level = models.PositiveSmallIntegerField(default=1)
    next_review = models.DateTimeField(blank=True, null=True)
    last_reviewed = models.DateTimeField(blank=True, null=True)
    type_success_count = models.PositiveIntegerField(
        default=0,
        help_text="Successful Type-it (example mode) checks; used for mastery level 4.",
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vocabulary_progress",
    )
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="student_progress",
    )
    custom_card = models.ForeignKey(
        CustomCard,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="student_progress",
    )

    class Meta:
        ordering = ["-last_reviewed", "-pk"]
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(custom_card__isnull=True, word__isnull=False)
                    | Q(custom_card__isnull=False, word__isnull=True)
                ),
                name="vocab_progress_exactly_one_target",
            ),
            models.UniqueConstraint(
                fields=("student", "word"),
                condition=Q(word__isnull=False),
                name="uniq_vocab_progress_student_word",
            ),
            models.UniqueConstraint(
                fields=("student", "custom_card"),
                condition=Q(custom_card__isnull=False),
                name="uniq_vocab_progress_student_custom",
            ),
        ]


class TypeItResult(models.Model):
    student_text = models.TextField()
    mode = models.CharField(
        max_length=32,
        help_text="sentence (example) or definition",
    )
    band_score = models.FloatField()
    improved_text = models.TextField(blank=True)
    ielts_mode = models.BooleanField(default=True)
    response_json = models.JSONField(blank=True, default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="type_it_results",
    )
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="type_it_results",
    )
    custom_card = models.ForeignKey(
        CustomCard,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="type_it_results",
    )

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(custom_card__isnull=True, word__isnull=False)
                    | Q(custom_card__isnull=False, word__isnull=True)
                ),
                name="type_it_result_exactly_one_target",
            ),
        ]
