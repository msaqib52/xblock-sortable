"""TO-DO: Write a description of what this XBlock is."""
import json
import urllib
import pkg_resources
import random
from xblock.core import XBlock
from xblock.exceptions import JsonHandlerError
from xblock.fields import Integer, Scope, String, List, Boolean
from xblock.fragment import Fragment

from xblockutils.resources import ResourceLoader


loader = ResourceLoader(__name__)


def _(text):
    """no-op function to scrape strings for i18n"""
    return text


def ngettext_fallback(text_singular, text_plural, number):
    """ Dummy `ngettext` replacement to make string extraction tools scrape strings marked for translation """
    if number == 1:
        return text_singular
    else:
        return text_plural


class DummyTranslationService(object):
    """
    Dummy drop-in replacement for i18n XBlock service
    """
    gettext = _
    ngettext = ngettext_fallback


@XBlock.needs('i18n')
class SortableXBlock(XBlock):
    """
    An XBlock for sorting problems.
    """
    DEFAULT_DATA = [
        {'position': 1, 'text': "Item at position 1"},
        {'position': 2, 'text': "Item at position 2"},
        {'position': 3, 'text': "Item at position 3"},
        {'position': 4, 'text': "Item at position 4"},
        {'position': 5, 'text': "Item at position 5"},
    ]

    has_score = True

    display_name = String(
        display_name=_("Title"),
        help=_("The title of the sorting problem. The title is displayed to learners."),
        scope=Scope.settings,
        default=_("Sorting Problem"),
        enforce_type=True,
    )

    question_text = String(
        display_name=_("Problem text"),
        help=_("The description of the problem or instructions shown to the learner."),
        scope=Scope.settings,
        default="",
        enforce_type=True,
    )

    max_attempts = Integer(
        display_name=_("Maximum attempts"),
        help=_(
            "Defines the number of times a student can try to answer this problem. "
            "If the value is not set, infinite attempts are allowed."
        ),
        scope=Scope.settings,
        default=3,
        enforce_type=True,
    )

    attempts = Integer(
        help=_("Number of attempts learner used"),
        scope=Scope.user_state,
        default=0,
        enforce_type=True,
    )

    item_background_color = String(
        display_name=_("Item background color"),
        help=_("The background color of sortable items"),
        scope=Scope.settings,
        default="#0075b4",
        enforce_type=True,
    )

    item_text_color = String(
        display_name=_("Item text color"),
        help=_("The text color of sortable items"),
        scope=Scope.settings,
        default="#ffffff",
        enforce_type=True,
    )

    completed = Boolean(
        help=_("Indicates whether a learner has completed the problem successfully at least once"),
        scope=Scope.user_state,
        default=False,
        enforce_type=True,
    )

    data = List(
        display_name=_("Sortable Items"),
        help=_(
            "Order will be randomized when presented to students"
        ),
        scope=Scope.content,
        default=DEFAULT_DATA,
        enforce_type=True,
    )

    @property
    def remaining_attempts(self):
        return self.max_attempts - self.attempts
    

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def student_view(self, context=None):
        """
        The primary view of the SortableXBlock, shown to students
        when viewing courses.
        """
        frag = Fragment()
        items = self.data[:]
        if not self.completed:
            random.shuffle(items)
        frag.add_content(loader.render_django_template(
            'static/html/sortable.html',
            context=dict(items=items, self=self),
            i18n_service=self.i18n_service)
        )
        frag.add_css(self.resource_string("static/css/sortable.css"))
        frag.add_javascript(self.resource_string("static/js/vendor/jquery-sortable.js"))
        frag.add_javascript(self.resource_string("static/js/src/sortable.js"))

        frag.initialize_js('SortableXBlock')
        return frag

    @XBlock.json_handler
    def submit_answer(self, data, suffix=''):
        """
        Checks submitted solution and returns feedback.
        """
        if self.remaining_attempts == 0:
            raise JsonHandlerError(409, "Max number of attempts reached")

        self.attempts += 1
        self.runtime.publish(self, "progress", {})
        correct = (data == [int(item['position']) for item in self.data])
        if correct:
            self.completed = True
            self.runtime.publish(self, "grade", {'value': 1.0, 'max_value': 1.0})
            feedback_message = 'Congratulations, Your answer is correct!'
        else:
            feedback_message = 'Incorrect answer!'
        
        return {
            'correct': correct,
            'remaining_attempts': self.remaining_attempts,
            'message': feedback_message,
        }

    def studio_view(self, context):
        """
        Editing view in Studio
        """
        frag = Fragment()
        context = {
            'self': self,
            'fields': self.fields, 
            'data': self.data,
        }
        frag.add_content(loader.render_django_template(
            'static/html/sortable_edit.html',
            context=context,
            i18n_service=self.i18n_service)
        )
        frag.add_css(self.resource_string("static/css/sortable_edit.css"))
        frag.add_javascript(self.resource_string("static/js/src/sortable_edit.js"))

        frag.initialize_js('SortableXBlockEdit')
        return frag

    @XBlock.json_handler
    def studio_submit(self, submissions, suffix=''):
        """
        Handles studio save.
        """
        self.display_name = submissions['display_name']
        self.max_attempts = submissions['max_attempts']
        self.question_text = submissions['question_text']
        self.item_background_color = submissions['item_background_color']
        self.item_text_color = submissions['item_text_color']
        self.data = submissions['data']

        return {
            'result': 'success',
        }

    @property
    def i18n_service(self):
        """ Obtains translation service """
        i18n_service = self.runtime.service(self, "i18n")
        if i18n_service:
            return i18n_service
        else:
            return DummyTranslationService()

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("SortableXBlock",
             """<sortable/>
             """),
            ("Multiple SortableXBlock",
             """<vertical_demo>
                <sortable/>
                <sortable/>
                <sortable/>
                </vertical_demo>
             """),
        ]
