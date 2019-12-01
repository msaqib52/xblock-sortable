Sortable XBlock
===========

An XBlock that implements sorting problem. Learners have to sort items by dragging them at their correct position. Authors can define items and their correct order from studio. This Xblock also supports grading.

Studio View:
![Studio view](/docs/studio-view.png)

Learners View:
![Learners view](/docs/learner-view.png)


Installation
------------

Install the requirements into the Python virtual environment of your `edx-platform` installation by running the following command from the root folder:

```bash
$ pip install -r requirements.txt
```


Enabling in Studio
------------------

You can enable the Sortable XBlock in Studio through the Advanced
Settings.

1. From the main page of a specific course, navigate to `Settings ->
   Advanced Settings` from the top menu.
2. Check for the `Advanced Module List` policy key, and add
   `"sortable"` to the policy value list.
3. Click the "Save changes" button.