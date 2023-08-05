from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from django.utils import timezone

def generate_pdf(vessel_instance):
    # Create a PDF buffer

    from io import BytesIO
    buffer = BytesIO()

    # Create a PDF document
    c = canvas.Canvas(buffer, pagesize=letter)

    # Set font and font size
    c.setFont("Helvetica", 12)

    # Draw text for each vessel detail
    y_position = 730  # Starting y position
    line_height = 20  # Height of each line
    details = {
        'Date': timezone.now().strftime('%d.%m.%Y'),
        'Iteration': vessel_instance.sourcePort + "  ---->  " + vessel_instance.DestinationPort,
        'Captain': vessel_instance.captain,
        'Agenty': vessel_instance.agenty,
        ':.........................................':'',
        'Total Balance': vessel_instance.getTotalBalance(),
        'Discounted': 'not yet make',
        'Extra Parking': vessel_instance.get_extra_parking(),
        'Pending Balance': vessel_instance.get_balance(),

        # Add other fields as needed
    }
    c.drawString(60, 750, f'Exit Report of {vessel_instance.launch}')
    for key, value in details.items():
        text = f"{key}: {value}"
        c.drawString(60, y_position, text)
        y_position -= line_height


    # make the Expenses table
    y_position -= line_height
    c.setFont("Helvetica-Bold", 14)
    c.drawString(60, y_position, f"Total Expenses:  AED {vessel_instance.total_expenses()}")
    y_position -= 2 * line_height

     # Draw the table headers
    table_data = [["No", "Date", "Amount", "Done By", "Note"]]

   # Assuming you have a list of expenses with date and description
    expenses = vessel_instance.vesselexpenses_set.all()
    for i, expense in enumerate(expenses, start=1):
        # Append data to the table
        row = [str(i), expense.date.strftime('%d.%m.%Y'), str(expense.amount), expense.done_by, expense.note]
        table_data.append(row)

    # Create the table
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), 'black'),
        ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), 'white'),
    ]))

    y_position -= line_height
    y_position -= 10 #half of the line
    # Draw the table on the PDF
    table.wrapOn(c, 400, 500)
    table.drawOn(c, 60, y_position)

    # make the Expenses table
    y_position -= line_height
    parking = vessel_instance.vesselparking_set.all()
    c.setFont("Helvetica", 12)
    for i in parking:
        c.drawString(60, y_position, f"Parking: {i.amount} paid for {i.days} days by {i.done_by} on {i.date.strftime('%d.%m.%Y')}.")
        y_position -= line_height
        c.drawString(60, y_position, f"Parking Note: {i.note}")
        y_position -= line_height


    exit = vessel_instance.vesselexit_set.all()

    c.setFont("Helvetica", 12)
    for e in exit:
        c.drawString(60, y_position, f"Exit: {e.amount} paid by {e.done_by} on {e.date.strftime('%d.%m.%Y')}.")
        y_position -= line_height
        c.drawString(60, y_position, f"Exit Note: {e.note}")
        y_position -= line_height


    attest = vessel_instance.vesselattestation_set.all()
    c.setFont("Helvetica", 12)
    for a in attest:
        c.drawString(60, y_position, f"Attestion: {a.amount} paid by {a.done_by} on {a.date.strftime('%d.%m.%Y')}.")
        y_position -= line_height
        c.drawString(60, y_position, f"Attestation Note: {a.note}")
        y_position -= line_height


    tc = vessel_instance.vesseltruecopy_set.all()
    c.setFont("Helvetica", 12)
    for t in tc:
        c.drawString(60, y_position, f"True Copy: {t.amount} paid by {t.done_by} on {t.date.strftime('%d.%m.%Y')}.")
        y_position -= line_height
        c.drawString(60, y_position, f"True Copy Note: {t.note}")
        y_position -= line_height


    manifest = vessel_instance.vesselmanifest_set.all()
    c.setFont("Helvetica", 12)
    for m in manifest:
        c.drawString(60, y_position, f"Manifest: {m.amount} paid by {m.done_by} on {m.date.strftime('%d.%m.%Y')}.")
        y_position -= line_height
        c.drawString(60, y_position, f"Manifest Note: {m.note}")
        y_position -= line_height


    amend = vessel_instance.vesselamend_set.all()
    c.setFont("Helvetica", 12)
    for m in amend:
        c.drawString(60, y_position, f"Amend: {m.amount} paid by {m.done_by} on {m.date.strftime('%d.%m.%Y')}.")
        y_position -= line_height
        c.drawString(60, y_position, f"Amend Note: {m.note}")
        y_position -= line_height

 
    hamali = vessel_instance.vesselhamali_set.all()
    c.setFont("Helvetica", 12)
    for h in hamali:
        c.drawString(60, y_position, f"Hammali: {h.hamal} loaded {h.hamal_loaded} container. his total hamali fees is {int(h.ctn_fees) * int(h.hamal_loaded)} AED. ")
        y_position -= line_height
        c.drawString(60, y_position, f"Loading date: {h.date.strftime('%d.%m.%Y')}")
        y_position -= line_height

    c.save()

    # Move the buffer's pointer to the beginning
    buffer.seek(0)

    # Get the content of the buffer as bytes
    pdf_content = buffer.getvalue()

    return pdf_content