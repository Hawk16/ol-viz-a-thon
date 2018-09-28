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

# ------------------------------------------------------------- #
#                        Load Input data                        #
# ------------------------------------------------------------- #

# Generate CSV input files from Viz-a-Thon CSV files
InputData().generate_data()
print('Input data generated.')

# All States (Overview)
display_cols = [
    'State', 'PopDensity', 'Rural', 
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
source2 = ColumnDataSource(df2)

# Names of Courts by State
df3 = pd.read_csv('viz_a_thon_data_sources/names_of_courts_by_state.csv')
source3 = ColumnDataSource(df3)

# Court Case Types
df4 = pd.read_csv('viz_a_thon_data_sources/all_court_case_types.csv')
source4 = ColumnDataSource(df4)

# Court Hieararchy
df5 = pd.read_csv('viz_a_thon_data_sources/court_hierarchy.csv')
source5 = ColumnDataSource(df5)

# ------------------------------------------ #
#              Update function               #
# ------------------------------------------ #

def update():
    
    current = df[
        (df['CaseloadLow'] >= caseload_size.value[0]) 
        & (df['CaseloadHigh'] <= caseload_size.value[1])
        & (df['RuralLow'] >= rural_prct.value)
        & (df['PopulationLow'] >= population_density.value)
        ]
    if death_penalty_select.value != 'N/A':
        current = current[current['DeathPen'] == death_penalty_select.value]
    if trial_struct.value != 'N/A':
        current = current[current['TrialStructure'] == trial_struct.value]
    if crim_trial_proc.value != 'N/A':
        current = current[current['CrimProc'] == crim_trial_proc.value]
    source.data = {
        'State': current.State,
        'PopDensity': current.PopDensity,
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
        if funding_select.value != 'N/A':
            current2 = current2[current2['FundingDescription'] == funding_select.value]
        if admin_appeal_select.value != 'N/A':
            current2 = current2[current2['AppealFromAdminAgency'] == admin_appeal_select.value]
        if court_desc_select.value != 'N/A':
            current2 = current2[current2['CourtLevelDescription'] == court_desc_select.value]
        if notes_contain.value != '':
            current2 = current2[current2['Notes'].str.contains(notes_contain.value.strip().lower())]
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
        current3 = df3[
            (df3['NumberDivisions'] >= num_divisions.value)
            & (df3['NumberJudges'] >= num_judges.value)
            & (df3['NumberPanels'] >= num_panels.value)
        ]
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
data_table1_header = Div(text='''<h2 align='left'>Overview</h2>''')
data_table2_header = Div(text='''<h2 align='left'>Courts, Jurisdiction, Funding, Admin Appeals</h2>''')
data_table3_header = Div(text='''<h2 align='left'>State Court Details</h2>''')
data_table4_header = Div(text='''<h2 align='left'>State Court Cases</h2>''')
data_table5_header = Div(text='''<h2 align='left'>State Court Hierarchy</h2>''')
flowcharts_header = Div(text='''<h2 align='left'>State Court FlowCharts</h2>''')
charts_header = Div(text='''<h2 align='left'>Overview Charts</h2>''')

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
dp.append('N/A')
death_penalty_select = Select(
    title='Death Penalty', 
    options=dp, 
    value='N/A')
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
trial_struct.append('N/A')
trial_struct = Select(
    title='Trial Structure', 
    options=trial_struct, 
    value='N/A')
trial_struct.on_change('value', lambda attr, old, new: update())

# Criminal Trial Procedure Select
crim_trial_proc = df['CrimProc'].unique().tolist()
crim_trial_proc.append('N/A')
crim_trial_proc = Select(
    title='Criminal Trial Structure', 
    options=crim_trial_proc, 
    value='N/A')
crim_trial_proc.on_change('value', lambda attr, old, new: update())

# Download button
download_button_table1 = Button(label="Download", button_type="success")
download_button_table1.callback = CustomJS(
    args=dict(source=source), 
    code=open('custom_js/download_states_overview.js').read())

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
funding_select = Select(
    title='Funding', 
    options=funding_select, 
    value='N/A')
funding_select.on_change('value', lambda attr, old, new: update())

# Appeal from Admin Agency Select
admin_appeal_select = df2['AppealFromAdminAgency'].unique().tolist()
admin_appeal_select.append('N/A')
admin_appeal_select = Select(
    title='Appeals from Administrative Agency', 
    options=admin_appeal_select, 
    value='N/A')
admin_appeal_select.on_change('value', lambda attr, old, new: update())

# Court Description Select
court_desc_select = df2['CourtLevelDescription'].unique().tolist()
court_desc_select.append('N/A')
court_desc_select = Select(
    title='Court Description', 
    options=court_desc_select, 
    value='N/A')
court_desc_select.on_change('value', lambda attr, old, new: update())

# Notes contain TextInput
notes_contain = df2['Notes'].unique().tolist()
notes_contain = TextInput(title='Notes contain')
notes_contain.on_change('value', lambda attr, old, new: update())

# Download button
download_button_table2 = Button(label="Download", button_type="success")
download_button_table2.callback = CustomJS(
    args=dict(source=source2), 
    code=open('custom_js/download_state_courts_jurisdiction_funding.js').read())

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

# Download button
download_button_table3 = Button(label="Download", button_type="success")
download_button_table3.callback = CustomJS(
    args=dict(source=source3), 
    code=open('custom_js/download_state_court_details.js').read())

# DataTable 4 ============ #

# State Select
state_select4 = df3['State'].unique().tolist()
state_select4.append('All')
state_select4 = Select(
    title='State', 
    options=state_select4, 
    value='All')
state_select4.on_change('value', lambda attr, old, new: update())

# Download button
download_button_table4 = Button(label="Download", button_type="success")
download_button_table4.callback = CustomJS(
    args=dict(source=source4), 
    code=open('custom_js/download_state_case_types.js').read())

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
download_button_table5 = Button(label="Download", button_type="success")
download_button_table5.callback = CustomJS(
    args=dict(source=source5), 
    code=open('custom_js/download_state_court_hiearchy.js').read())

# ---------------------------------------------------- #
#                       DataTables                     #
# ---------------------------------------------------- #

# DataTable # 1
columns = [
        TableColumn(field='State', title='State'),
        TableColumn(field='PopDensity', title='PopDensity'),
        TableColumn(field='Rural', title='Rural'),
        TableColumn(field='CaseloadSize', title='CaseloadSize'),
        TableColumn(field='TrialStructure', title='TrialStructure'),
        TableColumn(field='CrimProc', title='CrimProc'),
        TableColumn(field='DeathPen', title='DeathPen'),
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
    TableColumn(field='CourtName', title='CourtName'),
    TableColumn(field='CourtLevelDescription', title='CourtDescription'),
    TableColumn(field='FundingDescription', title='Funding'),
    TableColumn(field='AppealFromAdminAgency', title='AppealFromAdminAgency'),
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
    TableColumn(field='CourtNameName', title='CourtName'),
    TableColumn(field='NumberDivisions', title='NumberDivisions'),
    TableColumn(field='NumberJudges', title='NumberJudges'),
    TableColumn(field='NumberPanels', title='NumberPanels'),
    TableColumn(field='NumberOfIndividualCourts', title='NumberCourts'),
    TableColumn(field='PanelDecisionDescription', title='PanelDecision'),
    TableColumn(field='CaseManagementDescription', title='CaseManagement'),
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
    TableColumn(field='CourtName', title='CourtName'),
    TableColumn(field='CaseTypeDescription', title='CaseTypeDescription'),
    TableColumn(field='AppealByRight', title='AppealByRight'),
    TableColumn(field='AppealByPermission', title='AppealByPermission'),
    TableColumn(field='OriginalProceeding', title='OriginalProceeding'),
    TableColumn(field='InterlocutoryAppeal', title='InterlocutoryAppeal'),
    TableColumn(field='Exclusive', title='Exclusive'),
    TableColumn(field='Limited', title='Limited'),
    TableColumn(field='MinValue', title='MinValue'),
    TableColumn(field='MaxValue', title='MaxValue'),
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
    TableColumn(field='ChildCourtName', title='ChildCourt'),
    TableColumn(field='ParentCourtName', title='ParentCourt'),
]
data_table5 = DataTable(
    source=source5, 
    columns=columns5, 
    width=600, 
    height=300, 
    fit_columns=True,
    editable=True, 
    selectable=True)

# ------------------------------------------------ #
#                Flowchart Menu                    #
# ------------------------------------------------ #

# First State
flowcharts_div1 = Div(text="<img height=300 width=900 src='https://s3-us-west-1.amazonaws.com/viz-a-thon-images/NYFlowChart.png'></img>")

menu1 = [('Georgia', "<img height=300 width=900 src='https://s3-us-west-1.amazonaws.com/viz-a-thon-images/GeorgiaFlowChart.png'></img>"), 
        ('New York', "<img height=300 width=900 src='https://s3-us-west-1.amazonaws.com/viz-a-thon-images/NYFlowChart.png'></img>")]

def handler(attr, old, new):
    flowcharts_div1.text = new

dropdown = Dropdown(label='State Court System', menu=menu1)
dropdown.on_change('value', handler)
flowcharts_dropdown = widgetbox(dropdown)


# Second State
flowcharts_div2 = Div(text="<img height=300 width=900 src='https://s3-us-west-1.amazonaws.com/viz-a-thon-images/NYFlowChart.png'></img>")

menu2 = [('Georgia', "<img height=300 width=900 src='https://s3-us-west-1.amazonaws.com/viz-a-thon-images/GeorgiaFlowChart.png'></img>"), 
        ('New York', "<img height=300 width=900 src='https://s3-us-west-1.amazonaws.com/viz-a-thon-images/NYFlowChart.png'></img>")]

def handler2(attr, old, new):
    flowcharts_div2.text = new

dropdown2 = Dropdown(label='State Court System', menu=menu2)
dropdown2.on_change('value', handler2)
flowcharts_dropdown2 = widgetbox(dropdown2)

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
    death_penalty_select,
    download_button_table1)

controls2 = widgetbox(
    state_select, 
    court_desc_select,
    funding_select, 
    admin_appeal_select, 
    notes_contain, 
    download_button_table2) 

controls3 = widgetbox(
    state_select3,
    num_divisions,
    num_judges,
    num_panels,
    download_button_table3)

controls4 = widgetbox(
    state_select4,
    download_button_table4)

controls5 = widgetbox(
    state_select5,
    download_button_table5)
    
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
#
popdensity = all_states_display['PopulationDensity'].value_counts()
pop_densities = popdensity.index.values
p1 = figure(
    x_range=pop_densities,
    plot_height=250, 
    plot_width=350, 
    title='Population Density', 
    tools=tools, 
    toolbar_location='above')
p1.vbar(
    x=pop_densities,
    top=popdensity.values, 
    width=0.8,
    color='firebrick', 
    alpha=0.5)
p1.xaxis.axis_label = 'Population Density'
p1.yaxis.axis_label = 'Number of States'
p1.xgrid.grid_line_color = 'white'
p1.xaxis.major_label_orientation = math.pi/6

# % Rural of Population
#
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
rural_categories = rural.index.values
p3 = figure(
    x_range=rural_categories,
    plot_height=250, 
    plot_width=350,
    title='Rural %', 
    tools=tools,
    toolbar_location='above')
p3.vbar(
    x=rural_categories,
    top=rural.values, 
    width=0.8,
    color='firebrick', 
    alpha=0.5)
p3.xaxis.axis_label = '% of State Population that is Rural'
p3.xgrid.grid_line_color = 'white'
p3.xaxis.major_label_orientation = math.pi/6

# Caseload Size
#
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
caseloadsize_categories = caseloadsize.index.values
p4 = figure(
    x_range=caseloadsize_categories,
    plot_height=250, 
    plot_width=350, 
    title='Caseload Size', 
    tools=tools, 
    toolbar_location='above')
p4.vbar(
    x=caseloadsize_categories,
    top=caseloadsize.values, 
    width=0.8,
    color='firebrick', 
    alpha=0.5)
p4.xaxis.axis_label = 'Caseload Size'
p4.xgrid.grid_line_color = 'white'
p4.xaxis.major_label_orientation = math.pi/6

# Death Penalty
#
all_states_display['DeathPenalty'] = all_states_display['DeathPenalty'].str.replace('Missing information', 'N/A')
death_penalty = all_states_display['DeathPenalty'].value_counts()
death_penalty_categories = death_penalty.index.values
p5 = figure(
    x_range=death_penalty_categories,
    plot_height=250, 
    plot_width=350,
    title='Death Penalty', 
    tools=tools, 
    toolbar_location='above')
p5.vbar(
    x=death_penalty_categories,
    top=death_penalty.values, 
    width=0.8, 
    color='firebrick', 
    alpha=0.5)
p5.xaxis.axis_label = 'Death Penalty'
p5.xgrid.grid_line_color = 'white'

# ------------------------------------------- #
#                    Layout                   #
# ------------------------------------------- #

l = layout([
    [data_table1_header],
    [controls, table],
    [charts_header],
    [row([p1, p3, p4, p5])],
    [data_table2_header],
    [controls2, table2],
    [data_table3_header],
    [controls3, table3],
    [data_table4_header],
    [controls4, table4],
    [data_table5_header],
    [controls5, table5],
    [flowcharts_header],
    [flowcharts_div1], 
    [flowcharts_dropdown],
    [flowcharts_div2],
    [flowcharts_dropdown2],
], sizing_mode='fixed')

curdoc().add_root(l)
curdoc().title = 'StateCourtExplorer'

update()
