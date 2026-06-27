from django import forms
from .models import StartupIdea, Category


class StartupIdeaForm(forms.ModelForm):
    class Meta:
        model = StartupIdea
        fields = [
            "startup_name",
            "founder_name",
            "category",
            "industry",
            "problem_statement",
            "proposed_solution",
            "target_customers",
            "business_model",
            "revenue_model",
            "competitor_analysis",
            "unique_selling_proposition",
            "required_investment",
            "team_members",
            "expected_timeline",
            "pitch_deck",
            "logo",
        ]
        widgets = {
            "problem_statement": forms.Textarea(attrs={"rows": 4}),
            "proposed_solution": forms.Textarea(attrs={"rows": 4}),
            "target_customers": forms.Textarea(attrs={"rows": 3}),
            "business_model": forms.Textarea(attrs={"rows": 3}),
            "revenue_model": forms.Textarea(attrs={"rows": 3}),
            "competitor_analysis": forms.Textarea(attrs={"rows": 4}),
            "unique_selling_proposition": forms.Textarea(attrs={"rows": 3}),
            "team_members": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
        self.fields["category"].queryset = Category.objects.all()
        self.fields["category"].empty_label = "Select Category"
