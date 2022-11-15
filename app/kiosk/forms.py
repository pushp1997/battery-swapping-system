from django import forms


class UserForm(forms.Form):
    email = forms.EmailField(label="Email:", max_length=100, required=True, help_text="Enter email")
    your_name = forms.CharField(
        label="Full Name:", max_length=100, required=True, help_text="Enter your full name"
    )
