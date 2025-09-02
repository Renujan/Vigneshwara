from django.shortcuts import render
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
        bill = Bill.objects.get(pk=pk)
    except Bill.DoesNotExist:
        return HttpResponse("Bill not found", status=404)

    try:
        # Prepare data
        context = {
            'company_name': 'Your Company Name',  # Replace with your company details
            'address': 'Your Company Address, City, Country',
            'phone': 'Your Company Phone',
            'email': 'Your Company Email',
            'bill_no': f"Bill #{bill.id}",
            'bill_date': bill.created_at.strftime('%d/%m/%Y %H:%M:%S'),
            'customer_name': bill.customer_name or 'No Name',
            'contact_number': bill.contact_number or 'N/A',
            'address': bill.address or 'N/A',
            'total_amount': f"{bill.total_amount:.2f}",
            'discount': f"{bill.discount:.2f}",
            'final_amount': f"{bill.final_amount:.2f}",
        }

        # Prepare bill items for table using related_name 'bill_items'
        items_data = [['Item', 'Quantity', 'Price', 'Subtotal']]
        for item in bill.bill_items.all():
            items_data.append([
                item.item.name,
                str(item.quantity),
                f"{item.item.price:.2f}",
                f"{item.subtotal:.2f}",
            ])

        # Create PDF buffer
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
        styles = getSampleStyleSheet()
        story = []

        # Header
        header_style = ParagraphStyle(
            name='HeaderStyle',
            parent=styles['Heading1'],
            fontSize=18,
            alignment=1  # Center
        )
        story.append(Paragraph(context['company_name'], header_style))
        story.append(Paragraph(context['address'], styles['Normal']))
        story.append(Paragraph(f"Phone: {context['phone']} | Email: {context['email']}", styles['Normal']))
        story.append(Spacer(1, 12))

        # Bill Details Table
        data = [
            ['Bill No:', context['bill_no']],
            ['Date:', context['bill_date']],
            ['Customer Name:', context['customer_name']],
            ['Contact Number:', context['contact_number']],
            ['Address:', context['address']],
        ]
        table = Table(data, colWidths=[100, 400])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(table)
        story.append(Spacer(1, 12))

        # Bill Items
        story.append(Paragraph("Bill Items", styles['Heading2']))
        items_table = Table(items_data, colWidths=[200, 50, 100, 100])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(items_table)
        story.append(Spacer(1, 12))

        # Totals
        totals_data = [
            ['Total Amount:', context['total_amount']],
            ['Discount:', context['discount']],
            ['Final Amount:', context['final_amount']],
        ]
        totals_table = Table(totals_data, colWidths=[100, 400])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(totals_table)
        story.append(Spacer(1, 12))

        # Build PDF
        doc.build(story)

        # Return PDF response
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=bill_{context["bill_no"]}.pdf'
        return response

    except Exception as e:
        logger.error(f"Unexpected error in download_bill_pdf: {str(e)}")
        return HttpResponse(f"Unexpected error: {str(e)}", status=500)