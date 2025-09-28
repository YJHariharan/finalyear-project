"""
PDF Report Generator for DNA Alcoholism Effects Analysis
Generates comprehensive PDF reports for medical research and clinical use
"""

import io
import base64
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, red, orange, green
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import numpy as np

class PDFReportGenerator:
    """Generate comprehensive PDF reports for DNA analysis results"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Setup custom paragraph styles for the PDF report"""
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=HexColor('#1f4e79')
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=20,
            textColor=HexColor('#2e5c8a')
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=15,
            textColor=HexColor('#3e6b99'),
            borderWidth=1,
            borderColor=HexColor('#3e6b99'),
            borderPadding=5
        ))
        
        # Risk highlight styles
        self.styles.add(ParagraphStyle(
            name='HighRisk',
            parent=self.styles['Normal'],
            textColor=red,
            fontSize=11,
            leftIndent=20
        ))
        
        self.styles.add(ParagraphStyle(
            name='ModerateRisk',
            parent=self.styles['Normal'],
            textColor=orange,
            fontSize=11,
            leftIndent=20
        ))
        
        self.styles.add(ParagraphStyle(
            name='LowRisk',
            parent=self.styles['Normal'],
            textColor=green,
            fontSize=11,
            leftIndent=20
        ))
    
    def generate_comprehensive_pdf_report(self, report_data, output_buffer=None):
        """Generate a comprehensive PDF report from the analysis data"""
        
        if output_buffer is None:
            output_buffer = io.BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            output_buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Build the story (content elements)
        story = []
        
        # Add title page
        story.extend(self._create_title_page(report_data))
        story.append(PageBreak())
        
        # Add executive summary
        story.extend(self._create_executive_summary(report_data))
        story.append(PageBreak())
        
        # Add patient information
        story.extend(self._create_patient_info_section(report_data))
        
        # Add genetic analysis
        story.extend(self._create_genetic_analysis_section(report_data))
        story.append(PageBreak())
        
        # Add disease predictions
        story.extend(self._create_disease_predictions_section(report_data))
        story.append(PageBreak())
        
        # Add recommendations
        story.extend(self._create_recommendations_section(report_data))
        story.append(PageBreak())
        
        # Add monitoring schedule
        story.extend(self._create_monitoring_schedule_section(report_data))
        
        # Build PDF
        doc.build(story)
        
        output_buffer.seek(0)
        return output_buffer
    
    def _create_title_page(self, report_data):
        """Create the title page of the PDF report"""
        
        elements = []
        
        # Main title
        title = Paragraph(
            "DNA Alcoholism Effects Analysis Report",
            self.styles['CustomTitle']
        )
        elements.append(title)
        elements.append(Spacer(1, 30))
        
        # Subtitle
        subtitle = Paragraph(
            "Comprehensive Medical Assessment and Genetic Risk Analysis",
            self.styles['CustomSubtitle']
        )
        elements.append(subtitle)
        elements.append(Spacer(1, 50))
        
        # Report details
        report_info = [
            ['Report ID:', report_data.get('report_id', 'N/A')],
            ['Generated:', report_data.get('generated_at', 'N/A')],
            ['Patient Age:', report_data.get('patient_info', {}).get('age', 'N/A')],
            ['Analysis Type:', 'Individual DNA Analysis']
        ]
        
        report_table = Table(report_info, colWidths=[2*inch, 3*inch])
        report_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [HexColor('#f8f9fa'), HexColor('#ffffff')])
        ]))
        
        elements.append(report_table)
        elements.append(Spacer(1, 100))
        
        # Risk level highlight
        risk_level = report_data.get('medical_summary', {}).get('overall_risk_level', 'Unknown')
        risk_color = self._get_risk_color(risk_level)
        
        risk_highlight = Paragraph(
            f"<b>Overall Risk Level: {risk_level}</b>",
            ParagraphStyle(
                name='RiskHighlight',
                parent=self.styles['Normal'],
                fontSize=18,
                alignment=TA_CENTER,
                textColor=risk_color,
                borderWidth=2,
                borderColor=risk_color,
                borderPadding=10
            )
        )
        elements.append(risk_highlight)
        
        return elements
    
    def _create_executive_summary(self, report_data):
        """Create executive summary section"""
        
        elements = []
        
        # Section header
        header = Paragraph("Executive Summary", self.styles['SectionHeader'])
        elements.append(header)
        elements.append(Spacer(1, 20))
        
        # Medical summary data
        medical_summary = report_data.get('medical_summary', {})
        
        # Key findings
        summary_text = f"""
        This comprehensive DNA analysis evaluates alcohol-related disease risks across six organ systems. 
        The analysis incorporates genetic variants, lifestyle factors, and molecular markers to provide 
        personalized risk assessments and recommendations.
        
        <b>Key Findings:</b>
        • Overall Risk Level: {medical_summary.get('overall_risk_level', 'Unknown')}
        • Intervention Priority: {medical_summary.get('intervention_priority', 'Unknown')}
        • Monitoring Frequency: {medical_summary.get('monitoring_frequency', 'Unknown')}
        • Critical Recommendations: {medical_summary.get('critical_recommendations_count', 0)}
        """
        
        summary_para = Paragraph(summary_text, self.styles['Normal'])
        elements.append(summary_para)
        elements.append(Spacer(1, 20))
        
        # Primary concerns
        primary_concerns = medical_summary.get('primary_concerns', [])
        if primary_concerns:
            concerns_text = f"<b>Primary Concerns:</b> {', '.join(primary_concerns).title()}"
            concerns_para = Paragraph(concerns_text, self.styles['HighRisk'])
            elements.append(concerns_para)
            elements.append(Spacer(1, 10))
        
        # Secondary concerns
        secondary_concerns = medical_summary.get('secondary_concerns', [])
        if secondary_concerns:
            concerns_text = f"<b>Secondary Concerns:</b> {', '.join(secondary_concerns).title()}"
            concerns_para = Paragraph(concerns_text, self.styles['ModerateRisk'])
            elements.append(concerns_para)
        
        return elements
    
    def _create_patient_info_section(self, report_data):
        """Create patient information section"""
        
        elements = []
        
        # Section header
        header = Paragraph("Patient Information", self.styles['SectionHeader'])
        elements.append(header)
        elements.append(Spacer(1, 15))
        
        # Patient data
        patient_info = report_data.get('patient_info', {})
        
        patient_data = [
            ['Age:', patient_info.get('age', 'N/A')],
            ['Alcohol Consumption:', patient_info.get('alcohol_consumption', 'N/A')],
            ['ALDH2 Variant:', patient_info.get('aldh2_variant', 'N/A')],
            ['APOE Variant:', patient_info.get('apoe_variant', 'N/A')],
            ['CYP2E1 Activity:', str(patient_info.get('cyp2e1_activity', 'N/A'))],
            ['DNA Methylation:', str(patient_info.get('dna_methylation', 'N/A'))],
            ['Oxidative Stress:', str(patient_info.get('oxidative_stress', 'N/A'))]
        ]
        
        patient_table = Table(patient_data, colWidths=[2.5*inch, 3*inch])
        patient_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, black),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [HexColor('#f8f9fa'), HexColor('#ffffff')])
        ]))
        
        elements.append(patient_table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_genetic_analysis_section(self, report_data):
        """Create genetic analysis section"""
        
        elements = []
        
        # Section header
        header = Paragraph("Genetic Analysis", self.styles['SectionHeader'])
        elements.append(header)
        elements.append(Spacer(1, 15))
        
        genetic_analysis = report_data.get('genetic_analysis', {})
        
        # Overall genetic risk
        overall_risk = genetic_analysis.get('overall_genetic_risk', 0.0)
        risk_text = f"<b>Overall Genetic Risk Score:</b> {overall_risk:.3f}"
        risk_para = Paragraph(risk_text, self.styles['Normal'])
        elements.append(risk_para)
        elements.append(Spacer(1, 15))
        
        # ALDH2 Analysis
        aldh2_analysis = genetic_analysis.get('aldh2_analysis', {})
        aldh2_text = f"""
        <b>ALDH2 Gene Analysis:</b>
        • Variant: {aldh2_analysis.get('variant', 'N/A')}
        • Functional Status: {aldh2_analysis.get('functional_status', 'N/A')}
        • Alcohol Tolerance: {aldh2_analysis.get('alcohol_tolerance', 'N/A')}
        • Enzyme Activity: {aldh2_analysis.get('enzyme_activity', 'N/A')}
        • Risk Level: {aldh2_analysis.get('risk_level', 'N/A')}
        """
        aldh2_para = Paragraph(aldh2_text, self.styles['Normal'])
        elements.append(aldh2_para)
        elements.append(Spacer(1, 15))
        
        # APOE Analysis
        apoe_analysis = genetic_analysis.get('apoe_analysis', {})
        apoe_text = f"""
        <b>APOE Gene Analysis:</b>
        • Variant: {apoe_analysis.get('variant', 'N/A')}
        • Cardiovascular Risk: {apoe_analysis.get('cardiovascular_risk', 'N/A')}
        • Neurological Risk: {apoe_analysis.get('neurological_risk', 'N/A')}
        • Alzheimer's Risk: {apoe_analysis.get('alzheimer_risk', 'N/A')}
        • Risk Level: {apoe_analysis.get('risk_level', 'N/A')}
        """
        apoe_para = Paragraph(apoe_text, self.styles['Normal'])
        elements.append(apoe_para)
        elements.append(Spacer(1, 15))
        
        # CYP2E1 Analysis
        cyp2e1_analysis = genetic_analysis.get('cyp2e1_analysis', {})
        cyp2e1_text = f"""
        <b>CYP2E1 Enzyme Analysis:</b>
        • Activity Level: {cyp2e1_analysis.get('activity_level', 'N/A')}
        • Metabolic Rate: {cyp2e1_analysis.get('metabolic_rate', 'N/A')}
        • Alcohol Processing: {cyp2e1_analysis.get('alcohol_processing', 'N/A')}
        • Risk Level: {cyp2e1_analysis.get('risk_level', 'N/A')}
        """
        cyp2e1_para = Paragraph(cyp2e1_text, self.styles['Normal'])
        elements.append(cyp2e1_para)
        
        return elements
    
    def _create_disease_predictions_section(self, report_data):
        """Create disease predictions section"""
        
        elements = []
        
        # Section header
        header = Paragraph("Disease Risk Predictions", self.styles['SectionHeader'])
        elements.append(header)
        elements.append(Spacer(1, 15))
        
        disease_predictions = report_data.get('disease_predictions', {})
        
        # Create table for disease risks
        table_data = [['Organ System', 'Risk Score', 'Risk Percentage', 'Risk Category', 'Severity']]
        
        for organ, data in disease_predictions.items():
            risk_category = data.get('risk_category', 'Unknown')
            severity = data.get('severity_level', 'Unknown')
            
            table_data.append([
                organ.title(),
                data.get('risk_score', 'N/A'),
                data.get('risk_percentage', 'N/A'),
                risk_category,
                severity
            ])
        
        disease_table = Table(table_data, colWidths=[1.2*inch, 0.8*inch, 1*inch, 1.2*inch, 1*inch])
        disease_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, black),
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#3e6b99')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
        ]))
        
        # Add conditional row coloring based on risk
        for i, (organ, data) in enumerate(disease_predictions.items(), 1):
            risk_category = data.get('risk_category', '')
            if 'Critical' in risk_category:
                disease_table.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), HexColor('#ffebee'))]))
            elif 'High' in risk_category:
                disease_table.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), HexColor('#fff3e0'))]))
        
        elements.append(disease_table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_recommendations_section(self, report_data):
        """Create recommendations section"""
        
        elements = []
        
        # Section header
        header = Paragraph("Personalized Recommendations", self.styles['SectionHeader'])
        elements.append(header)
        elements.append(Spacer(1, 15))
        
        recommendations = report_data.get('recommendations', {})
        
        # Critical immediate recommendations
        critical_recs = recommendations.get('critical_immediate', [])
        if critical_recs:
            critical_header = Paragraph("<b>Critical - Immediate Action Required:</b>", self.styles['HighRisk'])
            elements.append(critical_header)
            for rec in critical_recs:
                rec_para = Paragraph(f"• {rec}", self.styles['HighRisk'])
                elements.append(rec_para)
            elements.append(Spacer(1, 15))
        
        # High priority recommendations
        high_priority_recs = recommendations.get('high_priority', [])
        if high_priority_recs:
            high_header = Paragraph("<b>High Priority:</b>", self.styles['ModerateRisk'])
            elements.append(high_header)
            for rec in high_priority_recs[:5]:  # Limit to top 5
                rec_para = Paragraph(f"• {rec}", self.styles['ModerateRisk'])
                elements.append(rec_para)
            elements.append(Spacer(1, 15))
        
        # Moderate priority recommendations
        moderate_recs = recommendations.get('moderate_priority', [])
        if moderate_recs:
            moderate_header = Paragraph("<b>Moderate Priority:</b>", self.styles['Normal'])
            elements.append(moderate_header)
            for rec in moderate_recs[:5]:  # Limit to top 5
                rec_para = Paragraph(f"• {rec}", self.styles['Normal'])
                elements.append(rec_para)
        
        return elements
    
    def _create_monitoring_schedule_section(self, report_data):
        """Create monitoring schedule section"""
        
        elements = []
        
        # Section header
        header = Paragraph("Recommended Monitoring Schedule", self.styles['SectionHeader'])
        elements.append(header)
        elements.append(Spacer(1, 15))
        
        monitoring = report_data.get('monitoring_schedule', {})
        
        # Immediate action
        immediate_actions = monitoring.get('immediate_action', [])
        if immediate_actions:
            immediate_header = Paragraph("<b>Immediate Action Required:</b>", self.styles['HighRisk'])
            elements.append(immediate_header)
            for action in immediate_actions:
                action_para = Paragraph(f"• {action}", self.styles['Normal'])
                elements.append(action_para)
            elements.append(Spacer(1, 10))
        
        # Monthly monitoring
        monthly_tests = monitoring.get('monthly_monitoring', [])
        if monthly_tests:
            monthly_header = Paragraph("<b>Monthly Monitoring:</b>", self.styles['Normal'])
            elements.append(monthly_header)
            for test in monthly_tests:
                test_para = Paragraph(f"• {test}", self.styles['Normal'])
                elements.append(test_para)
            elements.append(Spacer(1, 10))
        
        # Quarterly monitoring
        quarterly_tests = monitoring.get('quarterly_monitoring', [])
        if quarterly_tests:
            quarterly_header = Paragraph("<b>Quarterly Monitoring:</b>", self.styles['Normal'])
            elements.append(quarterly_header)
            for test in quarterly_tests:
                test_para = Paragraph(f"• {test}", self.styles['Normal'])
                elements.append(test_para)
            elements.append(Spacer(1, 10))
        
        # Annual monitoring
        annual_tests = monitoring.get('annual_monitoring', [])
        if annual_tests:
            annual_header = Paragraph("<b>Annual Monitoring:</b>", self.styles['Normal'])
            elements.append(annual_header)
            for test in annual_tests:
                test_para = Paragraph(f"• {test}", self.styles['Normal'])
                elements.append(test_para)
        
        return elements
    
    def _get_risk_color(self, risk_level):
        """Get color based on risk level"""
        risk_level = risk_level.lower()
        if 'high' in risk_level or 'critical' in risk_level:
            return red
        elif 'moderate' in risk_level:
            return orange
        else:
            return green
    
    def generate_research_dataset_export(self, batch_results, filename_prefix="research_dataset"):
        """Generate comprehensive research dataset export in multiple formats"""
        
        import pandas as pd
        
        # Create comprehensive dataset
        dataset = []
        
        for result in batch_results:
            record = {
                'patient_id': result.get('patient_id', ''),
                'age': result.get('age', ''),
                'alcohol_percentage': result.get('alcohol_percentage', ''),
                'gender': result.get('gender', ''),
                'aldh2_variant': result.get('aldh2_variant', ''),
                'apoe_variant': result.get('apoe_variant', ''),
                'cyp2e1_activity': result.get('cyp2e1_activity', ''),
                'dna_methylation': result.get('dna_methylation', ''),
                'oxidative_stress': result.get('oxidative_stress', ''),
                'bmi': result.get('bmi', ''),
                'years_drinking': result.get('years_drinking', ''),
                'lifestyle_score': result.get('lifestyle_score', ''),
                'family_history_heart': result.get('family_history_heart', ''),
                'family_history_liver': result.get('family_history_liver', ''),
                'family_history_kidney': result.get('family_history_kidney', ''),
                'heart_disease_risk': result.get('heart_risk', ''),
                'liver_disease_risk': result.get('liver_risk', ''),
                'kidney_disease_risk': result.get('kidney_risk', ''),
                'brain_disease_risk': result.get('brain_risk', ''),
                'pancreas_disease_risk': result.get('pancreas_risk', ''),
                'lung_disease_risk': result.get('lung_risk', ''),
                'heart_confidence': result.get('heart_confidence', ''),
                'liver_confidence': result.get('liver_confidence', ''),
                'kidney_confidence': result.get('kidney_confidence', ''),
                'brain_confidence': result.get('brain_confidence', ''),
                'pancreas_confidence': result.get('pancreas_confidence', ''),
                'lung_confidence': result.get('lung_confidence', ''),
                'genetic_risk_score': result.get('genetic_risk_score', ''),
                'environmental_risk_score': result.get('environmental_risk_score', ''),
                'composite_risk_score': result.get('composite_risk_score', ''),
                'timestamp': datetime.now().isoformat()
            }
            dataset.append(record)
        
        # Create DataFrame
        df = pd.DataFrame(dataset)
        
        # Generate multiple export formats
        exports = {}
        
        # CSV export
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        exports['csv'] = csv_buffer.getvalue()
        
        # JSON export
        json_buffer = io.StringIO()
        df.to_json(json_buffer, orient='records', indent=2)
        exports['json'] = json_buffer.getvalue()
        
        # Excel export
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Raw_Data', index=False)
            
            # Create summary statistics sheet
            summary_stats = df.describe()
            summary_stats.to_excel(writer, sheet_name='Summary_Statistics')
            
            # Create correlation matrix sheet
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            correlation_matrix = df[numeric_cols].corr()
            correlation_matrix.to_excel(writer, sheet_name='Correlations')
        
        excel_buffer.seek(0)
        exports['excel'] = excel_buffer.getvalue()
        
        return exports