from django import forms
from .models import MentorshipSession, Discussion


class MentorshipSessionForm(forms.ModelForm):
    class Meta:
        model = MentorshipSession
        fields = ["topic", "message", "preferred_date", "preferred_time"]
        widgets = {
            "preferred_date": forms.DateInput(attrs={"type": "date"}),
            "preferred_time": forms.TimeInput(attrs={"type": "time"}),
            "message": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ["title", "content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
