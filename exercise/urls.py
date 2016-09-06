from django.conf.urls import url

from course.urls import INSTANCE_URL_PREFIX, MODULE_URL_PREFIX, \
    USER_URL_PREFIX, EDIT_URL_PREFIX
from . import views, staff_views


EXERCISE_URL_PREFIX = MODULE_URL_PREFIX \
    + r'(?P<exercise_path>[\w\d\-\.\/]+)/'
SUBMISSION_URL_PREFIX = EXERCISE_URL_PREFIX \
    + r'submissions/(?P<submission_id>\d+)/'

urlpatterns = [

    # In the ordering, note that most general exercise URL has to be last.

    url(INSTANCE_URL_PREFIX + r'toc/$',
        views.TableOfContentsView.as_view(),
        name="toc"),
    url(USER_URL_PREFIX + r'results/$',
        views.ResultsView.as_view(),
        name="results"),
    url(SUBMISSION_URL_PREFIX + r'$',
        views.SubmissionView.as_view(),
        name="submission"),
    url(SUBMISSION_URL_PREFIX + r'plain/$',
        views.SubmissionPlainView.as_view(),
        name="submission-plain"),
    url(SUBMISSION_URL_PREFIX + r'poll/$',
        views.SubmissionPollView.as_view(),
        name="submission-poll"),
    url(SUBMISSION_URL_PREFIX \
            + r'file/(?P<file_id>\d+)/(?P<file_name>[\w\d\_\-\.]+)',
        views.SubmittedFileView.as_view(),
        name="submission-file"),

    url(EXERCISE_URL_PREFIX + r'submissions/$',
        staff_views.ListSubmissionsView.as_view(),
        name="submission-list"),
    url(EXERCISE_URL_PREFIX + r'submissions/create_and_assess/$',
        staff_views.CreateSubmissionView.as_view(),
        name="submission-create"),
    url(SUBMISSION_URL_PREFIX + r'inspect/$',
        staff_views.InspectSubmissionView.as_view(),
        name="submission-inspect"),
    url(SUBMISSION_URL_PREFIX + r're-submit/$',
        staff_views.ResubmitSubmissionView.as_view(),
        name="submission-re-submit"),
    url(SUBMISSION_URL_PREFIX + r'assess/$',
        staff_views.AssessSubmissionView.as_view(),
        name="submission-assess"),
    url(EDIT_URL_PREFIX + r'results/$',
        staff_views.AllResultsView.as_view(),
        name="all-results"),
    url(EDIT_URL_PREFIX + r'fetch-metadata/$',
        staff_views.FetchMetadataView.as_view(),
        name="exercise-metadata"),

    url(EXERCISE_URL_PREFIX + r'plain/$',
        views.ExercisePlainView.as_view(),
        name="exercise-plain"),
    url(EXERCISE_URL_PREFIX + r'info/model/$',
        views.ExerciseModelView.as_view(),
        name="exercise-model"),
    url(EXERCISE_URL_PREFIX + r'info/$',
        views.ExerciseInfoView.as_view(),
        name="exercise-info"),
    url(EXERCISE_URL_PREFIX + r'$',
        views.ExerciseView.as_view(),
        name="exercise"),
]
