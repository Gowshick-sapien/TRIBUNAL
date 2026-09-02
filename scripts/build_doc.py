import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def set_cell_background(cell, fill_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_document(output_path):
    doc = docx.Document()
    
    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Base Font
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Calibri'
    font.size = Pt(11)
    font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    # Document Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run_title = p_title.add_run('TRIBUNAL End-to-End Investigation Walkthrough')
    run_title.font.name = 'Segoe UI'
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x0F, 0x29, 0x4A) # Dark Navy Header

    p_sub = doc.add_paragraph()
    run_sub = p_sub.add_run('Visual Companion & Screenshot Evaluation Guide')
    run_sub.font.name = 'Segoe UI'
    run_sub.font.size = Pt(13)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    # Metadata Info Box Table
    meta_table = doc.add_table(rows=1, cols=1)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = meta_table.cell(0, 0)
    set_cell_background(cell, 'F0F4F8')
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    p_meta = cell.paragraphs[0]
    p_meta.paragraph_format.space_after = Pt(0)
    r_meta = p_meta.add_run('Document Type: Hackathon Jury & Evaluation Visual Guide  |  System Version: v2.0  |  Platform: TRIBUNAL AI Multi-Expert')
    r_meta.font.size = Pt(9.5)
    r_meta.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
    r_meta.font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Intro Paragraph
    p_intro = doc.add_paragraph()
    p_intro.add_run('This visual companion guide provides a step-by-step evaluation protocol for testing TRIBUNAL\'s autonomous multi-expert legal/investigative framework. Use the formatted screenshot containers below to paste high-resolution images from each evaluation step.')

    # Helper function for custom styled headings
    def add_custom_heading(text, level=1):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(text)
        run.font.name = 'Segoe UI'
        run.font.bold = True
        if level == 1:
            run.font.size = Pt(15)
            run.font.color.rgb = RGBColor(0x0F, 0x29, 0x4A)
        elif level == 2:
            run.font.size = Pt(13)
            run.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
        return p

    # Helper function for screenshot container box
    def add_screenshot_box(step_num, step_title, caption_text):
        tbl = doc.add_table(rows=2, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # Row 0: Placeholder Area
        cell_img = tbl.cell(0, 0)
        set_cell_background(cell_img, 'FAFAFA')
        set_cell_margins(cell_img, top=400, bottom=400, left=200, right=200)
        p_img = cell_img.paragraphs[0]
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_box = p_img.add_run(f'[ INSERT SCREENSHOT HERE: {step_title.upper()} ]')
        r_box.font.name = 'Consolas'
        r_box.font.size = Pt(11)
        r_box.font.bold = True
        r_box.font.color.rgb = RGBColor(0x71, 0x80, 0x96)
        
        p_subbox = cell_img.add_paragraph()
        p_subbox.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_hint = p_subbox.add_run('(Paste high-resolution screenshot into this container or replace placeholder text)')
        r_hint.font.size = Pt(9)
        r_hint.font.italic = True
        r_hint.font.color.rgb = RGBColor(0xA0, 0xAE, 0xC0)
        
        # Row 1: Caption Area
        cell_cap = tbl.cell(1, 0)
        set_cell_background(cell_cap, 'EDF2F7')
        set_cell_margins(cell_cap, top=100, bottom=100, left=200, right=200)
        p_cap = cell_cap.paragraphs[0]
        p_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_cap_label = p_cap.add_run(f'Figure {step_num}: ')
        r_cap_label.font.bold = True
        r_cap_label.font.size = Pt(9.5)
        r_cap_label.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
        r_cap_txt = p_cap.add_run(caption_text)
        r_cap_txt.font.size = Pt(9.5)
        r_cap_txt.font.italic = True
        r_cap_txt.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

        doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # --- Step 1 ---
    add_custom_heading('Step 1: Launch System & Open Dashboard', level=1)
    p = doc.add_paragraph()
    p.add_run('1. Open terminal and launch FastAPI backend service (`uvicorn api.app:app --port 8000`).\n')
    p.add_run('2. Open React dashboard in browser (`http://localhost:5173`).\n')
    p.add_run('3. Verification Point: Verify top navigation header displays green "API Connected" status indicator.')
    add_screenshot_box(1, 'System Launch & Dashboard Homepage', 'TRIBUNAL Multi-Expert Web Dashboard homepage showing connected API status header.')

    # --- Step 2 ---
    add_custom_heading('Step 2: Select Pre-Configured Evaluation Scenario', level=1)
    p = doc.add_paragraph()
    p.add_run('1. Click on the "Sample Queries" dropdown in the top navigation search header.\n')
    p.add_run('2. Choose Scenario A (ACC-90812 — Structuring Sweep), Scenario B (ACC-10492 — Dormancy Reactivation), or Scenario C (ACC-44910 — Shell Counterparty Sweep).\n')
    p.add_run('3. Click "Investigate" to trigger the multi-expert pipeline execution.')
    add_screenshot_box(2, 'Sample Queries & Search Header', 'Top navigation search bar displaying sample scenarios dropdown menu and Investigate button.')

    # --- Step 3 ---
    add_custom_heading('Step 3: Inspect Multi-Expert Panel Findings', level=1)
    p = doc.add_paragraph()
    p.add_run('Examine the three domain expert reasoning cards rendered in the main workspace:\n')
    p.add_run('• Financial Expert Card: Flags structuring transactions under $10,000, velocity spikes, and transfer volumes.\n')
    p.add_run('• Behavioral Expert Card: Compares historical baselines, account dormancy reactivation (>180 days), and payment method drift.\n')
    p.add_run('• Defense Agent Rebuttal Card: Cross-examines findings against commercial exceptions (payroll, vendor contracts) to rebut false positives.')
    add_screenshot_box(3, 'Multi-Expert Findings Cards', 'Workspace panel cards for Financial Expert, Behavioral Expert, and Defense Agent showing findings and rebuttal arguments.')

    # --- Step 4 ---
    add_custom_heading('Step 4: Navigate Interactive Evidence Graph', level=1)
    p = doc.add_paragraph()
    p.add_run('1. Explore the central node-link evidence graph powered by React Flow.\n')
    p.add_run('2. Click on target account nodes (e.g. ACC-90812) or transaction edges to open the Node Metadata Drawer.\n')
    p.add_run('3. Review calculated PageRank metrics, degree centrality scores, and structural anomaly indicators.')
    add_screenshot_box(4, 'Interactive Evidence Graph & Metadata Drawer', 'React Flow Evidence Graph canvas with node selection drawer showing PageRank and centrality metrics.')

    # --- Step 5 ---
    add_custom_heading('Step 5: Audit Tribunal Consensus & Final Verdict', level=1)
    p = doc.add_paragraph()
    p.add_run('1. Review the top Tribunal Verdict Banner displaying overall case recommendation.\n')
    p.add_run('2. Categories: GUILTY / HIGH RISK, SUSPICIOUS / REVIEW, or INNOCENT / CLEARED BY DEFENSE.\n')
    p.add_run('3. Verification Point: Inspect transparent calibrated confidence score (e.g. 87.5% Confidence) synthesized from mathematical evidence weighing.')
    add_screenshot_box(5, 'Tribunal Consensus Verdict Banner', 'Verdict Header rendering calibrated confidence percentage, recommendation status, and synthesis summary.')

    # --- Step 6 ---
    add_custom_heading('Step 6: Download & Audit Multi-Format Reports', level=1)
    p = doc.add_paragraph()
    p.add_run('1. Scroll to the Export & Audit Section.\n')
    p.add_run('2. Test download buttons for HTML Report (interactive styled report), Markdown Summary (GFM formatted), and JSON Case File (complete provenance schema).')
    add_screenshot_box(6, 'Export & Audit Reports View', 'Report export action panel with buttons for downloading HTML, Markdown, and JSON case file formats.')

    # --- Verification Matrix ---
    add_custom_heading('Evaluation Verification Matrix', level=1)
    matrix_table = doc.add_table(rows=4, cols=5)
    matrix_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    headers = ['Scenario ID', 'Target Entity', 'Key Expert Trigger', 'Defense Outcome', 'Expected Final Verdict']
    row_hdr = matrix_table.rows[0]
    for idx, text in enumerate(headers):
        cell = row_hdr.cells[idx]
        set_cell_background(cell, '0F294A')
        set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.font.bold = True
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    data = [
        ['SCN-01', 'ACC-90812', '$9.5k x 3 within 24h', 'No payroll contract found', 'SUSPICIOUS (85%+)'],
        ['SCN-02', 'ACC-10492', '210-day dormancy reactivation', 'Frequency spike confirmed', 'HIGH RISK (90%+)'],
        ['SCN-03', 'ACC-77102', 'High monthly payout volume', 'Verified corporate payroll', 'CLEARED BY DEFENSE']
    ]

    for r_idx, row_data in enumerate(data):
        row = matrix_table.rows[r_idx + 1]
        bg_color = 'FFFFFF' if r_idx % 2 == 0 else 'F7FAFC'
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.size = Pt(9)
            if c_idx == 0:
                run.font.bold = True

    doc.save(output_path)
    print(f'Successfully created Word document: {output_path}')

if __name__ == '__main__':
    create_document(r'd:\TRIBUNAL\docs\End_to_End_Investigation_Walkthrough_Visual_Guide.docx')
    create_document(r'D:\TRIBUNAL_Submission\docs\End_to_End_Investigation_Walkthrough_Visual_Guide.docx')
