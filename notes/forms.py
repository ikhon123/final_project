from django import forms
from .models import Note, Folder, Tag
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Hidden, Button, HTML, Div, Field, Row, Fieldset

class NoteForm(forms.ModelForm):
    class Meta: 
        model = Note
        fields = ('title','content','contact','deposit')
        
    
    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "noteform"
        
        folder = Div('folder', css_class="col-xs-12", style="padding:0px;")
        #self.helper.layout.pop(6) 
        #self.helper.layout.insert(6,Fieldset("Select folder",folder, Button("createfoldermodal", value="Create New Folder", css_class="btn btn-primary btn-sm col-xs-12 ", data_toggle="modal", data_target="#myModal")))
        
        
        tag = Div('tag',css_class = "col-xs-12", style="padding:0px;")
        #self.helper.layout.pop(7)
        #self.helper.layout.pop()
        #self.helper.layout.insert(7, Fieldset("Select Tag",tag, Button("createtagmodal", value="Create New Tag", css_class="btn btn-primary btn-sm col-xs-12", data_toggle="modal", data_target="#myModal2")))
        
        self.helper.layout.append(Button('btn_createnote', 'Create Note', css_class='createnote', style="margin-top:15px;"))
        self.helper.layout.append(Hidden(name='btn_createnote', value="btn_createnote"))
        
        # self.helper.layout.pop(9)
        #self.helper.layout.append(Hidden(name="user", value="4"))
        #self.helper.add_input(Submit('submit', 'Create Note'))
        
    def full_clean(self):#http://stackoverflow.com/questions/4340287/override-data-validation-on-one-django-form-element
        super(NoteForm, self).full_clean()
        if 'tag' in self._errors:
            self.cleaned_data['tag'] = []
            print("remove tag errors")
            del self._errors['tag']

class NoteFormUpdate(forms.ModelForm):
    class Meta: 
        model = Note
        #fields = '__all__'
        exclude = ['user']
        
    def __init__(self, *args, **kwargs):
        super(NoteFormUpdate, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "noteformupdate"
        
        self.helper.add_input(Submit('submit', 'Update'))

