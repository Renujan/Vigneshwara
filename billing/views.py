from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Bill
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import logging

logger = logging.getLogger(__name__)

def download_bill_pdf(request, pk):
    """
    Generate and download a PDF for a specific bill.
    """
    try:
        bill = get_object_or_404(Bill, pk=pk)
        
        # Prepare data
        context = {
            'company_name': 'Your Company Name',
            'company_address': 'Your Company Address, City, Country',  # Changed from 'address' to avoid conflict
            'phone': 'Your Company Phone',
            'email': 'Your Company Email',
            'bill_no': f"Bill #{bill.id}",
            'bill_date': bill.created_at.strftime('%d/%m/%Y %H:%M:%S'),
            'customer_name': bill.customer_name or 'No Name',
            'contact_number': bill.contact_number or 'N/A',
            'customer_address': bill.address or 'N/A',  # Changed from 'address' to avoid conflict
            'total_amount': f"{bill.total_amount:.2f}",
            'discount': f"{bill.discount:.2f}",
            'final_amount': f"{bill.final_amount:.2f}",
        }

        # Prepare bill items
        items_data = [['Item', 'Quantity', 'Price', 'Subtotal']]
        for item in bill.bill_items.all():
            items_data.append([
                item.item.name,
                str(item.quantity),
                f"{item.item.price:.2f}",
                f"{item.subtotal:.2f}",
            ])

        # Create PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Header
        story.append(Paragraph(context['company_name'], styles['Heading1']))
        story.append(Paragraph(context['company_address'], styles['Normal']))
        story.append(Paragraph(f"Phone: {context['phone']} | Email: {context['email']}", styles['Normal']))
        story.append(Spacer(1, 12))

        # Bill Details
        data = [
            ['Bill No:', context['bill_no']],
            ['Date:', context['bill_date']],
            ['Customer Name:', context['customer_name']],
            ['Contact Number:', context['contact_number']],
            ['Address:', context['customer_address']],
        ]
        table = Table(data, colWidths=[100, 300])
        story.append(table)
        story.append(Spacer(1, 12))

        # Bill Items
        story.append(Paragraph("Bill Items", styles['Heading2']))
        items_table = Table(items_data)
        story.append(items_table)
        story.append(Spacer(1, 12))

        # Totals
        totals_data = [
            ['Total Amount:', context['total_amount']],
            ['Discount:', context['discount']],
            ['Final Amount:', context['final_amount']],
        ]
        totals_table = Table(totals_data, colWidths=[100, 300])
        story.append(totals_table)

        # Build PDF
        doc.build(story)

        # Return response
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=bill_{bill.id}.pdf'
        return response

    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        return HttpResponse(f"Error generating PDF: {str(e)}", status=500)