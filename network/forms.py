from django import forms


class PostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(
        attrs={'autofocus': 'autofocus', "placeholder": "What is going on?", "rows": 3, "class": "form-control"}), required=True, max_length=500)


class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(
        attrs={"placeholder": "Send your answer", "rows": 2, "class": "form-control"}), required=True, max_length=500)
