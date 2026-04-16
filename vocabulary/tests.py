import json
import os
import tempfile
from datetime import timedelta
from pathlib import Path
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from boostingscore.models import UserProfile
from boostingscore.openai_key import resolve_openai_api_key
from vocabulary.models import CustomCard, CustomDeck, VocabularyProgress, Word
from vocabulary.progress_service import record_flashcard_rating


def _complete_placement(user):
    UserProfile.objects.update_or_create(
        user=user,
        defaults={"placement_completed": True, "level": 2},
    )


class CustomCardFormPageTests(TestCase):
    """Create/edit single flashcard uses green studio layout + vocab_custom_card.css."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="t_custom", password="x")
        _complete_placement(self.user)
        self.client = Client(HTTP_HOST="localhost")

    def test_create_page_has_stylesheet_and_layout(self):
        self.client.force_login(self.user)
        r = self.client.get("/vocabulary/custom/new/")
        self.assertEqual(r.status_code, 200)
        body = r.content.decode()
        self.assertIn("vocab_custom_card.css", body)
        self.assertIn("vcustom-form-page-body", body)
        self.assertIn("vcustom-layout", body)
        self.assertIn("Named deck", body)

    def test_vocab_custom_card_css_exists(self):
        path = Path(settings.BASE_DIR) / "static" / "css" / "vocab_custom_card.css"
        self.assertTrue(path.is_file())
        self.assertIn("vcustom-layout", path.read_text(encoding="utf-8"))


class VocabTopicMyVocabularyLabelTests(TestCase):
    """Studio: topic button shows active label; modal lists sets with personal (other)."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="t_topic_lbl", password="x")
        _complete_placement(self.user)
        self.client = Client(HTTP_HOST="localhost")

    def test_index_shows_topic_picker_modal_and_current_label(self):
        self.client.force_login(self.user)
        r = self.client.get(reverse("vocabulary:index"))
        self.assertEqual(r.status_code, 200)
        body = r.content.decode()
        self.assertIn('class="vocab-app"', body)
        self.assertIn("Environment", body)
        self.assertIn("vocab-topic-select", body)
        self.assertIn("vocab-topic-picker-modal", body)
        self.assertIn("Your vocabulary sets", body)
        self.assertIn("My vocabulary", body)
        self.assertIn("vocab-topic-deck-card", body)
        self.assertIn("Study flashcards", body)
        self.assertIn("All sets", body)
        self.assertIn("Choose vocabulary set. Current:", body)
        self.assertNotRegex(body, r">Other</a>")  # pill label, not substring in JS comments


class VocabularyHomeTests(TestCase):
    """Dashboard at /vocabulary/ (root) with stats and method shortcuts."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="t_vocab_home", password="x")
        _complete_placement(self.user)
        self.client = Client(HTTP_HOST="localhost")

    def test_home_requires_login(self):
        r = self.client.get(reverse("vocabulary:home"), follow=False)
        self.assertEqual(r.status_code, 302)

    def test_home_renders_for_authenticated_user(self):
        self.client.force_login(self.user)
        r = self.client.get(reverse("vocabulary:home"), follow=False)
        self.assertEqual(r.status_code, 200)
        body = r.content.decode()
        self.assertIn("vocab-methods", body)
        self.assertIn("How do you want to study today?", body)
        self.assertIn(reverse("vocabulary:guide"), body)


class VocabularyGuideTests(TestCase):
    """Standalone guide at /vocabulary/guide/."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="t_vocab_guide", password="x")
        _complete_placement(self.user)
        self.client = Client(HTTP_HOST="localhost")

    def test_guide_requires_login(self):
        r = self.client.get(reverse("vocabulary:guide"), follow=False)
        self.assertEqual(r.status_code, 302)

    def test_guide_renders(self):
        self.client.force_login(self.user)
        r = self.client.get(reverse("vocabulary:guide"), follow=False)
        self.assertEqual(r.status_code, 200)
        body = r.content.decode()
        self.assertIn("guide-page", body)
        self.assertIn("Vocabulary guide", body)
        self.assertIn("swTab", body)


class TypeItDeckSelectTests(TestCase):
    """Standalone Type it deck picker + session redirect into studio."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="t_type_it", password="x")
        _complete_placement(self.user)
        self.client = Client(HTTP_HOST="localhost")

    def test_deck_select_page_anonymous_ok(self):
        r = self.client.get(reverse("vocabulary:type_it_deck_select"))
        self.assertEqual(r.status_code, 200)
        body = r.content.decode()
        self.assertIn("ti-page", body)
        self.assertIn("Writing practice", body)
        self.assertIn(reverse("vocabulary:type_it_session"), body)

    def test_session_redirect_topic(self):
        self.client.force_login(self.user)
        r = self.client.get(
            reverse("vocabulary:type_it_session") + "?topic=environment",
            follow=False,
        )
        self.assertIn(r.status_code, (200, 302))
        if r.status_code == 200:
            self.assertIn("ti-session-page", r.content.decode())
        else:
            self.assertEqual(r["Location"], reverse("vocabulary:type_it_deck_select"))

    def test_session_redirect_custom_deck(self):
        self.client.force_login(self.user)
        deck = CustomDeck.objects.create(student=self.user, name="lab")
        r = self.client.get(
            reverse("vocabulary:type_it_session") + f"?custom_deck={deck.pk}",
            follow=False,
        )
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r["Location"], reverse("vocabulary:type_it_deck_select"))

    def test_session_invalid_redirects_to_picker(self):
        self.client.force_login(self.user)
        r = self.client.get(reverse("vocabulary:type_it_session"), follow=False)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r["Location"], reverse("vocabulary:type_it_deck_select"))

    def test_session_result_empty_redirects_to_picker(self):
        self.client.force_login(self.user)
        r = self.client.get(
            reverse("vocabulary:type_it_session_result"), follow=False
        )
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r["Location"], reverse("vocabulary:type_it_deck_select"))

    def test_session_index_past_end_redirects_to_result(self):
        self.client.force_login(self.user)
        Word.objects.create(
            word="ti_past_end_word",
            topic=Word.TOPIC_ENVIRONMENT,
            level=2,
            definition="def",
        )
        r = self.client.get(
            reverse("vocabulary:type_it_session")
            + "?topic=environment&index=2",
            follow=False,
        )
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r["Location"], reverse("vocabulary:type_it_session_result"))

    def test_session_result_renders_with_history(self):
        self.client.force_login(self.user)
        session = self.client.session
        session["type_it_history"] = [
            {"word": "sample", "band": 6.0, "sentence": "A short answer."}
        ]
        session["type_it_bands"] = [6.0]
        session.save()
        r = self.client.get(reverse("vocabulary:type_it_session_result"), follow=False)
        self.assertEqual(r.status_code, 200)
        body = r.content.decode()
        self.assertIn("Session complete", body)
        self.assertIn("sample", body)


class MainCssCacheBustTests(TestCase):
    """main.css is linked with ?v= so browsers pick up stylesheet updates."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="t_css_bust", password="x")
        _complete_placement(self.user)
        self.client = Client(HTTP_HOST="localhost")

    def test_vocabulary_page_links_versioned_main_css(self):
        self.client.force_login(self.user)
        r = self.client.get(reverse("vocabulary:index"))
        self.assertEqual(r.status_code, 200)
        body = r.content.decode()
        ver = getattr(settings, "STATIC_CSS_VERSION", "")
        self.assertTrue(ver, msg="STATIC_CSS_VERSION should be set in settings")
        self.assertIn(f"main.css?v={ver}", body)


class VocabSpeakIconCssTests(TestCase):
    """Listen buttons: outlined green circle + SVG on ::after (Safari-safe)."""

    def test_main_css_speak_icon_layering(self):
        path = Path(settings.BASE_DIR) / "static" / "css" / "main.css"
        text = path.read_text(encoding="utf-8")
        self.assertIn("--vocab-speak-green:", text)
        self.assertIn(".vocab-card-speak::after", text)
        self.assertIn(".vocab-speak-icon-wrap::after", text)
        self.assertIn("appearance: none", text)
        # Two-wave stroke path (inner + outer arc)
        self.assertIn("M16.5%207.2q2.6%204.8%200%209.6", text)


class FlashcardCreatePageTests(TestCase):
    """Regression: flashcard set create must ship fc_create.css and page body class."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="t_fc", password="x")
        _complete_placement(self.user)
        self.client = Client(HTTP_HOST="localhost")

    def test_page_includes_stylesheet_and_body_class(self):
        self.client.force_login(self.user)
        r = self.client.get("/vocabulary/set/ai/")
        self.assertEqual(r.status_code, 200)
        body = r.content.decode()
        self.assertIn("fc_create.css", body)
        self.assertIn("fc-create-page-body", body)
        self.assertIn("vocab-app", body)
        self.assertIn("Create a new flashcard set", body)
        self.assertIn('id="fc-set-title"', body)
        self.assertIn('id="fc-set-description"', body)

    def test_fc_create_css_file_on_disk(self):
        path = Path(settings.BASE_DIR) / "static" / "css" / "fc_create.css"
        self.assertTrue(path.is_file(), msg="static/css/fc_create.css must exist")
        self.assertIn("fc-create-layout", path.read_text(encoding="utf-8"))


class FlashcardSetSaveTests(TestCase):
    """Bulk save creates CustomDeck + links cards for personal (other) topic."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="t_fc_save", password="x")
        _complete_placement(self.user)
        self.client = Client(HTTP_HOST="localhost")
        self.save_url = reverse("vocabulary:flashcard_set_save")

    def test_personal_set_requires_title(self):
        self.client.force_login(self.user)
        import json

        r = self.client.post(
            self.save_url,
            data=json.dumps(
                {
                    "topic": "other",
                    "level": 2,
                    "set_title": "",
                    "set_description": "Note",
                    "cards": [{"word": "a", "definition": "b", "example_sentence": ""}],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(r.status_code, 400)
        self.assertFalse(CustomCard.objects.filter(student=self.user).exists())

    def test_personal_set_creates_set_and_links_cards(self):
        self.client.force_login(self.user)
        import json

        r = self.client.post(
            self.save_url,
            data=json.dumps(
                {
                    "topic": "other",
                    "level": 2,
                    "set_title": "Python basics",
                    "set_description": "Study notes",
                    "cards": [
                        {
                            "word": "term1",
                            "definition": "def1",
                            "example_sentence": "",
                        }
                    ],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(r.status_code, 200)
        payload = r.json()
        self.assertTrue(payload.get("ok"))
        self.assertEqual(payload.get("created"), 1)
        cset = CustomDeck.objects.get(student=self.user, name="Python basics")
        self.assertEqual(cset.description, "Study notes")
        card = CustomCard.objects.get(student=self.user, word="term1")
        self.assertEqual(card.deck_id, cset.id)

    def test_catalog_topic_does_not_require_set_title(self):
        self.client.force_login(self.user)
        import json

        r = self.client.post(
            self.save_url,
            data=json.dumps(
                {
                    "topic": "environment",
                    "level": 2,
                    "set_title": "",
                    "cards": [{"word": "erosion", "definition": "wear", "example_sentence": ""}],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(r.status_code, 200)
        card = CustomCard.objects.get(student=self.user, word="erosion")
        self.assertIsNone(card.deck_id)


class DeckCreateSaveTests(TestCase):
    """Named deck create page saves CustomDeck + cards."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="t_deck_page", password="x")
        _complete_placement(self.user)
        self.client = Client(HTTP_HOST="localhost")
        self.save_url = reverse("vocabulary:deck_create_save")
        self.create_url = reverse("vocabulary:deck_create")

    def test_create_page_loads(self):
        self.client.force_login(self.user)
        r = self.client.get(self.create_url)
        self.assertEqual(r.status_code, 200)
        body = r.content.decode()
        self.assertIn("Create a deck", body)
        self.assertIn("AI illustration", body)
        self.assertIn("AI generator", body)
        self.assertIn("Generate with AI", body)

    def test_requires_login(self):
        import json

        r = self.client.post(
            self.save_url,
            data=json.dumps({"name": "A", "cards": [{"word": "w", "definition": "d"}]}),
            content_type="application/json",
        )
        self.assertEqual(r.status_code, 302)

    def test_save_deck_and_cards(self):
        import json

        self.client.force_login(self.user)
        r = self.client.post(
            self.save_url,
            data=json.dumps(
                {
                    "name": "GRE verbs",
                    "description": "Week 1",
                    "level": 2,
                    "cards": [
                        {"word": "abate", "definition": "reduce"},
                    ],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertTrue(data.get("ok"))
        deck = CustomDeck.objects.get(student=self.user, name="GRE verbs")
        self.assertEqual(deck.description, "Week 1")
        card = CustomCard.objects.get(student=self.user, word="abate")
        self.assertEqual(card.deck_id, deck.id)
        self.assertEqual(card.topic, CustomCard.TOPIC_OTHER)
        self.assertIn("deck=", data.get("redirect_url", ""))

    def test_save_attaches_optional_image_base64(self):
        import json

        tiny_png_b64 = (
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
        )
        self.client.force_login(self.user)
        r = self.client.post(
            self.save_url,
            data=json.dumps(
                {
                    "name": "With image",
                    "level": 2,
                    "cards": [
                        {
                            "word": "pixel",
                            "definition": "dot",
                            "image_base64": tiny_png_b64,
                        },
                    ],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(r.status_code, 200)
        card = CustomCard.objects.get(student=self.user, word="pixel")
        self.assertTrue(card.definition_image)


class FlashReviewSettingsTests(TestCase):
    """UserProfile review intervals persist and drive VocabularyProgress.next_review."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="t_rev_set", password="pw")
        _complete_placement(self.user)
        self.client = Client(HTTP_HOST="localhost")
        self.word = Word.objects.create(
            word="flashsettings_word",
            topic=Word.TOPIC_ENVIRONMENT,
            level=2,
            definition="x",
        )
        self.settings_url = reverse("vocabulary:progress_review_settings")

    def test_post_saves_profile(self):
        self.client.force_login(self.user)
        r = self.client.post(
            self.settings_url,
            data=json.dumps(
                {
                    "review_easy_days": 14,
                    "review_hard_days": 3,
                    "review_session_size": 10,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertTrue(data.get("ok"))
        p = UserProfile.objects.get(user=self.user)
        self.assertEqual(p.review_easy_days, 14)
        self.assertEqual(p.review_hard_days, 3)
        self.assertEqual(p.review_session_size, 10)

    def test_invalid_easy_days_rejected(self):
        self.client.force_login(self.user)
        r = self.client.post(
            self.settings_url,
            data=json.dumps(
                {
                    "review_easy_days": 4,
                    "review_hard_days": 1,
                    "review_session_size": 20,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(r.status_code, 400)

    def test_rating_uses_saved_easy_interval(self):
        self.client.force_login(self.user)
        self.client.post(
            self.settings_url,
            data=json.dumps(
                {
                    "review_easy_days": 30,
                    "review_hard_days": 2,
                    "review_session_size": 20,
                }
            ),
            content_type="application/json",
        )
        before = timezone.now()
        record_flashcard_rating(self.user, "word", self.word.pk, "easy")
        prog = VocabularyProgress.objects.get(student=self.user, word=self.word)
        self.assertIsNotNone(prog.next_review)
        delta = prog.next_review - before
        self.assertGreaterEqual(delta, timedelta(days=29, seconds=-60))
        self.assertLessEqual(delta, timedelta(days=31, seconds=60))

    def test_hard_sets_next_review_from_profile(self):
        self.client.force_login(self.user)
        self.client.post(
            self.settings_url,
            data=json.dumps(
                {
                    "review_easy_days": 7,
                    "review_hard_days": 5,
                    "review_session_size": 20,
                }
            ),
            content_type="application/json",
        )
        before = timezone.now()
        record_flashcard_rating(self.user, "word", self.word.pk, "hard")
        prog = VocabularyProgress.objects.get(student=self.user, word=self.word)
        delta = prog.next_review - before
        self.assertGreaterEqual(delta, timedelta(days=4, seconds=-60))
        self.assertLessEqual(delta, timedelta(days=6, seconds=60))


class ResolveOpenAiApiKeyTests(TestCase):
    """`.env` loader accepts OPENAI_API_KEY=value (fixes legacy raw-first-line-only logic)."""

    def test_dotenv_openai_api_key_line(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": ""}):
            with tempfile.TemporaryDirectory() as tmp:
                p = Path(tmp) / ".env"
                p.write_text('OPENAI_API_KEY="sk-from-env-file"\n', encoding="utf-8")
                with override_settings(BASE_DIR=Path(tmp)):
                    self.assertEqual(resolve_openai_api_key(), "sk-from-env-file")

    def test_dotenv_legacy_raw_key_line(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": ""}):
            with tempfile.TemporaryDirectory() as tmp:
                p = Path(tmp) / ".env"
                p.write_text("sk-legacy-raw-only\n", encoding="utf-8")
                with override_settings(BASE_DIR=Path(tmp)):
                    self.assertEqual(resolve_openai_api_key(), "sk-legacy-raw-only")


class WordListPageTests(TestCase):
    """Dedicated word list: topic query, layout shell, stats row."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="t_word_list", password="x")
        _complete_placement(self.user)
        self.client = Client(HTTP_HOST="localhost")

    def test_missing_topic_redirects(self):
        self.client.force_login(self.user)
        r = self.client.get(reverse("vocabulary:word_list"))
        self.assertEqual(r.status_code, 302)

    def test_word_list_page_renders(self):
        self.client.force_login(self.user)
        r = self.client.get(reverse("vocabulary:word_list") + "?topic=environment")
        self.assertEqual(r.status_code, 200)
        body = r.content.decode()
        self.assertIn('class="wl-page"', body)
        self.assertIn("Total words", body)
        self.assertIn("Struggling", body)
        self.assertIn("wl-search", body)

    def test_word_list_all_renders(self):
        self.client.force_login(self.user)
        r = self.client.get(reverse("vocabulary:word_list") + "?all=1")
        self.assertEqual(r.status_code, 200)
        body = r.content.decode()
        self.assertIn("All vocabulary", body)
        self.assertIn('class="wl-page"', body)
