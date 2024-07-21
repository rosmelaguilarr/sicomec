from django.forms import ModelForm
from django import forms
from .models import Vehicle, Driver, FuelTap, Ballot, LicenseCategory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit


# DRIVER FORM --------------------------------------------------------------------

class DriverForm(ModelForm):

    class Meta:     
        model = Driver
        fields = ['dni', 'name','last_name', 'license', 'category', 'expiration', 'available', 'justify']

        widgets = {
            'expiration': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
            'justify': forms.Textarea(attrs={'rows': 1}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.name:  
            self.fields['dni'].widget.attrs['readonly'] = True

        self.fields['dni'].widget.attrs.update({'autofocus': 'autofocus'})

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'card card-body mb-5'
        self.helper.layout = Layout(
            Row(
                Column('dni', css_class='form-group col-md-6 mb-0'),
                Column('name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                Column('license', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                
                Column('category', css_class='form-group col-md-6 mb-0'),
                Column('expiration', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                
                Column('available', css_class='form-group col-md-6 mb-0'),
                Column('justify', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Guardar', css_class='btn btn-primary')
        )

        self.fields['category'].empty_label = 'Escoge categoría...'



# VIHICLE FORM --------------------------------------------------------------------

class VehicleForm(ModelForm):

    class Meta:     
        model = Vehicle
        fields = ['plate','type','name','brand','chassis','model','production','fuel','mileage','hourometer','soat','citv']

        widgets = {
            'production': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
            'soat': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
            'citv': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['plate'].widget.attrs.update({'autofocus': 'autofocus'})

        if self.instance.brand:  
            self.fields['plate'].widget.attrs['readonly'] = True
            self.fields['type'].widget.attrs['readonly'] = True

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'card card-body mb-5'
        self.helper.layout = Layout(
            Row(
                Column('plate', css_class='form-group col-md-6 mb-0'),
                Column('type', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('brand', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('model', css_class='form-group col-md-6 mb-0'),
                Column('chassis', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('production', css_class='form-group col-md-6 mb-0'),
                Column('fuel', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('mileage', css_class='form-group col-md-6 mb-0'),
                Column('hourometer', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('soat', css_class='form-group col-md-6 mb-0'),
                Column('citv', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),

            Submit('submit', 'Guardar', css_class='btn btn-primary')
        )

        self.fields['type'].empty_label = 'Escoge tipo...'
        self.fields['fuel'].empty_label = 'Escoge combustible...'



# FUELTAP FORM --------------------------------------------------------------------

class FuelTapForm(ModelForm):

    class Meta:     
        model = FuelTap
        fields = ['ruc','business_name','address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['ruc'].widget.attrs.update({'autofocus': 'autofocus'})

        if self.instance.business_name:  
            self.fields['ruc'].widget.attrs['readonly'] = True

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'card card-body mb-5'
        self.helper.layout = Layout(
            Row(
                Column('ruc', css_class='form-group col-md-6 mb-0'),
                Column('business_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('address', css_class='form-group col-md-6 mb-0'),
                # Column('license', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Guardar', css_class='btn btn-primary')
        )



# BALLOT FORM --------------------------------------------------------------------

class BallotForm(ModelForm):

    class Meta:     
        model = Ballot
        fields = ['driver_name','driver_last_name','driver_license','driver_category','drive_to','vehicle_plate', 'vehicle_name','vehicle_brand','place','reason','exit_date','exit_time']

        widgets = {
            'driver_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'driver_last_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'driver_license': forms.TextInput(attrs={'readonly': 'readonly'}),
            'driver_category': forms.TextInput(attrs={'readonly': 'readonly'}),
            'vehicle_plate': forms.TextInput(attrs={'readonly': 'readonly'}),
            'vehicle_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'vehicle_brand': forms.TextInput(attrs={'readonly': 'readonly'}),
            'reason': forms.Textarea(attrs={'rows': 1}),

            'exit_date': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
            'exit_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'card card-body mb-5'
        self.helper.layout = Layout(
            Row(
                Column('driver_name', css_class='form-group col-md-6 mb-0'),
                Column('driver_last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('driver_license', css_class='form-group col-md-6 mb-0'),
                Column('driver_category', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('drive_to', css_class='form-group col-md-6 mb-0'),
                Column('vehicle_plate', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('vehicle_name', css_class='form-group col-md-6 mb-0'),
                Column('vehicle_brand', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('place', css_class='form-group col-md-6 mb-0'),
                Column('reason', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('exit_date', css_class='form-group col-md-6 mb-0'),
                Column('exit_time', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Guardar', css_class='btn btn-primary')
        )
