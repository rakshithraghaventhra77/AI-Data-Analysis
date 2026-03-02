from io import BytesIO
import pandas as pd
from datetime import datetime

def generate_pdf_report(df, metrics, status_dist, trends, insights):
    """
    Generate a professional PDF report of the analysis.
    Requires reportlab and PIL to be installed.
    """
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
        
        # Create PDF buffer
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        # Create styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4a8a'),
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1f4a8a'),
            spaceAfter=8,
            spaceBefore=8,
            fontName='Helvetica-Bold'
        )
        
        text_style = ParagraphStyle(
            'CustomText',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_LEFT
        )
        
        # Build story
        story = []
        
        # Title
        story.append(Paragraph("AI Powered Data Analysis Report", title_style))
        story.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}", text_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", heading_style))
        total_orders = metrics.get('total_orders', 0)
        avg_delivery = metrics.get('average_delivery_days', 0)
        late_pct = metrics.get('late_delivery_percentage', 0)
        
        summary_text = f"""
        This report provides a comprehensive analysis of the e-commerce order dataset containing {total_orders:,} orders.
        The dataset shows an average delivery time of {avg_delivery:.2f} days, with {late_pct:.2f}% of orders delivered late.
        Key performance metrics, trends, and recommendations are detailed below.
        """
        story.append(Paragraph(summary_text.strip(), text_style))
        story.append(Spacer(1, 0.15*inch))
        
        # Key Metrics
        story.append(Paragraph("Key Performance Indicators", heading_style))
        metrics_data = [
            ['Metric', 'Value'],
            ['Total Orders', f"{total_orders:,}"],
            ['Average Delivery Time', f"{avg_delivery:.2f} days"],
            ['Late Delivery Rate', f"{late_pct:.2f}%"],
            ['On-Time Delivery Rate', f"{100 - late_pct:.2f}%"]
        ]
        
        metrics_table = Table(metrics_data, colWidths=[3*inch, 2*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4a8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10)
        ]))
        story.append(metrics_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Order Status Distribution
        story.append(Paragraph("Order Status Distribution", heading_style))
        status_data = [['Status', 'Count']]
        for status, count in list(status_dist.items())[:10]:
            status_data.append([status.title(), f"{count}"])
        
        status_table = Table(status_data, colWidths=[3*inch, 2*inch])
        status_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4a8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9)
        ]))
        story.append(status_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Insights
        story.append(Paragraph("AI-Generated Insights", heading_style))
        insights_text = insights if isinstance(insights, str) else str(insights)
        story.append(Paragraph(insights_text[:500], text_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Recommendations
        story.append(Paragraph("Recommendations", heading_style))
        recommendations = [
            "Monitor late deliveries and work with logistics partners to improve on-time delivery rates.",
            "Analyze seasonal trends to optimize inventory and staffing levels.",
            "Implement automated alerts for orders exceeding estimated delivery dates.",
            "Conduct root cause analysis for canceled orders and develop mitigation strategies."
        ]
        
        for i, rec in enumerate(recommendations, 1):
            story.append(Paragraph(f"<b>{i}.</b> {rec}", text_style))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Footer
        footer_text = "© 2024 AI Powered Data Analysis Generator | Confidential"
        story.append(Paragraph(footer_text, ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey, alignment=TA_CENTER)))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    except ImportError:
        # Fallback: return None if reportlab not installed
        return None

def generate_csv_report(df, metrics, status_dist, trends, insights):
    """
    Generate a CSV export of key data.
    """
    try:
        output = BytesIO()
        
        # Combine all data into a single CSV-like format
        report_data = {
            'Metric': list(metrics.keys()),
            'Value': list(metrics.values())
        }
        
        report_df = pd.DataFrame(report_data)
        report_df.to_csv(output, index=False)
        output.seek(0)
        return output
    except Exception as e:
        return None

def get_report_downloads(df, metrics, status_dist, trends, insights):
    """
    Return available report formats and generate them.
    """
    return {
        "pdf": "PDF report with detailed analysis",
        "csv": "CSV export of data and metrics",
        "json": "JSON format of all metrics and insights"
    }
