from django.forms import ModelForm
from django import forms
from .models import Vehicle, Driver, FuelTap, Ballot, BuyOrder, FuelOrder
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django.utils import timezone
import datetime
import pytz
from django.core.exceptions import ValidationError

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

        self.fields['dni'].widget.attrs.update({'autofocus': 'autofocus'})

        if self.instance.name:  
            self.fields['dni'].widget.attrs['readonly'] = True
            self.fields['dni'].widget.attrs.pop('autofocus', None)


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
        fields = ['plate','type','name','brand','chassis','model','production','fuel','mileage','hourometer','soat','citv', 'available', 'justify']

        widgets = {
            'soat': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
            'citv': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
            'justify': forms.Textarea(attrs={'rows': 1}),
            'production': forms.NumberInput(attrs={'min': 1975, 'max': datetime.datetime.now().year}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['type'].widget.attrs.update({'autofocus': 'autofocus'})

        if self.instance.plate:  
            self.fields['plate'].widget.attrs['readonly'] = True
            self.fields['type'].widget.attrs['readonly'] = True
            self.fields['type'].widget.attrs.pop('autofocus', None)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'card card-body mb-5'
        self.helper.layout = Layout(
            Row(
                Column('type', css_class='form-group col-md-4 mb-0'),
                Column('plate', css_class='form-group col-md-4 mb-0'),
                Column('name', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('brand', css_class='form-group col-md-4 mb-0'),
                Column('model', css_class='form-group col-md-4 mb-0'),
                Column('chassis', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('production', css_class='form-group col-md-4 mb-0'),
                Column('fuel', css_class='form-group col-md-4 mb-0'),
                Column('mileage', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('hourometer', css_class='form-group col-md-4 mb-0'),
                Column('soat', css_class='form-group col-md-4 mb-0'),
                Column('citv', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('available', css_class='form-group col-md-4 mb-0'),
                Column('justify', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Guardar', css_class='btn btn-primary')
        )

        self.fields['type'].empty_label = 'Escoge clase...'
        self.fields['fuel'].empty_label = 'Escoge combustible...'



# FUELTAP FORM --------------------------------------------------------------------

class FuelTapForm(ModelForm):

    class Meta:     
        model = FuelTap
        fields = ['ruc','business_name','address','email','phone']

        widgets = {
                'business_name': forms.Textarea(attrs={'rows': 1}),
                'address': forms.Textarea(attrs={'rows': 1}),
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['ruc'].widget.attrs.update({'autofocus': 'autofocus'})
        self.fields['email'].widget = forms.EmailInput(attrs={'type': 'email'})

        if self.instance.business_name:  
            self.fields['ruc'].widget.attrs['readonly'] = True
            self.fields['ruc'].widget.attrs.pop('autofocus', None)


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
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('phone', css_class='form-group col-md-6 mb-0'),
                # Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Guardar', css_class='btn btn-primary')
        )



# BUY ORDER FORM --------------------------------------------------------------------

class BuyOrderForm(ModelForm):

    class Meta:     
        model = BuyOrder
        fields = ['order','user_area','fuel','stock','date','fueltap']

        widgets = {
                'date': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
                'detail': forms.Textarea(attrs={'rows': 1}),
                'user_area': forms.Textarea(attrs={'rows': 1}),
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['order'].widget.attrs.update({'autofocus': 'autofocus'})

        if self.instance.user_area:  
            self.fields['order'].widget.attrs['readonly'] = True
            self.fields['stock'].widget.attrs['readonly'] = True
            self.fields['order'].widget.attrs.pop('autofocus', None)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'card card-body mb-5'
        self.helper.layout = Layout(
            Row(
                Column('order', css_class='form-group col-md-6 mb-0'),
                Column('user_area', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('fueltap', css_class='form-group col-md-6 mb-0'),
                Column('fuel', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('stock', css_class='form-group col-md-6 mb-0'),
                Column('date', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Guardar', css_class='btn btn-primary')
        )

        self.fields['fueltap'].empty_label = 'Escoge proveedor...'
        self.fields['fuel'].empty_label = 'Escoge combustible...'



# FUEL ORDER FORM --------------------------------------------------------------------

class FuelOrderForm(ModelForm):

    driver = forms.ModelChoiceField(
    queryset=Driver.objects.filter(available=True),
    label='Conductor',
    required=False,
    )

    plate = forms.ModelChoiceField(
        queryset=Vehicle.objects.filter(available=True),
        label='Placa',
        required=False,
    )

    class Meta:     
        model = FuelOrder
        fields = ['fueltap','order','user_area','driver','plate','brand','vehicle','place','reason','quantity','fuel','voucher','date','fuel_loan','fuel_return','detail','residue_buy_order']

        widgets = {
                'date': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
                'user_area': forms.Textarea(attrs={'rows': 1}),
                'detail': forms.Textarea(attrs={'rows': 1}),
                'reason': forms.Textarea(attrs={'rows': 1}),
                'fueltap': forms.Textarea(attrs={'rows': 1}),
                'place': forms.Textarea(attrs={'rows': 1}),
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['order'].widget.attrs.update({'autofocus': 'autofocus'})
        self.fields['user_area'].widget.attrs.update({
        'readonly': 'readonly',
        'style': 'background-color: #e9ecef;'  
        })
        self.fields['fueltap'].widget.attrs.update({
        'readonly': 'readonly',
        'style': 'background-color: #e9ecef;',
        })
        self.fields['brand'].widget.attrs.update({
        'readonly': 'readonly',
        'style': 'background-color: #e9ecef; pointer-events: none;',
        })
        self.fields['fuel'].widget.attrs.update({
        'readonly': 'readonly',
        'style': 'background-color: #e9ecef; pointer-events: none;',
        })
        self.fields['vehicle'].widget.attrs.update({
        'readonly': 'readonly',
        'style': 'background-color: #e9ecef; pointer-events: none;',
        })
        self.fields['residue_buy_order'].widget.attrs.update({
        'readonly': 'readonly',
        'style': 'background-color: #e9ecef; pointer-events: none;',
        })

        # if self.instance.code:  
        #     self.fields['order'].widget.attrs.pop('autofocus', None)
        #     self.fields['brand'].widget.attrs['readonly'] = True
        #     self.fields['fueltap'].widget.attrs['readonly'] = True
        #     self.fields['fuel'].widget.attrs['readonly'] = True
        #     self.fields['vehicle'].widget.attrs['readonly'] = True
        #     self.fields['quantity'].widget.attrs['readonly'] = True
        #     self.fields['fuel_loan'].widget.attrs['readonly'] = True
        #     self.fields['fuel_return'].widget.attrs['readonly'] = True


        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'card card-body mb-5'
        self.helper.layout = Layout(
            Row(
                Column('fuel_loan', css_class='form-group col-md-4 mb-0'),
                Column('fuel_return', css_class='form-group col-md-4 mb-0'),
                Column('residue_buy_order', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('order', css_class='form-group col-md-4 mb-0'),
                Column('user_area', css_class='form-group col-md-8 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('fueltap', css_class='form-group col-md-4 mb-0'),
                Column('driver', css_class='form-group col-md-4 mb-0'),
                Column('plate', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('brand', css_class='form-group col-md-4 mb-0'),
                Column('vehicle', css_class='form-group col-md-4 mb-0'),
                Column('fuel', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('quantity', css_class='form-group col-md-4 mb-0'),
                Column('voucher', css_class='form-group col-md-4 mb-0'),
                Column('date', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('place', css_class='form-group col-md-4 mb-0 place-container'),
                Column('reason', css_class='form-group col-md-8 mb-0 reason-container'),
                Column('detail', css_class='form-group col-md-12 mb-0 detail-container'),
                css_class='form-row'
            ),
            Submit('submit', 'Guardar', css_class='btn btn-primary')
        )

        self.fields['fueltap'].empty_label = 'Escoge proveedor...'
        self.fields['order'].empty_label = 'Escoge orden...'
        self.fields['driver'].empty_label = 'Escoge conductor...'
        self.fields['plate'].empty_label = 'Escoge placa...'
        self.fields['fuel'].empty_label = 'Escoge combustible...'



# BALLOT FORM --------------------------------------------------------------------

class BallotForm(ModelForm):

    driver = forms.ModelChoiceField(
        queryset=Driver.objects.filter(available=True),
        label='Conductor',
    )

    plate = forms.ModelChoiceField(
        queryset=Vehicle.objects.filter(available=True),
        label='Placa',
    )

    class Meta:     
        model = Ballot
        fields = ['driver','driver_license','driver_category','drive_to','plate', 'vehicle_name','vehicle_brand','place','reason','exit_date','exit_time']

        widgets = {
            'driver_license': forms.TextInput(attrs={'readonly': 'readonly'}),
            'driver_category': forms.TextInput(attrs={'readonly': 'readonly'}),
            'vehicle_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'vehicle_brand': forms.TextInput(attrs={'readonly': 'readonly'}),
            'reason': forms.Textarea(attrs={'rows': 1}),
            'drive_to': forms.Textarea(attrs={'rows': 1}),
            'place': forms.Textarea(attrs={'rows': 1}),
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
                Column('driver', css_class='form-group col-md-4 mb-0'),
                Column('driver_license', css_class='form-group col-md-4 mb-0'),
                Column('driver_category', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('plate', css_class='form-group col-md-4 mb-0'),
                Column('vehicle_brand', css_class='form-group col-md-4 mb-0'),
                Column('vehicle_name', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('drive_to', css_class='form-group col-md-8 mb-0'),
                Column('place', css_class='form-group col-md-4 mb-0'),
                Column('reason', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('exit_date', css_class='form-group col-md-4 mb-0'),
                Column('exit_time', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Guardar', css_class='btn btn-primary')
        )

        self.fields['driver'].empty_label = 'Escoge conductor...'
        self.fields['plate'].empty_label = 'Escoge placa...'

    def clean(self):
        cleaned_data = super().clean()
        driver = cleaned_data.get('driver')
        plate = cleaned_data.get('plate')
        exit_date = cleaned_data.get('exit_date')
        exit_time = cleaned_data.get('exit_time')

        if exit_date and exit_time:
            # exit_datetime = timezone.make_aware(datetime.datetime.combine(exit_date, exit_time), timezone.get_current_timezone())
            exit_datetime = timezone.make_aware(datetime.datetime.combine(exit_date, exit_time), timezone=pytz.timezone('America/Lima'))

            if exit_datetime < timezone.now():
                raise ValidationError('Fecha y hora de salida no pueden ser anteriores a la fecha y hora actual.')

            if driver and Ballot.objects.filter(driver=driver, exit_date=exit_date, exit_time=exit_time).exclude(id=self.instance.id).exists():
                raise ValidationError('Ya existe un registro para el conductor en esta fecha y hora.')

            if plate and Ballot.objects.filter(plate=plate, exit_date=exit_date, exit_time=exit_time).exclude(id=self.instance.id).exists():
                raise ValidationError('Ya existe un registro para el vehículo en esta fecha y hora.')

        return cleaned_data
