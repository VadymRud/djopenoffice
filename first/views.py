from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponseBadRequest
from django import forms
from django.template import RequestContext
import django_excel as excel
from first.models import Choice


class UploadFileForm(forms.Form):
    file = forms.FileField()


def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
            return excel.make_response(filehandle.get_sheet(), "csv")
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render_to_response('upload_form.html',
                              {'form': form},
                              context_instance=RequestContext(request))


def download(request):
    sheet = excel.pe.Sheet([[1, 2], [3, 4]])
    return excel.make_response(sheet, "ods", file_name='ffff')


def embed_handson_table_from_a_single_table(request):
    """
    Renders one table in a handsontable
    """
    content = excel.pe.save_as(
        model=Choice,
        dest_file_type='handsontable.html',
        dest_embed=True)
    content.seek(0)
    return render(
        request,
        'custom-handson-table.html',
        {
            'handsontable_content': content.read()
        })
