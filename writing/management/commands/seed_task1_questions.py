"""Insert static IELTS Academic Task 1 prompts if the table has none (or with --force)."""

from django.core.management.base import BaseCommand
from django.db import transaction

from writing.models import WritingQuestion

# (topic, level, question_text, prompt_kind)
TASK1_SEED: list[tuple[str, int, str, str]] = [
    (
        WritingQuestion.TOPIC_ENVIRONMENT,
        1,
        "The bar chart below shows average household recycling rates (%) in four cities in 2015 and 2020. "
        "Summarize the information by selecting and reporting the main features, and make comparisons where relevant.",
        WritingQuestion.T1_CHART,
    ),
    (
        WritingQuestion.TOPIC_ENVIRONMENT,
        2,
        "The line graph shows carbon dioxide emissions (million tonnes) from transport in one country between 1990 and 2020. "
        "Summarize the information by selecting and reporting the main features, and make comparisons where relevant.",
        WritingQuestion.T1_CHART,
    ),
    (
        WritingQuestion.TOPIC_ENVIRONMENT,
        3,
        "The table gives information about water use (litres per person per day) in urban and rural areas in three regions. "
        "Summarize the information by selecting and reporting the main features, and make comparisons where relevant.",
        WritingQuestion.T1_TABLE,
    ),
    (
        WritingQuestion.TOPIC_HEALTH,
        1,
        "The pie charts compare the main reasons people visited a clinic in two different years. "
        "Summarize the information by selecting and reporting the main features, and make comparisons where relevant.",
        WritingQuestion.T1_CHART,
    ),
    (
        WritingQuestion.TOPIC_HEALTH,
        2,
        "The diagram illustrates the stages in the process of blood donation from registration to storage. "
        "Summarize the information by selecting and reporting the main features.",
        WritingQuestion.T1_PROCESS,
    ),
    (
        WritingQuestion.TOPIC_HEALTH,
        3,
        "The chart shows the percentage of adults doing moderate exercise at least three times a week, by age group, in 2010 and 2020. "
        "Summarize the information by selecting and reporting the main features, and make comparisons where relevant.",
        WritingQuestion.T1_CHART,
    ),
    (
        WritingQuestion.TOPIC_TECHNOLOGY,
        1,
        "The bar chart shows the number of mobile phone subscriptions (per 100 people) in five countries in 2005 and 2015. "
        "Summarize the information by selecting and reporting the main features, and make comparisons where relevant.",
        WritingQuestion.T1_CHART,
    ),
    (
        WritingQuestion.TOPIC_TECHNOLOGY,
        2,
        "The line graph compares the percentage of households with broadband internet access in urban and rural areas from 2010 to 2020. "
        "Summarize the information by selecting and reporting the main features, and make comparisons where relevant.",
        WritingQuestion.T1_CHART,
    ),
    (
        WritingQuestion.TOPIC_TECHNOLOGY,
        3,
        "The table presents average daily screen time (hours) for children in three age groups across four countries. "
        "Summarize the information by selecting and reporting the main features, and make comparisons where relevant.",
        WritingQuestion.T1_TABLE,
    ),
    (
        WritingQuestion.TOPIC_EDUCATION,
        1,
        "The bar chart shows the proportion of students studying foreign languages at secondary school in four countries. "
        "Summarize the information by selecting and reporting the main features, and make comparisons where relevant.",
        WritingQuestion.T1_CHART,
    ),
    (
        WritingQuestion.TOPIC_EDUCATION,
        2,
        "The pie charts compare sources of university funding in one country in 2000 and 2020. "
        "Summarize the information by selecting and reporting the main features, and make comparisons where relevant.",
        WritingQuestion.T1_CHART,
    ),
    (
        WritingQuestion.TOPIC_EDUCATION,
        3,
        "The chart shows enrolment in online courses (thousands) by subject area over a five-year period. "
        "Summarize the information by selecting and reporting the main features, and make comparisons where relevant.",
        WritingQuestion.T1_CHART,
    ),
    (
        WritingQuestion.TOPIC_SOCIETY,
        1,
        "The bar chart shows the percentage of people who used public transport to commute in five cities in one year. "
        "Summarize the information by selecting and reporting the main features, and make comparisons where relevant.",
        WritingQuestion.T1_CHART,
    ),
    (
        WritingQuestion.TOPIC_SOCIETY,
        2,
        "The line graph shows the average age of first marriage for men and women in one country between 1980 and 2020. "
        "Summarize the information by selecting and reporting the main features, and make comparisons where relevant.",
        WritingQuestion.T1_CHART,
    ),
    (
        WritingQuestion.TOPIC_SOCIETY,
        3,
        "The maps show the centre of a town in 1990 and 2020. Summarize the information by selecting and reporting the main features, "
        "and make comparisons where relevant.",
        WritingQuestion.T1_MAP,
    ),
]


class Command(BaseCommand):
    help = "Create static Task 1 WritingQuestion rows (15) if none exist, unless --force replaces them."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--force",
            action="store_true",
            help="Delete existing Task 1 questions, then insert seed data.",
        )

    def handle(self, *args, **options) -> None:
        force = options["force"]
        existing = WritingQuestion.objects.filter(question_type=WritingQuestion.TASK1).count()

        if existing and not force:
            self.stdout.write(
                self.style.NOTICE(
                    f"Skip: {existing} Task 1 question(s) already exist. Use --force to replace."
                )
            )
            return

        with transaction.atomic():
            if force:
                deleted, _ = WritingQuestion.objects.filter(
                    question_type=WritingQuestion.TASK1
                ).delete()
                self.stdout.write(self.style.WARNING(f"Deleted {deleted} Task 1 row(s)."))

            rows = [
                WritingQuestion(
                    question_text=text,
                    question_type=WritingQuestion.TASK1,
                    topic=topic,
                    level=level,
                    prompt_kind=kind,
                )
                for topic, level, text, kind in TASK1_SEED
            ]
            WritingQuestion.objects.bulk_create(rows)

        self.stdout.write(self.style.SUCCESS(f"Inserted {len(rows)} Task 1 questions."))
