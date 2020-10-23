from django import forms

class CommentForm(forms.Form):
    comment = forms.CharField(label = 'Your comment', max_length = 100)



class BidForm(forms.Form):
    bid = forms.IntegerField()
