from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.utils.text import slugify
import uuid

class Website(models.Model):
    name = models.CharField(max_length=200)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.name)
        qr.make(fit=True)
        qrcode_img = qr.make_image(fill='black', back_color='white')

        # Create canvas and paste QR code
        canvas = Image.new('RGB', (290, 290), 'white')
        canvas.paste(qrcode_img.resize((290, 290)))

        # Ensure unique filename
        fname = f'qr_code-{slugify(self.name)}-{uuid.uuid4().hex}.png'

        # Save QR code to image field
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)

        super().save(*args, **kwargs)