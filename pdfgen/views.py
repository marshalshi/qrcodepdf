from django.shortcuts import render

import qrcode
from reportlab.pdfgen import canvas
from django.http import HttpResponse

import StringIO
from reportlab.lib.units import inch, cm
from reportlab.lib.utils import ImageReader
def some_view(request):

    code_string = "Hello World"
    # make qrcode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=200,
    )
    qr.add_data(code_string)
    qr.make(fit=True)
    
    img = qr.make_image()

    
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    
    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw code on PDF
    imgdata = StringIO.StringIO()
    img.save(imgdata)
    imgdata.seek(0)
    image = ImageReader(imgdata)
    p.drawImage(image, 200, 500, 200, 200)
    
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    # position at 100*100
    p.drawString(270, 500, code_string)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response
