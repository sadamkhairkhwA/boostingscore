from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q, UniqueConstraint


class UserProfile(models.Model):
    LEVEL_CHOICES = [(1, "Beginner"), (2, "Standard"), (3, "Advanced")]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    level = models.IntegerField(choices=LEVEL_CHOICES, default=1)
    placement_score = models.IntegerField(default=0)
    placement_completed = models.BooleanField(default=False)
    placement_results = models.JSONField(default=dict, blank=True)
    placement_taken_at = models.DateTimeField(null=True, blank=True)
    diagnostic_completed = models.BooleanField(default=False)
    diagnostic_results = models.JSONField(default=dict, blank=True)
    section_reviews = models.JSONField(default=dict, blank=True)
    streak = models.IntegerField(default=0)
    best_streak = models.IntegerField(default=0)
    reading_speed_wpm = models.IntegerField(null=True, blank=True)
    review_easy_days = models.IntegerField(default=7)
    review_hard_days = models.IntegerField(default=1)
    review_hard_hours = models.PositiveSmallIntegerField(default=24)
    review_good_hours = models.PositiveSmallIntegerField(default=72)
    review_easy_hours = models.PositiveSmallIntegerField(default=168)
    last_activity_date = models.DateField(null=True, blank=True)
    plan = models.CharField(max_length=32, default="free")
    speaking_ai_notice_seen = models.BooleanField(default=False)
    pending_email = models.EmailField(blank=True, default="")
    pending_email_sent_at = models.DateTimeField(null=True, blank=True)

    @property
    def level_label(self):
        return {1: "Beginner", 2: "Standard", 3: "Advanced"}.get(self.level, "Beginner")

    @property
    def band_range(self):
        if self.placement_completed and isinstance(self.placement_results, dict):
            label = (self.placement_results.get("band_range") or "").strip()
            if label:
                return label
        return {1: "Band 4–5", 2: "Band 5.5–6.5", 3: "Band 7–9"}.get(self.level, "Band 4–5")

    @property
    def level_badge_text(self):
        """Header pill: placement band once taken, otherwise Beginner/Standard/Advanced."""
        if self.placement_completed and isinstance(self.placement_results, dict):
            label = (self.placement_results.get("band_range") or "").strip()
            if label:
                return label
        return self.level_label

    def __str__(self):
        return f"{self.user.username} — {self.level_label}"


class SignupCode(models.Model):
    """6-digit email verification code for activating a new account."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="signup_code"
    )
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"SignupCode for {self.user.username}"


class Word(models.Model):
    TOPIC_CHOICES = [
        ("environment", "Environment"),
        ("health", "Health"),
        ("technology", "Technology"),
        ("education", "Education"),
        ("society", "Society"),
        ("travel", "Travel"),
        ("science", "Science"),
        ("business", "Business"),
    ]
    LEVEL_CHOICES = [(1, "Beginner"), (2, "Standard"), (3, "Advanced")]
    word = models.CharField(max_length=100)
    topic = models.CharField(max_length=50, choices=TOPIC_CHOICES)
    level = models.IntegerField(choices=LEVEL_CHOICES, default=1)
    definition = models.TextField()
    example_sentence = models.TextField()
    collocations = models.JSONField(default=list, blank=True)
    synonyms = models.JSONField(default=list, blank=True)
    part_of_speech = models.CharField(max_length=50, blank=True)
    phonetic = models.CharField(max_length=100, blank=True)
    ielts_note = models.TextField(
        blank=True,
        help_text="IELTS usage note for Type it and study views.",
    )
    definition_image = models.ImageField(
        upload_to="vocab_word_images/", blank=True, null=True
    )
    topic_pack = models.ForeignKey(
        "TopicIELTSWordCache",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="pack_words",
    )

    class Meta:
        ordering = ["topic", "level", "word"]

    def __str__(self):
        return f"{self.word} ({self.topic})"


class TopicIELTSWordCache(models.Model):
    """Cached AI-generated word lists per topic (beginner / standard / advanced)."""

    STATUS_GENERATING = "generating"
    STATUS_READY = "ready"
    STATUS_ERROR = "error"

    topic = models.CharField(max_length=50, unique=True, db_index=True)
    status = models.CharField(max_length=20, default=STATUS_GENERATING)
    beginner = models.JSONField(default=list, blank=True)
    standard = models.JSONField(default=list, blank=True)
    advanced = models.JSONField(default=list, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.topic} ({self.status})"


class VocabularyProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(
        Word, null=True, blank=True, on_delete=models.CASCADE, related_name="progress_rows"
    )
    custom_card = models.ForeignKey(
        "CustomCard",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="progress_rows",
    )
    method = models.CharField(max_length=50, default="flashcard")
    status = models.CharField(max_length=20, default="learning")
    times_seen = models.IntegerField(default=0)
    times_correct = models.IntegerField(default=0)
    times_wrong = models.IntegerField(default=0)
    times_marked_hard = models.IntegerField(default=0)
    is_hard_word = models.BooleanField(
        default=False,
        help_text="Keeps this word in the Hard words collection until the user clears it.",
    )
    hard_easy_streak = models.PositiveSmallIntegerField(
        default=0,
        help_text="Consecutive Easy ratings while the word is in the Hard words collection.",
    )
    mastery_level = models.IntegerField(default=1)
    next_review = models.DateTimeField(null=True, blank=True)
    last_reviewed = models.DateTimeField(null=True, blank=True)
    is_favored = models.BooleanField(default=False)
    sessions_seen = models.IntegerField(default=0)
    last_session_date = models.DateField(null=True, blank=True)
    type_success_count = models.IntegerField(default=0)
    easy_chip_master_count = models.IntegerField(
        default=0,
        help_text="Times user rated Easy on flashcards; chip turns green at 3.",
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=("student", "word"),
                condition=Q(word__isnull=False),
                name="vocab_progress_student_word_uniq",
            ),
            UniqueConstraint(
                fields=("student", "custom_card"),
                condition=Q(custom_card__isnull=False),
                name="vocab_progress_student_custom_uniq",
            ),
        ]

    def __str__(self):
        label = (
            self.word.word
            if self.word_id
            else (self.custom_card.word if self.custom_card_id else "?")
        )
        return f"{self.student.username} — {label} — level {self.mastery_level}"


class TypeItResult(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE, null=True, blank=True)
    student_text = models.TextField()
    mode = models.CharField(max_length=50, default="word")
    band_score = models.FloatField(null=True, blank=True)
    improved_text = models.TextField(blank=True)
    ielts_mode = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} — band {self.band_score}"


class TypeItAttempt(models.Model):
    """Single Type it practice attempt, scored by AI (definition, sentence, or both)."""

    MODE_DEFINITION = "definition"
    MODE_SENTENCE = "sentence"
    MODE_BOTH = "both"
    MODE_CHOICES = [
        (MODE_DEFINITION, "Definition only"),
        (MODE_SENTENCE, "Sentence only"),
        (MODE_BOTH, "Definition + sentence"),
    ]

    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="type_it_attempts"
    )
    word = models.ForeignKey(
        Word, on_delete=models.CASCADE, related_name="type_it_attempts", null=True, blank=True
    )
    custom_word = models.ForeignKey(
        "CustomDeckWord",
        on_delete=models.CASCADE,
        related_name="type_it_attempts",
        null=True,
        blank=True,
    )
    custom_card = models.ForeignKey(
        "CustomCard",
        on_delete=models.CASCADE,
        related_name="type_it_attempts",
        null=True,
        blank=True,
    )
    deck_slug = models.CharField(max_length=80, db_index=True)
    mode = models.CharField(max_length=16, choices=MODE_CHOICES, default=MODE_BOTH, db_index=True)
    definition_score = models.PositiveSmallIntegerField(null=True, blank=True)
    sentence_score = models.PositiveSmallIntegerField(null=True, blank=True)
    total_score = models.PositiveSmallIntegerField()
    assisted = models.BooleanField(default=False)
    student_definition = models.TextField(blank=True)
    student_sentence = models.TextField(blank=True)
    feedback_json = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["student", "word"]),
            models.Index(fields=["student", "deck_slug"]),
            models.Index(
                fields=["student", "custom_card"],
                name="vocabulary__student_8a1f2c_idx",
            ),
        ]

    def __str__(self):
        if self.word_id:
            label = self.word.word
        elif self.custom_word_id:
            label = self.custom_word.word
        else:
            label = "?"
        return f"{self.student.username} — {label} — {self.total_score}"


class CustomDeck(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    colour = models.CharField(max_length=20, default="navy")
    emoji = models.CharField(max_length=10, default="📖")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} — {self.name}"


class CustomCard(models.Model):
    """User-authored card; ``topic`` groups cards into the same topic decks as Words."""

    TOPIC_OTHER = "other"
    TOPIC_CHOICES = list(Word.TOPIC_CHOICES) + [(TOPIC_OTHER, "My vocabulary")]

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    deck = models.ForeignKey(CustomDeck, on_delete=models.CASCADE)
    word = models.CharField(max_length=200)
    definition = models.TextField()
    example_sentence = models.TextField(blank=True)
    topic = models.CharField(
        max_length=50, choices=TOPIC_CHOICES, default=TOPIC_OTHER
    )
    level = models.IntegerField(choices=Word.LEVEL_CHOICES, default=1)
    part_of_speech = models.CharField(max_length=50, blank=True)
    is_mastered = models.BooleanField(default=False)
    next_review_at = models.DateTimeField(null=True, blank=True)
    definition_image = models.ImageField(
        upload_to="vocab_custom_images/", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.word


class CustomDeckWord(models.Model):
    deck = models.ForeignKey(CustomDeck, on_delete=models.CASCADE, related_name="words")
    word = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.deck.name}: {self.word}"


class DailyAiUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="daily_ai_usage")
    usage_date = models.DateField()
    count = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["-usage_date"]
        unique_together = [("user", "usage_date")]

    def __str__(self):
        return f"{self.user_id} {self.usage_date}: {self.count}"


class AiUsageLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ai_usage_logs")
    feature = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "-created_at"], name="vocab_ai_user_created_idx"),
            models.Index(fields=["feature", "-created_at"], name="vocab_ai_feat_created_idx"),
        ]

    def __str__(self):
        return f"{self.user_id} {self.feature} @ {self.created_at}"


class FeedbackSubmission(models.Model):
    TYPE_BUG = "bug"
    TYPE_SUGGESTION = "suggestion"
    TYPE_OTHER = "other"
    TYPE_CHOICES = [
        (TYPE_BUG, "Bug"),
        (TYPE_SUGGESTION, "Suggestion"),
        (TYPE_OTHER, "Something else"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="feedback_submissions",
    )
    email = models.EmailField(blank=True, default="")
    feedback_type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, default=TYPE_SUGGESTION
    )
    message = models.TextField()
    page_url = models.CharField(max_length=500, blank=True, default="")
    user_agent = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Feedback submission"
        verbose_name_plural = "Feedback submissions"
        indexes = [
            models.Index(
                fields=["user", "-created_at"], name="vocab_fb_user_created_idx"
            ),
            models.Index(
                fields=["feedback_type", "-created_at"],
                name="vocab_fb_type_created_idx",
            ),
        ]

    def __str__(self):
        return f"{self.feedback_type} from {self.email or self.user_id} @ {self.created_at}"
