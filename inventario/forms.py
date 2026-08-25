from django import forms


class CSVImportForm(forms.Form):
    archivo = forms.FileField(help_text='CSV UTF-8: codigo,nombre,categoria,proveedor,precio_compra,precio_venta,stock_minimo')
    def clean_archivo(self):
        archivo = self.cleaned_data['archivo']
        if not archivo.name.lower().endswith('.csv'): raise forms.ValidationError('Seleccione un archivo CSV.')
        return archivo

class CatalogoCSVImportForm(forms.Form):
    archivo = forms.FileField(help_text='Archivo CSV codificado en UTF-8.')
    def clean_archivo(self):
        archivo = self.cleaned_data['archivo']
        if not archivo.name.lower().endswith('.csv'):
            raise forms.ValidationError('Seleccione un archivo CSV.')
        return archivo
