"""
PDF generation for Soil Health Card
Government format using ReportLab
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from typing import Dict
import io


def generate_pdf(farmer_data: Dict, soil_data: Dict, recommendation_data: Dict) -> bytes:
    """
    Generate PDF format Soil Health Card
    Returns PDF bytes
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#4CAF50'), 
                                   spaceAfter=12, alignment=TA_CENTER, fontName='Helvetica-Bold')
    heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#2E7D32'),
                                     spaceAfter=10, fontName='Helvetica-Bold')
    
    story = []
    
    # Title
    story.append(Paragraph("SOIL HEALTH CARD", title_style))
    story.append(Paragraph("Government of India - Department of Agriculture", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Farmer Information
    story.append(Paragraph("FARMER INFORMATION", heading_style))
    farmer_table_data = [
        ['Name:', farmer_data.get('name', '')],
        ['Village:', farmer_data.get('village', '')],
        ['District:', farmer_data.get('district', '')],
        ['State:', farmer_data.get('state', '')],
        ['Field Area:', f"{farmer_data.get('field_area', '')} hectares"],
        ['Crop:', f"{farmer_data.get('crop_name', '')} ({farmer_data.get('crop_season', '')})"]
    ]
    farmer_table = Table(farmer_table_data, colWidths=[2*inch, 4*inch])
    farmer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E8F5E9')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2E7D32')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(farmer_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Table 1: Soil Analysis
    story.append(Paragraph("TABLE 1: SOIL HEALTH SUMMARY", heading_style))
    soil_headers = [['Parameter', 'Value', 'Unit', 'Status']]
    soil_rows = [
        ['Nitrogen (N)', str(soil_data.get('nitrogen', 'N/A')), 'mg/kg', get_status_text(soil_data.get('nitrogen', 0), 20, 40)],
        ['Phosphorus (P)', str(soil_data.get('phosphorus', 'N/A')), 'mg/kg', get_status_text(soil_data.get('phosphorus', 0), 15, 35)],
        ['Potassium (K)', str(soil_data.get('potassium', 'N/A')), 'mg/kg', get_status_text(soil_data.get('potassium', 0), 20, 35)],
        ['pH', str(soil_data.get('ph', 'N/A')), '–', get_ph_status_text(soil_data.get('ph', 7))],
    ]
    if soil_data.get('ec'):
        soil_rows.append(['EC', str(soil_data.get('ec')), 'dS/m', 'Normal' if soil_data.get('ec', 0) < 2 else 'High'])
    if soil_data.get('organic_carbon'):
        soil_rows.append(['Organic Carbon', str(soil_data.get('organic_carbon')), '%', 'Low' if soil_data.get('organic_carbon', 0) < 0.5 else 'Good'])
    
    soil_table = Table(soil_headers + soil_rows, colWidths=[2*inch, 1.5*inch, 1*inch, 1.5*inch])
    soil_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    story.append(soil_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Table 2: Fertilizer Recommendations
    story.append(Paragraph("TABLE 2: FERTILIZER RECOMMENDATIONS", heading_style))
    
    # Parse additional data
    import json
    additional_data = {}
    try:
        additional_data_str = recommendation_data.get('additional_data', '{}')
        if isinstance(additional_data_str, str) and '{' in additional_data_str:
            json_match = additional_data_str[additional_data_str.find('{'):]
            additional_data = json.loads(json_match)
    except:
        pass
    
    fert_headers = [['Fertilizer', 'Quantity (kg/ha)', 'Govt. Price/50kg', 'Est. Cost']]
    fert_rows = []
    
    fertilizer_details = additional_data.get('fertilizer_details', [])
    for fert in fertilizer_details:
        price_raw = fert.get('price_per_50kg', 0)
        
        # Handle unverified prices (strings like "Govt. price not available")
        if isinstance(price_raw, (int, float)):
            price = price_raw
            cost = (fert.get('quantity_kg_per_hectare', 0) / 50) * price
            price_display = f"₹{price}"
            cost_display = f"₹{int(cost)}"
        else:
            # Price is a string (not verified)
            price_display = str(price_raw)
            cost_display = "N/A"
        
        fert_rows.append([
            fert.get('fertilizer', ''),
            f"{fert.get('quantity_kg_per_hectare', 0):.2f}",
            price_display,
            cost_display
        ])
    
    fert_rows.append(['TOTAL', '', '', f"₹{recommendation_data.get('estimated_cost', 0)}"])
    
    fert_table = Table(fert_headers + fert_rows, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1*inch])
    fert_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E8F5E9')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ]))
    story.append(fert_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Important Notes
    story.append(Paragraph("IMPORTANT NOTES", heading_style))
    notes = [
        "• Soil test validity: One cropping season",
        "• Follow split application schedules as recommended",
        "• Apply during appropriate soil moisture conditions",
        "• Use FYM/compost @ 5-10 tonnes/ha for sustained soil health",
        "• Contact Krishi Vigyan Kendra (KVK) for field-specific guidance"
    ]
    for note in notes:
        story.append(Paragraph(note, styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
    
    # Footer
    story.append(Spacer(1, 0.3*inch))
    footer_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    story.append(Paragraph(footer_text, styles['Italic']))
    
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


def get_status_text(value, low, high):
    if value < low:
        return 'Low'
    elif value > high:
        return 'High'
    return 'Medium'


def get_ph_status_text(ph):
    if ph < 5.5:
        return 'Acidic'
    elif ph > 7.5:
        return 'Alkaline'
    return 'Neutral'
