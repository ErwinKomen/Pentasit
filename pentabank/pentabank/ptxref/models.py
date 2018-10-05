from django.db import models

# Paratext reference format
MAX_TEXT_LEN=255

class Book(models.Model):
    abbr = models.CharField("Book abbreviation", max_length=3)
    english = models.CharField("Book name", max_length=40)
    number = models.IntegerField("Number of this book")


class Reference(models.Model):
    """A reference to one particular verse"""

    book = models.ForeignKey(Book)
    chapter = models.IntegerField("Chapter")
    verse = models.IntegerField("Verse")


class Selection(models.Model):
    """One <Selection>"""

    verse = models.ForeignKey(Reference, related_name="start_verse")
    endverse = models.ForeignKey(Reference, related_name="end_verse")
    text = models.CharField("Selected text", max_length=MAX_TEXT_LEN, default="", blank=True)
    start = models.IntegerField("Start position", blank=True, default=0)
    before = models.TextField("Context before", default="")
    after = models.TextField("Context after", default="")


class VerseCollection(models.Model):
    """A collection of verse items"""

    version = models.CharField("Scripture version", max_length=20, blank=True, default="")
    header = models.TextField("Header text", blank=True, default="")


class VerseItem(models.Model):
    """A verselistitem"""

    denied = models.CharField("Denied", max_length=10, default="False")
    message = models.TextField("Message", default="")
    selection = models.ForeignKey(Selection)
    # [1] Each verseitem belongs to a collection
    versecollection = models.ForeignKey(VerseCollection)
