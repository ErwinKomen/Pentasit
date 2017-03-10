"""Situations for the pentaset records.

A situation defines parameters that need to be satisfied and that together determine the choice of a particular pentaset category.
"""
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


RELATION_NAME = "relation.name"
NP_TYPE = "situation.npType"
PENTA_CAT = "situation.penta"
PENTA_ANT = "situation.antecedent"
ACTION = "situation.action"
PART_OF_SPEECH = "pos.name"
OTHER_REQ = "other.name"


class FieldChoice(models.Model):

    field = models.CharField(max_length=50)
    english_name = models.CharField(max_length=50)
    dutch_name = models.CharField(max_length=50)
    machine_value = models.IntegerField(help_text="The actual numeric value stored in the database. Created automatically.")

    def __str__(self):
        return "{}: {}, {} ({})".format(
            self.field, self.english_name, self.dutch_name, str(self.machine_value))

    class Meta:
        ordering = ['field','machine_value']


def build_choice_list(field):
    """Create a list of choice-tuples"""

    choice_list = [];

    try:
        # check if there are any options at all
        if FieldChoice.objects == None:
            # Take a default list
            choice_list = [('0','-'),('1','N/A')]
        else:
            for choice in FieldChoice.objects.filter(field__iexact=field):
                choice_list.append((str(choice.machine_value),choice.english_name));

            choice_list = sorted(choice_list,key=lambda x: x[1]);
    except:
        choice_list = [('0','-'),('1','N/A')];

    # Signbank returns: [('0','-'),('1','N/A')] + choice_list
    # We do not use defaults
    return choice_list;

def choice_english(field, num):
    """Get the english name of the field with the indicated machine_number"""

    try:
        result_list = FieldChoice.objects.filter(field__iexact=field).filter(machine_value=num)
        if (result_list == None):
            return "(No results for "+field+" with number="+num
        return result_list[0].english_name
    except:
        return "(empty)"

def m2m_combi(items):
    qs = items.all()
    sBack = '-'.join([str(thing) for thing in qs])
    return sBack
  

class HelpChoice(models.Model):
    """Define the URL to link to for the help-text"""
    
    field = models.CharField(max_length=200)        # The 'path' to and including the actual field
    searchable = models.BooleanField(default=False) # Whether this field is searchable or not
    display_name = models.CharField(max_length=50)  # Name between the <a></a> tags
    help_url = models.URLField(default='')          # THe actual help url (if any)

    def __str__(self):
        return "[{}]: {}".format(
            self.field, self.display_name)

    def Text(self):
        help_text = ''
        # is anything available??
        if (self.help_url != ''):
            if self.help_url[:4] == 'http':
                help_text = "See: <a href='{}'>{}</a>".format(
                    self.help_url, self.display_name)
            else:
                help_text = "{} ({})".format(
                    self.display_name, self.help_url)
        return help_text


def get_help(field):
    """Create the 'help_text' for this element"""

    # find the correct instance in the database
    help_text = ""
    try:
        entry_list = HelpChoice.objects.filter(field__iexact=field)
        entry = entry_list[0]
        # Note: only take the first actual instance!!
        help_text = entry.Text()
    except:
        help_text = "Sorry, no help available for " + field

    return help_text
  

class Word(models.Model):
    name = models.CharField("The word", blank=False, max_length=50, help_text=get_help('word'))
    # [1] Each Word belongs exactly to one [Node]
    node = models.ForeignKey("Node", blank=False, null=False, default=1, related_name="words")

    def __str__(self):
        return self.name


class Relation(models.Model):
    name = models.TextField("Path from PP down", blank=False, help_text=get_help(RELATION_NAME))

    def __str__(self):
        return self.name


class NpType(models.Model):
    """NP type"""

    # name (1)
    name = models.CharField("NP type", choices=build_choice_list(NP_TYPE), max_length=5, help_text=get_help(NP_TYPE), default='0')
    # [1] Each NpType belongs exactly to one [Node]
    node = models.ForeignKey("Node", blank=False, null=False, default=1, related_name="nptypes")

    def __str__(self):
        return choice_english(NP_TYPE, self.name)


class Node(models.Model):
    """Nodal requirement"""

    # relation (1)
    relation = models.ForeignKey(Relation, blank=False)
    # pos (0-1)
    pos = models.CharField("Part of speech", max_length=50,  blank=True, help_text=get_help(PART_OF_SPEECH))
    # word (0-n)
    # word = models.ManyToManyField(Word, blank=True, default=1, related_name="nodem2m_word")
    # NPtype (0-n)
    # npType = models.ManyToManyField(NpType, blank=True, default=1, related_name="nodem2m_npType")
    # Other requirements
    other = models.CharField("Other", max_length=100, blank=True, help_text=get_help(OTHER_REQ))
    # [1] Each Node belongs exactly to one [Situation]
    situation = models.ForeignKey("Situation", blank=False, null=False, default=1, related_name="nodes")

    def nptypelist(self):
        """NPtype list"""
        return "-".join([choice_english(NP_TYPE, p.name) for p in self.npType.all()])

    def wordlist(self):
        """Word list"""
        return "-".join([p.name for p in self.words.all()])

    def __str__(self):
        sName = str(self.relation) + ": "
        # get POS
        pos = self.pos
        if pos != "": sName = sName + pos
        # get list of words
        #words = self.words        # m2m_combi(self.word)
        words = m2m_combi(self.words)
        if words != "": sName = sName + ", " + words
        # get list of NP types
        npTypes = m2m_combi(self.nptypes)    # m2m_combi(self.npType)
        if (npTypes != ""): sName = sName + " (" + npTypes + ")"
        # Get other requirements
        others = self.other
        if (others != ""): sName = sName + " [" + others + "]"
        return sName


class Example(models.Model):
    """Example(s)"""

    # sentence (1)
    sentence = models.TextField("Sentence", blank=False)
    # TextId (1)
    textId = models.CharField("Text ID", max_length=70,  blank=False)
    # Sentence identifier (1)
    sentId = models.CharField("Sentence ID", max_length=70, blank=False)
    # [1] Each example belongs exactly to one [Situation]
    situation = models.ForeignKey("Situation", blank=False, null=False, default=1, related_name="examples")

    def __str__(self):
        return "{}:{}".format(self.textId, self.sentId)
      

# Create your models here.
class Situation(models.Model):
    """Description of a pentaset situation"""

    # name (1)
    name = models.CharField("Name", max_length=50, blank=False)
    # preposition (0-1)
    preposition = models.CharField("Preposition", max_length=20, blank=True)
    # nodes (0-n)
    # nodes = models.ManyToManyField(Node, blank=True, default=1, related_name="situationm2m_node")
    # NPtype (1)
    npType = models.CharField("NP type", choices=build_choice_list(NP_TYPE), max_length=5, help_text=get_help(NP_TYPE), default='0')
    # Pentaset category (1)
    penta = models.CharField("Ref cat", choices=build_choice_list(PENTA_CAT), max_length=5, help_text=get_help(PENTA_CAT), default='0')
    # Antecedent (0-1)
    antecedent = models.ForeignKey(Node, help_text=get_help(PENTA_ANT), related_name='node_situation_antecedent', blank=True, null=True)
    # Action (0-1)
    action = models.CharField("Action", choices=build_choice_list(ACTION), max_length=5, help_text=get_help(ACTION), default='0')
    # Example (1-n)
    # example = models.ManyToManyField(Example, blank=False, default=1, related_name="situationm2m_example")

    def __str__(self):
        sName = "{}:{} ".format(
          choice_english(PENTA_CAT, self.penta), 
          choice_english(NP_TYPE, self.npType))
        if (self.antecedent != None): sName = sName + "ant=" + str(self.antecedent)
        if (self.preposition != ""): sName = sName + "p=" + self.preposition + " "
        sName = sName + m2m_combi(self.nodes) + " "
        return sName

    
