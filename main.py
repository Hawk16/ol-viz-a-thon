import math
import pandas as pd
from datetime import date

from bokeh.io import curdoc
from bokeh.models import Div
from bokeh.models import CustomJS
from bokeh.layouts import row
from bokeh.layouts import column
from bokeh.layouts import layout
from bokeh.plotting import figure
from bokeh.layouts import widgetbox
from bokeh.events import ButtonClick
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Button
from bokeh.models.widgets import Slider
from bokeh.models.widgets import Select
from bokeh.models.widgets import Dropdown
from bokeh.models.widgets import TextInput
from bokeh.models.widgets import DataTable
from bokeh.models.widgets import TableColumn
from bokeh.models.widgets import RangeSlider
from bokeh.models.widgets import NumberFormatter

from lib.input_data import InputData
from collections import OrderedDict
# ------------------------------------------------------------- #
#                        Load Input data                        #
# ------------------------------------------------------------- #

# Generate CSV input files from Viz-a-Thon CSV files
InputData().generate_data()
print('Input data generated.')

# All States (Overview)
display_cols = [
    'State', 'PopDensity', 'PopulationCategory', 'Rural', 
    'TrialStructure', 'CrimProc', 
    'DeathPen', 'CaseloadSize', 
    'CaseloadLow', 'CaseloadHigh',
    'RuralLow', 'RuralHigh',
    'PopulationLow', 'PopulationHigh', 
    'NeighboringStates']
df = pd.read_csv('viz_a_thon_data_sources/all_states_display.csv')
all_states_display = df.copy()
df.rename(columns={
    'USStateName': 'State', 
    'PopulationDensity': 'PopDensity', 
    'TrialCriminalProc': 'CrimProc',
    'DeathPenalty': 'DeathPen'}, inplace=True)
df = df[display_cols]
source = ColumnDataSource(df)

# US States and Courts
df2 = pd.read_csv('viz_a_thon_data_sources/us_states_and_courts.csv')
df2['Link'] = df2['Link'].str.replace('-99', '')
df2['Notes'] = df2['Notes'].fillna('')
source2 = ColumnDataSource(df2)

# Names of Courts by State
df3 = pd.read_csv('viz_a_thon_data_sources/names_of_courts_by_state.csv')
df3['CaseManagementDescription'] = df3['CaseManagementDescription'].str.replace('-99', '')
df3['CaseManagementDescription'] = df3['CaseManagementDescription'].str.replace('-98', '')
df3['PanelDecisionDescription'] = df3['PanelDecisionDescription'].fillna('')
df3['PanelDecisionDescription'] = df3['PanelDecisionDescription'].str.replace('Missing information', '')
df3['CaseManagementDescription'] = df3['CaseManagementDescription'].fillna('')
source3 = ColumnDataSource(df3)

# Court Case Types
df4 = pd.read_csv('viz_a_thon_data_sources/all_court_case_types.csv')
df4['AppealByRight'] = df4['AppealByRight'].replace(True, 'Yes')
df4['AppealByRight'] = df4['AppealByRight'].replace(False, 'No')
df4['AppealByPermission'] = df4['AppealByPermission'].replace(True, 'Yes')
df4['AppealByPermission'] = df4['AppealByPermission'].replace(False, 'No')
df4['OriginalProceeding'] = df4['OriginalProceeding'].replace(True, 'Yes')
df4['OriginalProceeding'] = df4['OriginalProceeding'].replace(False, 'No')
df4['InterlocutoryAppeal'] = df4['InterlocutoryAppeal'].replace(True, 'Yes')
df4['InterlocutoryAppeal'] = df4['InterlocutoryAppeal'].replace(False, 'No')
df4['Exclusive'] = df4['Exclusive'].replace(True, 'Yes')
df4['Exclusive'] = df4['Exclusive'].replace(False, 'No')
df4['Limited'] = df4['Limited'].replace(True, 'Yes')
df4['Limited'] = df4['Limited'].replace(False, 'No')
df4['MinValue'] = df4['MinValue'].replace(-98, 0)
df4['MaxValue'] = df4['MinValue'].replace(-98, 0)
df4['Notes'] = df4['Notes'].fillna('')
df4['Notes'] = df4['Notes'].fillna('')
source4 = ColumnDataSource(df4)

# Court Hieararchy
df5 = pd.read_csv('viz_a_thon_data_sources/court_hierarchy.csv')
source5 = ColumnDataSource(df5)

# ------------------------------------------ #
#              Update function               #
# ------------------------------------------ #

def reset_overview_table(event):
    current = df
    source.data = {
        'State': current.State,
        'PopDensity': current.PopDensity,
        'PopulationCategory': current.PopulationCategory,
        'Rural': current.Rural,
        'TrialStructure': current.TrialStructure,
        'CrimProc': current.CrimProc,
        'DeathPen': current.DeathPen,
        'CaseloadSize': current.CaseloadSize,
        'CaseloadLow': current.CaseloadLow,
        'NeighboringStates': current.NeighboringStates,
        'CaseloadHigh': current.CaseloadHigh}

def reset_court_jurisdiction_funding_table(event):
    current2 = df2
    source2.data = {
        'State': current2.State,
        'CourtName': current2.CourtName,
        'CourtLevelDescription': current2.CourtLevelDescription,
        'FundingDescription': current2.FundingDescription,
        'AppealFromAdminAgency': current2.AppealFromAdminAgency,
        'CSPAggID': current2.CSPAggID,
        'Notes': current2.Notes,
        'Link': current2.Link}

def reset_state_court_details_table(event):
    current3 = df3
    source3.data = {
        'State': current3.State,
        'CourtNameName': current3.CourtNameName,
        'NumberDivisions': current3.NumberDivisions,
        'NumberJudges': current3.NumberJudges,
        'NumberPanels': current3.NumberPanels,
        'PanelDecisionDescription': current3.PanelDecisionDescription,
        'NumberOfIndividualCourts': current3.NumberOfIndividualCourts,
        'CaseManagementDescription': current3.CaseManagementDescription}

def reset_state_court_cases_table(event):
    current4 = df4
    source4.data = {
        'State': current4.State,
        'CourtName': current4.CourtName,
        'CaseTypeDescription': current4.CaseTypeDescription,
        'AppealByRight': current4.AppealByRight,
        'AppealByPermission': current4.AppealByPermission,
        'OriginalProceeding': current4.OriginalProceeding,
        'InterlocutoryAppeal': current4.InterlocutoryAppeal,
        'Exclusive': current4.Exclusive,
        'Limited': current4.Limited,
        'MinValue': current4.MinValue,
        'MaxValue': current4.MaxValue,
        'Notes': current4.Notes}

def reset_state_court_hierarchy_table(event):
    current5 = df5
    source5.data = {
        'State': current5.State,
        'ChildCourtName': current5.ChildCourtName,
        'ParentCourtName': current5.ParentCourtName}

def update():
    
    current = df[
        (df['CaseloadLow'] >= caseload_size.value[0]) 
        & (df['CaseloadHigh'] <= caseload_size.value[1])
        & (df['RuralLow'] >= rural_prct.value)
        & (df['PopulationLow'] >= population_density.value)
        ]
    if death_penalty_select.value != 'Select value ...':
        current = current[current['DeathPen'] == death_penalty_select.value]
    if trial_struct.value != 'Select value ...':
        current = current[current['TrialStructure'] == trial_struct.value]
    if crim_trial_proc.value != 'Select value ...':
        current = current[current['CrimProc'] == crim_trial_proc.value]
    source.data = {
        'State': current.State,
        'PopDensity': current.PopDensity,
        'PopulationCategory': current.PopulationCategory,
        'Rural': current.Rural,
        'TrialStructure': current.TrialStructure,
        'CrimProc': current.CrimProc,
        'DeathPen': current.DeathPen,
        'CaseloadSize': current.CaseloadSize,
        'CaseloadLow': current.CaseloadLow,
        'NeighboringStates': current.NeighboringStates,
        'CaseloadHigh': current.CaseloadHigh}
    
    if state_select.value != 'All':
        current2 = df2[df2['State'] == state_select.value]
    else:
        current2 = df2
        if funding_select.value != 'Select value ...':
            current2 = current2[current2['FundingDescription'] == funding_select.value]
        if admin_appeal_select.value != 'Select value ...':
            current2 = current2[current2['AppealFromAdminAgency'] == admin_appeal_select.value]
        if court_desc_select.value != 'Select value ...':
            current2 = current2[current2['CourtLevelDescription'] == court_desc_select.value]
        if notes_contain.value != '':
            current2 = current2[current2['Notes'].str.contains(notes_contain.value.strip().lower())]
        if cspaggid_select.value != 'Select value ...':
            current2 = current2[current2['CSPAggID'] == cspaggid_select.value]
    source2.data = {
        'State': current2.State,
        'CourtName': current2.CourtName,
        'CourtLevelDescription': current2.CourtLevelDescription,
        'FundingDescription': current2.FundingDescription,
        'AppealFromAdminAgency': current2.AppealFromAdminAgency,
        'CSPAggID': current2.CSPAggID,
        'Notes': current2.Notes,
        'Link': current2.Link}
    
    if state_select3.value != 'All':
        current3 = df3[df3['State'] == state_select3.value]
    else:
        current3 = df3
    if num_divisions.value != 0:
        current3 = current3[current3['NumberDivisions'] >= num_divisions.value]
    if num_judges.value != 0:
        current3 = current3[current3['NumberJudges'] >= num_judges.value]
    if num_panels.value != 0:
        current3 = current3[current3['NumberPanels'] >= num_panels.value]
    if panel_decision_select.value != 'Select value ...':
        current3 = current3[current3['PanelDecisionDescription'] == panel_decision_select.value]
    source3.data = {
        'State': current3.State,
        'CourtNameName': current3.CourtNameName,
        'NumberDivisions': current3.NumberDivisions,
        'NumberJudges': current3.NumberJudges,
        'NumberPanels': current3.NumberPanels,
        'PanelDecisionDescription': current3.PanelDecisionDescription,
        'NumberOfIndividualCourts': current3.NumberOfIndividualCourts,
        'CaseManagementDescription': current3.CaseManagementDescription}

    if state_select4.value != 'All':
        current4 = df4[df4['State'] == state_select4.value]
    else:
        current4 = df4 
    if case_type_select.value != 'Select value ...':
        current4 = current4[current4['CaseTypeDescription'] == case_type_select.value]
    source4.data = {
        'State': current4.State,
        'CourtName': current4.CourtName,
        'CaseTypeDescription': current4.CaseTypeDescription,
        'AppealByRight': current4.AppealByRight,
        'AppealByPermission': current4.AppealByPermission,
        'OriginalProceeding': current4.OriginalProceeding,
        'InterlocutoryAppeal': current4.InterlocutoryAppeal,
        'Exclusive': current4.Exclusive,
        'Limited': current4.Limited,
        'MinValue': current4.MinValue,
        'MaxValue': current4.MaxValue,
        'Notes': current4.Notes}
    
    if state_select5.value != 'All':
        current5 = df5[df5['State'] == state_select5.value]
    else:
        current5 = df5 
    source5.data = {
        'State': current5.State,
        'ChildCourtName': current5.ChildCourtName,
        'ParentCourtName': current5.ParentCourtName}
    
# -------------------------------------------------------------- #
#                        HTML Headers                            #
# -------------------------------------------------------------- #

# HTML Headers for DataTables
table_of_contents = Div(text="""
<div>
<p><a id=page_top></a></p>
<p>
  <!--h2 style="padding-left: 12px; padding-right: 12px;">Contents</h2></p-->
  <ul>
    <li><a href='#States Overview'>States Overview Table</a></li>
    <li><a href='#Courts Overview'>Courts Overview Table</a></li>
    <li><a href='#Court Details'>Court Details Table</a></li>
    <li><a href='#Court Cases'>Court Cases Table</a></li>
    <li><a href='#Court Hierarchies'>Court Hierarchies Table</a></li>
    <li><a href='#Case Flowcharts'>Case Flowcharts</a></li>
  </ul>
</div>
<br>
""")
top_of_page_link = Div(text="""<a href='#page_top' align='left'>Top of Page</a>""")
top_of_page_link2 = Div(text="""<a href='#page_top' align='left'>Top of Page</a>""")
top_of_page_link3 = Div(text="""<a href='#page_top' align='left'>Top of Page</a>""")
top_of_page_link4 = Div(text="""<a href='#page_top' align='left'>Top of Page</a>""")
top_of_page_link5 = Div(text="""<a href='#page_top' align='left'>Top of Page</a>""")
top_of_page_link6 = Div(text="""<a href='#page_top' align='left'>Top of Page</a>""")

data_table1_header1 = Div(text="""<h1 id='States Overview' align='left'>States Overview</h1>""")
data_table1_header2 = Div(text="""<h1 align='left'><font color='white'>States Overview</font></h1>""")
data_table2_header = Div(text="""<h1 id='Courts Overview' align='left'>Courts Overview</h1>""")
data_table3_header = Div(text="""<h1 id='Court Details' align='left'>Court Details</h1>""")
data_table4_header = Div(text="""<h1 id='Court Cases' align='left'>Court Cases</h1>""")
data_table5_header = Div(text="""<h1 id='Court Hierarchies' align='left'>Court Hierarchies</h1>""")
flowcharts_header = Div(text="""
<h1 id='Case Flowcharts' align='left'>Case Flowcharts</h1>
<p><b>Select a state then click on a particular court to highlight the appeals process.<b></p>
""")
charts_header = Div(text='''<h2 align='left'>Overview Charts</h1>''')
line_breaks = Div(text="""<h1><font color='white'></font></h1>""")

flowcharts_iframe = Div(text="""
<iframe height='750' width='1200' scrolling='no' src='http://vizathon.onelegal.com:3000/' 
    style="border-radius: 25px;
    -moz-transform: scale(0.55, 0.55); 
    -webkit-transform: scale(0.55, 0.55); 
    -o-transform: scale(0.55, 0.55);
    -ms-transform: scale(0.55, 0.55);
    transform: scale(0.55, 0.55); 
    -moz-transform-origin: top left;
    -webkit-transform-origin: top left;
    -o-transform-origin: top left;
    -ms-transform-origin: top left;
    transform-origin: top left;"></iframe>
""")
flowcharts_iframe2 = Div(text="""
<iframe height='750' width='1200' scrolling='no' src='http://vizathon.onelegal.com:3000/' 
    style="border-radius: 25px;
    -moz-transform: scale(0.55, 0.55); 
    -webkit-transform: scale(0.55, 0.55); 
    -o-transform: scale(0.55, 0.55);
    -ms-transform: scale(0.55, 0.55);
    transform: scale(0.55, 0.55); 
    -moz-transform-origin: top right;
    -webkit-transform-origin: top right;
    -o-transform-origin: top right;
    -ms-transform-origin: top right;
    transform-origin: top right;"></iframe>
""")

# --------------------------------------------------------- #
#                        Widgets                            #
# --------------------------------------------------------- #

# DataTable1 ============== #

# Caseload Size RangeSlider
caseload_size = RangeSlider(
    title='CaseloadSize', 
    start=0, 
    end=df['CaseloadHigh'].max(),
    value=(0, df['CaseloadHigh'].max()),
    step=1000, 
    format='0,0')
caseload_size.on_change('value', lambda attr, old, new: update())

# % Rural
rural_prct = Slider(
    title='% Rural', 
    start=0, 
    end=df['RuralHigh'].max(), 
    value=0, 
    step=1)
rural_prct.on_change('value', lambda attr, old, new: update())

# Death Penalty Select
dp = df['DeathPen'].unique().tolist()
dp.remove('Missing information')
dp.append('Select value ...')
death_penalty_select = Select(
    title='Death Penalty', 
    options=dp, 
    value='Select value ...')
death_penalty_select.on_change('value', lambda attr, old, new: update())

# Population Density
population_density = Slider(
    title='Population Density', 
    start=0, 
    end=df['PopulationHigh'].max(), 
    value=0, 
    step=100)
population_density.on_change('value', lambda attr, old, new: update())

# Trial Structure Select
trial_struct = df['TrialStructure'].unique().tolist()
trial_struct.append('Select value ...')
trial_struct = Select(
    title='Trial Structure', 
    options=trial_struct, 
    value='Select value ...')
trial_struct.on_change('value', lambda attr, old, new: update())

# Criminal Trial Procedure Select
crim_trial_proc = df['CrimProc'].unique().tolist()
crim_trial_proc.append('Select value ...')
crim_trial_proc = Select(
    title='Criminal Trial Structure', 
    options=crim_trial_proc, 
    value='Select value ...')
crim_trial_proc.on_change('value', lambda attr, old, new: update())

# Download button
download_button_table1 = Button(label="Export as CSV", button_type="success")
download_button_table1.callback = CustomJS(
    args=dict(source=source), 
    code=open('custom_js/download_states_overview.js').read())

reset_button_table1 = Button(label='Reset Table', button_type='primary')
reset_button_table1.on_event(ButtonClick, reset_overview_table) 

# DataTable2 ================ #

# State Select
state_select = df2['State'].unique().tolist()
state_select.append('All')
state_select = Select(
    title='State', 
    options=state_select, 
    value='All')
state_select.on_change('value', lambda attr, old, new: update())

# Funding Select 
funding_select = df2['FundingDescription'].unique().tolist() 
funding_select.append('N/A') 
funding_select.append('Select value ...') 
funding_select = Select(
    title='Funding', 
    options=funding_select, 
    value='Select value ...')
funding_select.on_change('value', lambda attr, old, new: update())

# CSPAggID Select 
cspaggid_select = df2['CSPAggID'].unique().tolist() 
cspaggid_select.append('N/A') 
cspaggid_select.append('Select value ...') 
cspaggid_select = Select(
    title='CSPAggID', 
    options=cspaggid_select, 
    value='Select value ...')
cspaggid_select.on_change('value', lambda attr, old, new: update())

# Appeal from Admin Agency Select
admin_appeal_select = df2['AppealFromAdminAgency'].unique().tolist()
admin_appeal_select.append('Select value ...')
admin_appeal_select = Select(
    title='Appeals from Administrative Agency', 
    options=admin_appeal_select, 
    value='Select value ...')
admin_appeal_select.on_change('value', lambda attr, old, new: update())

# Court Description Select
court_desc_select = df2['CourtLevelDescription'].unique().tolist()
court_desc_select.append('Select value ...')
court_desc_select = Select(
    title='Jurisdiction', 
    options=court_desc_select, 
    value='Select value ...')
court_desc_select.on_change('value', lambda attr, old, new: update())

# Notes contain TextInput
notes_contain = df2['Notes'].unique().tolist()
notes_contain = TextInput(title='Search Notes')
notes_contain.on_change('value', lambda attr, old, new: update())

# Download button
download_button_table2 = Button(label="Export as CSV", button_type="success")
download_button_table2.callback = CustomJS(
    args=dict(source=source2), 
    code=open('custom_js/download_state_courts_jurisdiction_funding.js').read())

reset_button_table2 = Button(label='Reset Table', button_type='primary')
reset_button_table2.on_event(ButtonClick, reset_court_jurisdiction_funding_table)

# DataTable3 ================= #

# State Select
state_select3 = df3['State'].unique().tolist()
state_select3.append('All')
state_select3 = Select(
    title='State', 
    options=state_select3, 
    value='All')
state_select3.on_change('value', lambda attr, old, new: update())

# Number of Divisions
num_divisions = Slider(
    title='# Divisions', 
    start=0, 
    end=df3['NumberDivisions'].max(), 
    value=0, 
    step=1)
num_divisions.on_change('value', lambda attr, old, new: update())

# Number of Judges
num_judges = Slider(
    title='# Judges', 
    start=0, 
    end=36, 
    value=0, 
    step=1)
num_judges.on_change('value', lambda attr, old, new: update())

# Number of Panels
num_panels = Slider(
    title='# Panels', 
    start=0, 
    end=df3['NumberPanels'].max(), 
    value=0, 
    step=1)
num_panels.on_change('value', lambda attr, old, new: update())

# Panel Decision Select 
panel_decision_select = df3['PanelDecisionDescription'].unique().tolist() 
panel_decision_select.append('Select value ...') 
panel_decision_select = Select(
    title='Panel Decision', 
    options=panel_decision_select, 
    value='Select value ...')
panel_decision_select.on_change('value', lambda attr, old, new: update())

# Download button
download_button_table3 = Button(label="Export as CSV", button_type="success")
download_button_table3.callback = CustomJS(
    args=dict(source=source3), 
    code=open('custom_js/download_state_court_details.js').read())

reset_button_table3 = Button(label='Reset Table', button_type='primary')
reset_button_table3.on_event(ButtonClick, reset_state_court_details_table)

# DataTable 4 ============ #

# State Select
state_select4 = df3['State'].unique().tolist()
state_select4.append('All')
state_select4 = Select(
    title='State', 
    options=state_select4, 
    value='All')
state_select4.on_change('value', lambda attr, old, new: update())

# Case type select
case_types = df4['CaseTypeDescription'].unique().tolist()
case_types.append('Select value ...')
case_type_select = Select(
    title='Case Type', 
    options=case_types, 
    value='Select value ...')
case_type_select.on_change('value', lambda attr, old, new: update())

# Download button
download_button_table4 = Button(label="Export as CSV", button_type="success")
download_button_table4.callback = CustomJS(
    args=dict(source=source4), 
    code=open('custom_js/download_state_case_types.js').read())

reset_button_table4 = Button(label='Reset Table', button_type='primary')
reset_button_table4.on_event(ButtonClick, reset_state_court_cases_table)

# DataTable 5 ============ # 

# State Select
state_select5 = df3['State'].unique().tolist()
state_select5.append('All')
state_select5 = Select(
    title='State', 
    options=state_select5, 
    value='All')
state_select5.on_change('value', lambda attr, old, new: update())

# Download button
download_button_table5 = Button(label="Export as CSV", button_type="success")
download_button_table5.callback = CustomJS(
    args=dict(source=source5), 
    code=open('custom_js/download_state_court_hiearchy.js').read())

reset_button_table5 = Button(label='Reset Table', button_type='primary')
reset_button_table5.on_event(ButtonClick, reset_state_court_hierarchy_table)

# ---------------------------------------------------- #
#                       DataTables                     #
# ---------------------------------------------------- #

# DataTable # 1
columns = [
        TableColumn(field='State', title='State'),
        TableColumn(field='PopDensity', title='Population Density'),
        TableColumn(field='PopulationCategory', title='Population'),
        TableColumn(field='Rural', title='Rural'),
        TableColumn(field='CaseloadSize', title='Caseload Size'),
        TableColumn(field='TrialStructure', title='Trial Structure'),
        TableColumn(field='CrimProc', title='Criminal Procedure'),
        TableColumn(field='DeathPen', title='Death Penalty'),
        TableColumn(field='NeighboringStates', title='Neighbors')]
data_table = DataTable(
    source=source, 
    columns=columns, 
    width=1100, 
    height=300,
    fit_columns=True,
    editable=True, selectable=True)

# DataTable #2
columns2 = [
    TableColumn(field='State', title='State'),
    TableColumn(field='CourtName', title='Court Name'),
    TableColumn(field='CourtLevelDescription', title='Jurisdiction'),
    TableColumn(field='FundingDescription', title='Funding'),
    TableColumn(field='AppealFromAdminAgency', title='Appeal from Admin. Agency'),
    TableColumn(field='Notes', title='Notes'),
    TableColumn(field='CSPAggID', title='CSPAggID'),
    TableColumn(field='Link', title='URL')]
data_table2 = DataTable(
    source=source2, 
    columns=columns2, 
    width=1100, 
    height=300, 
    fit_columns=True,
    editable=True, 
    selectable=True)

# DataTable #3
columns3 = [
    TableColumn(field='State', title='State'),
    TableColumn(field='CourtNameName', title='Court'),
    TableColumn(field='NumberDivisions', title='Number of Divisions'),
    TableColumn(field='NumberJudges', title='Number of Judges'),
    TableColumn(field='NumberPanels', title='Number of  Panels'),
    TableColumn(field='NumberOfIndividualCourts', title='Number of Courts'),
    TableColumn(field='PanelDecisionDescription', title='Panel Decision'),
    TableColumn(field='CaseManagementDescription', title='Case Management'),
]
data_table3 = DataTable(
    source=source3, 
    columns=columns3, 
    width=1100, 
    height=300, 
    fit_columns=True,
    editable=True, 
    selectable=True)

# DataTable 4
columns4 = [
    TableColumn(field='State', title='State'),
    TableColumn(field='CourtName', title='Court Name'),
    TableColumn(field='CaseTypeDescription', title='Case Type Description'),
    TableColumn(field='AppealByRight', title='Appeal by Right'),
    TableColumn(field='AppealByPermission', title='Appeal by Permission'),
    TableColumn(field='OriginalProceeding', title='Original Proceeding'),
    TableColumn(field='InterlocutoryAppeal', title='Interlocutory Appeal'),
    TableColumn(field='Exclusive', title='Exclusive'),
    TableColumn(field='Limited', title='Limited'),
    TableColumn(field='MinValue', title='Min. Value'),
    TableColumn(field='MaxValue', title='Max. Value'),
    TableColumn(field='Notes', title='Notes'),
]
data_table4 = DataTable(
    source=source4, 
    columns=columns4, 
    width=1100, 
    height=300, 
    fit_columns=True,
    editable=True, 
    selectable=True)

# DataTable 4
columns5 = [
    TableColumn(field='State', title='State'),
    TableColumn(field='ChildCourtName', title='Child Court'),
    TableColumn(field='ParentCourtName', title='Parent Court'),
]
data_table5 = DataTable(
    source=source5, 
    columns=columns5, 
    width=600, 
    height=300, 
    fit_columns=True,
    editable=True, 
    selectable=True)

# ----------------------------------------------- #
#                   Controls                      #
# ----------------------------------------------- #

# Controls
controls = widgetbox(
    population_density,
    rural_prct, 
    caseload_size,  
    trial_struct,
    crim_trial_proc,
    death_penalty_select)
export_button1 = widgetbox(download_button_table1)
reset_button1 = widgetbox(reset_button_table1)

controls2 = widgetbox(
    state_select, 
    court_desc_select,
    funding_select, 
    cspaggid_select,
    admin_appeal_select, 
    notes_contain) 
export_button2 = widgetbox(download_button_table2)
reset_button2 = widgetbox(reset_button_table2) 

controls3 = widgetbox(
    state_select3,
    num_divisions,
    num_judges,
    num_panels, 
    panel_decision_select)
reset_button3 = widgetbox(reset_button_table3)
export_button3 = widgetbox(download_button_table3)

controls4 = widgetbox(
    state_select4,
    case_type_select)
export_button4 = widgetbox(download_button_table4)
reset_button4 = widgetbox(reset_button_table4)

controls5 = widgetbox(
    state_select5)
export_button5 = widgetbox(download_button_table5)
reset_button5 = widgetbox(reset_button_table5)
    
table = widgetbox(data_table)
table2 = widgetbox(data_table2)
table3 = widgetbox(data_table3)
table4 = widgetbox(data_table4)
table5 = widgetbox(data_table5)

# ------------------------------------------- #
#                    Charts                   #
# ------------------------------------------- #

tools = 'pan,wheel_zoom,reset'

# Population Density
TOOLTIPS = '''<div style="max-width: 180px;">@desc</div>'''
popdensity = all_states_display['PopulationDensity'].value_counts()
popdensity = popdensity.reindex(['0-20', '21-50', '51-100', '101-200', '201-500', '501-1000', '1001-highest'])

states_to_display = OrderedDict()
for category in ['0-20', '21-50', '51-100', '101-200', '201-500', '501-1000', '1001-highest']:
    states_to_display[category] = list(all_states_display[all_states_display['PopulationDensity'] == category]['USStateName'].values)
states_to_display_as_str = [str(vals).strip('[]').replace("'", '\n') for vals in states_to_display.values()]
pop_densities = popdensity.index.values
src = ColumnDataSource(data=dict(x=pop_densities, y=popdensity.values, desc=states_to_display_as_str))

p1 = figure(
    x_range=pop_densities,
    plot_height=250, 
    plot_width=350, 
    title='Population Density', 
    tools=tools, 
    toolbar_location='above',
    tooltips=TOOLTIPS)
p1.vbar(
    x='x',
    top='y', 
    width=0.8,
    color='firebrick', 
    alpha=0.5,
    source=src)
p1.xaxis.axis_label = 'People Per Square Mile'
p1.yaxis.axis_label = 'States'
p1.xgrid.grid_line_color = 'white'
p1.xaxis.major_label_orientation = math.pi/6
p1.xaxis.axis_label_text_color = 'firebrick'
p1.xaxis.axis_label_text_font_style = 'bold'
p1.yaxis.axis_label_text_color = 'firebrick'
p1.yaxis.axis_label_text_font_style = 'bold'

# % Rural of Population
def transform_rural_column(row):
    if row['Rural'] == '26-49% of the population':
        return '26-49%'
    elif row['Rural'] == '16-25% of the population':
        return '16-25%'
    elif row['Rural'] == 'Less than or equal to 15% of the population':
        return '<= 15%'
    elif row['Rural'] == 'Greater than or equal to 50% of the population':
        return '>= 50%'
    elif row['Rural'] == 'Missing information':
        return 'N/A'
all_states_display['Rural'] = all_states_display.apply(transform_rural_column, axis=1)
rural = all_states_display['Rural'].value_counts()
rural = rural.reindex(['<= 15%', '16-25%', '26-49%', '>= 50%', 'N/A'])

states_to_display2 = OrderedDict()
for category in ['<= 15%', '16-25%', '26-49%', '>= 50%', 'N/A']:
    states_to_display2[category] = list(all_states_display[all_states_display['Rural'] == category]['USStateName'].values)
states_to_display_as_str2 = [str(vals).strip('[]').replace("'", '\n') for vals in states_to_display2.values()]
rural_categories = rural.index.values
src2 = ColumnDataSource(data=dict(x=rural_categories, y=rural.values, desc=states_to_display_as_str2))

p3 = figure(
    x_range=rural_categories,
    plot_height=250, 
    plot_width=350,
    title='Rural %', 
    tools=tools,
    toolbar_location='above',
    tooltips=TOOLTIPS)
p3.vbar(
    x='x',
    top='y', 
    width=0.8,
    color='firebrick', 
    alpha=0.5,
    source=src2)
p3.xaxis.axis_label = '% of State Population that is Rural'
p3.xgrid.grid_line_color = 'white'
p3.xaxis.major_label_orientation = math.pi/6
p3.xaxis.axis_label_text_color = 'firebrick'
p3.xaxis.axis_label_text_font_style = 'bold'
p3.xaxis.axis_label_standoff = 20

# Caseload Size
def transform_caseload_size_column(row):
    if row['CaseloadSize'] == '1.1 Million-3 Million':
        return '1.1M - 3M'
    elif row['CaseloadSize'] == '501 Thousand-1 Million':
        return '500k - 1M'
    elif row['CaseloadSize'] == 'Under 200 Thousand':
        return '< 200k'
    elif row['CaseloadSize'] == '201 Thousand-500 Thousand':
        return '201k - 500k'
    elif row['CaseloadSize'] == '3.1 Million-6 Million':
        return '3.1M - 6M'
    elif row['CaseloadSize'] == 'Over 6 Million':
        return '> 6M'
all_states_display['CaseloadSize'] = all_states_display.apply(transform_caseload_size_column, axis=1)
caseloadsize = all_states_display['CaseloadSize'].value_counts()

caseloadsize = caseloadsize.reindex(['< 200k', '201k - 500k', '500k - 1M', '1.1M - 3M', '3.1M - 6M', '> 6M'])
states_to_display3 = OrderedDict()
for category in ['< 200k', '201k - 500k', '500k - 1M', '1.1M - 3M', '3.1M - 6M', '> 6M']:
    states_to_display3[category] = list(all_states_display[all_states_display['CaseloadSize'] == category]['USStateName'].values)
states_to_display_as_str3 = [str(vals).strip('[]').replace("'", '\n') for vals in states_to_display3.values()]
caseloadsize_categories = caseloadsize.index.values
src3 = ColumnDataSource(data=dict(x=caseloadsize_categories, y=caseloadsize.values, desc=states_to_display_as_str3))

p4 = figure(
    x_range=caseloadsize_categories,
    plot_height=250, 
    plot_width=350, 
    title='Caseload Size', 
    tools=tools, 
    toolbar_location='above',
    tooltips=TOOLTIPS)
p4.vbar(
    x='x',
    top='y', 
    width=0.8,
    color='firebrick', 
    alpha=0.5,
    source=src3)
p4.xaxis.axis_label = 'Caseload Size'
p4.xgrid.grid_line_color = 'white'
p4.xaxis.major_label_orientation = math.pi/6
p4.xaxis.axis_label_text_color = 'firebrick'
p4.xaxis.axis_label_text_font_style = 'bold'
p4.xaxis.axis_label_standoff = 10

# Death Penalty
all_states_display['DeathPenalty'] = all_states_display['DeathPenalty'].str.replace('Missing information', 'N/A')
death_penalty = all_states_display['DeathPenalty'].value_counts()

states_to_display4 = OrderedDict()
for category in ['Yes', 'No', 'N/A']:
    states_to_display4[category] = list(all_states_display[all_states_display['DeathPenalty'] == category]['USStateName'].values)
states_to_display_as_str4 = [str(vals).strip('[]').replace("'", '\n') for vals in states_to_display4.values()]
death_penalty_categories = death_penalty.index.values
src4 = ColumnDataSource(data=dict(x=death_penalty_categories, y=death_penalty.values, desc=states_to_display_as_str4))

p5 = figure(
    x_range=death_penalty_categories,
    plot_height=250, 
    plot_width=350,
    title='Death Penalty', 
    tools=tools, 
    toolbar_location='above',
    tooltips=TOOLTIPS)
p5.vbar(
    x='x',
    top='y', 
    width=0.8, 
    color='firebrick', 
    alpha=0.5,
    source=src4)
p5.xaxis.axis_label = 'Death Penalty'
p5.xgrid.grid_line_color = 'white'
p5.xaxis.axis_label_text_color = 'firebrick'
p5.xaxis.axis_label_text_font_style = 'bold'
p5.xaxis.axis_label_standoff = 30

# ------------------------------------------- #
#                    Layout                   #
# ------------------------------------------- #

l = layout([
    [table_of_contents],
    [row([p1, p3, p4, p5])],
    [data_table1_header2],
    [data_table1_header1, reset_button1, export_button1],
    [controls, table],
    [top_of_page_link],
    [data_table2_header, reset_button2, export_button2],
    [controls2, table2],
    [top_of_page_link2],
    [data_table3_header, reset_button3, export_button3],
    [controls3, table3],
    [top_of_page_link3],
    [data_table4_header, reset_button4, export_button4],
    [controls4, table4],
    [top_of_page_link4],
    [data_table5_header, reset_button5, export_button5],
    [controls5, table5],
    [top_of_page_link5],
    [flowcharts_header],
    [flowcharts_iframe, flowcharts_iframe2],
], sizing_mode='fixed')

curdoc().add_root(l)
curdoc().title = 'StateCourtExplorer'

update()
