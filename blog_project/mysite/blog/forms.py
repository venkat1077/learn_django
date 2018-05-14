from django import forms
from blog.models import Post, Comment


class PostForm(forms.ModelForm):

    # Meta class is to provide metadata to the ModelForms class(PostForm in this case)
    class Meta():
        # model attribute to to create a form(for Post model here)
        model = Post
        # fields attribute to spcify the fields to be included in the form
        # (to include the specified fields)
        fields = ('author', 'title', 'text')

        # creating widgets for form fields(styling)
        widgets = {
             # connect widgets to css styling
             # explanation: title field is connected to one(testinputclass) css class
             # TextInput & TextArea are widgets here
            'title':forms.TextInput(attrs={'class':'testinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }

class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('author', 'text')

        widgets = {
            'author':forms.TextInput(attrs={'class':'testinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
        }
