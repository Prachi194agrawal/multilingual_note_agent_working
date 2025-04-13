from fpdf import FPDF
import os
from datetime import datetime

class TranscriptPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Meeting Transcript and Summary', 0, 1, 'C')
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf(transcript, summary, action_items, filename=None):
    """
    Generate a PDF report from the transcript and summary.
    
    Args:
        transcript: The full transcript text
        summary: The summary text
        action_items: List of action items
        filename: Output filename (optional)
        
    Returns:
        Path to the generated PDF file
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"meeting_summary_{timestamp}.pdf"
    
    # Ensure the output directory exists
    os.makedirs("outputs", exist_ok=True)
    output_path = os.path.join("outputs", filename)
    
    # Create PDF
    pdf = TranscriptPDF()
    pdf.add_page()
    
    # Add summary
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Summary', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 10, summary)
    pdf.ln(10)
    
    # Add action items
    if action_items:
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Action Items', 0, 1)
        pdf.set_font('Arial', '', 11)
        for item in action_items:
            pdf.cell(10, 10, chr(149), 0, 0)  # Bullet point
            pdf.multi_cell(0, 10, item)
        pdf.ln(10)
    
    # Add transcript
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Full Transcript', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 10, transcript)
    
    # Save PDF
    pdf.output(output_path)
    return output_path