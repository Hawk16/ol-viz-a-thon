"""This file creates DataFrames to serve as input for Bokeh Dashboard."""

import re
import numpy as np
import pandas as pd

class InputData():
    
    def __init__(self):
        self.appeals = self.format_appeals_data()
        self.crim_appeals_struct = self.format_crim_appeals_data()
        self.case_mgmt = self.format_case_mgmt_data()
        self.case_type = self.format_case_type_data()
        self.caseload_size = self.format_caseload_size_data()
        self.child_court = self.format_child_court_data()
        self.courts = self.format_courts_data()
        self.court_case_type = self.format_court_case_types_data()
        self.court_court_names = self.format_court_court_names_data()
        self.court_level = self.format_court_level_data()
        self.court_names = self.format_court_names_data()
        self.death_penalty = self.format_death_penalty_data()
        self.e_filing_fee = self.format_e_filing_fee_data()
        self.e_filing_mandatory = self.format_e_filing_mandatory_data()
        self.funding = self.format_funding_data()
        self.neighbor = self.format_neighbor_data()
        self.neighbor_states = self.format_neighbor_states_data()
        self.panel_decision = self.format_panel_decision_data()
        self.pop_category = self.format_pop_category_data()
        self.pop_density = self.format_pop_density_data()
        self.rural = self.format_rural_data()
        self.trial_criminal_proc = self.format_trial_criminal_proc_data()
        self.trial_struct = self.format_trial_struct_data()
        self.us_state = self.format_us_state_data()
        self.us_state_court = self.format_us_state_court_data()
        self.us_state_neighbor = self.format_us_state_neighbor_data()
        
    def format_appeals_data(self):
        appeals = pd.read_csv('Vizathon-Data/AppealProcess.csv')
        return appeals

    def format_crim_appeals_data(self):
        crim_appeals_struct = pd.read_csv('Vizathon-Data/AppellateCriminalStructure.csv')
        return crim_appeals_struct

    def format_case_mgmt_data(self):
        case_mgmt = pd.read_csv('Vizathon-Data/CaseManagement.csv')
        return case_mgmt

    def format_case_type_data(self):
        case_type = pd.read_csv('Vizathon-Data/CaseType.csv')
        return case_type

    def format_caseload_size_data(self):
        caseload_size = pd.read_csv('Vizathon-Data/CaseloadSize.csv')
        return caseload_size

    def format_child_court_data(self):
        child_court = pd.read_csv('Vizathon-Data/ChildCourt.csv') 
        return child_court

    def format_courts_data(self):
        courts = pd.read_csv('Vizathon-Data/Court.csv')
        courts.drop('Unnamed: 9', axis=1, inplace=True)
        courts.drop('Unnamed: 10', axis=1, inplace=True)
        return courts

    def format_court_case_types_data(self):
        court_case_type = pd.read_csv('Vizathon-Data/CourtCaseType.csv')
        return court_case_type

    def format_court_court_names_data(self):
        court_court_names = pd.read_csv('Vizathon-Data/CourtCourtName.csv')
        return court_court_names

    def format_court_level_data(self):
        court_level = pd.read_csv('Vizathon-Data/CourtLevel.csv')
        return court_level

    def format_court_names_data(self):
        court_names = pd.read_csv('Vizathon-Data/CourtName.csv')
        return court_names

    def format_death_penalty_data(self):
        death_penalty = pd.read_csv('Vizathon-Data/DeathPenalty.csv')  
        return death_penalty

    def format_e_filing_fee_data(self):
        e_filing_fee = pd.read_csv('Vizathon-Data/EFilingFee.csv')
        return e_filing_fee

    def format_e_filing_mandatory_data(self):
        e_filing_mandatory = pd.read_csv('Vizathon-Data/EfilingMandatory.csv')
        return e_filing_mandatory

    def format_funding_data(self):
        funding = pd.read_csv('Vizathon-Data/Funding.csv')
        return funding

    def format_neighbor_data(self):
        neighbor = pd.read_csv('Vizathon-Data/Neighbor.csv')
        return neighbor

    def format_neighbor_states_data(self):
        neighbor_states = pd.read_csv('Vizathon-Data/USStateNeighbor.csv')
        return neighbor_states

    def format_panel_decision_data(self):
        panel_decision = pd.read_csv('Vizathon-Data/PanelDecision.csv')
        return panel_decision

    def format_pop_category_data(self):
        pop_category = pd.read_csv('Vizathon-Data/PopulationCategory.csv')
        return pop_category

    def format_pop_density_data(self):
        pop_density = pd.read_csv('Vizathon-Data/PopulationDensity.csv')
        return pop_density

    def format_rural_data(self):
        rural = pd.read_csv('Vizathon-Data/Rural.csv')
        return rural

    def format_trial_criminal_proc_data(self):
        trial_criminal_proc = pd.read_csv('Vizathon-Data/TrialCriminalProcessing.csv')
        return trial_criminal_proc

    def format_trial_struct_data(self):
        trial_struct = pd.read_csv('Vizathon-Data/TrialStructure.csv')
        return trial_struct

    def format_us_state_data(self):
        us_state = pd.read_csv('Vizathon-Data/USState.csv')
        return us_state
    
    def format_us_state_court_data(self):
        us_state_court = pd.read_csv('Vizathon-Data/USStateCourt.csv')
        return us_state_court

    def format_us_state_neighbor_data(self):
        us_state_neighbor = pd.read_csv('Vizathon-Data/USStateNeighbor.csv')
        return us_state_neighbor
    
    # ============= Misc. helper methods ==================
    #
    def get_neighboring_states(self, us_state_name=None):
        us_state_id = self.us_state[
            self.us_state['USStateName'] == us_state_name]['USStateID'].values[0]
        neighbor_state_ids = list(
            self.neighbor[self.neighbor['USStateID'] == us_state_id]['NeighborUSStateID'].values)
        all_neighbor_states = []
        for neighbor_state_id in neighbor_state_ids:
            try:
                all_neighbor_states.append(self.us_state[
                    self.us_state['USStateID'] == neighbor_state_id]['USStateName'].values[0])
            except IndexError:
                all_neighbor_states.append(None)
        return all_neighbor_states
    
    def get_states_and_neighbors_df(self, row):
        return self.get_neighboring_states(us_state_name=row['USStateName'])
    
    def get_population_density(self, row):
        return self.pop_density[self.pop_density['PopulationDensityID'] == row['PopulationDensityID']]['PopulationDensityDescription'].values[0]
    
    def get_population_category(self, row):
        return self.pop_category[
            self.pop_category['PopulationCategoryID'] == row['PopulationCategoryID']
        ]['PopulationCategoryDescription'].values[0]
    
    def get_rural_description(self, row):
        return self.rural[self.rural['RuralID'] == row['RuralID']]['RuralDescription'].values[0]
    
    def get_trial_structure(self, row):
        return self.trial_struct[
            self.trial_struct['TrialStructureID'] == row['TrialStructureID']
        ]['TrialStructureDescription'].values[0]
    
    def add_appellate_crim_struct(self, row):
        return self.crim_appeals_struct[
            self.crim_appeals_struct['AppellateCriminalStructureID'] == row['AppellateCriminalStructureID']
            ]['AppellateCriminalStructureDescription'].values[0]
    
    def add_trial_criminal_process(self, row):
        return self.trial_criminal_proc[
            self.trial_criminal_proc['TrialCriminalProcessingID'] == row['TrialCriminalProcessingID']
            ]['TrialCriminalProcessingDescription'].values[0]
    
    def get_death_penalty(self, row):
        return self.death_penalty[
            self.death_penalty['DeathPenaltyID'] == row['DeathPenaltyID']
            ]['DeathPenaltyDescription'].values[0]

    def get_trial_caseload_size(self, row):
        return self.caseload_size[
            self.caseload_size['CaseloadSizeID'] == row['TrialCaseloadSizeID']
        ]['CaseloadSizeDescription'].values[0]
    
    def get_pop_density_low(self, row):
        return row['PopulationDensity'].split('-')[0]

    def get_pop_density_high(self, row):
        return row['PopulationDensity'].split('-')[-1]
    
    def remove_highest_str(self, row, col):
        if row[col] == 'highest':
            return np.nan
        else:
            return row[col]
        
    def add_population_category_low(self, row):
        return row['PopulationCategory'].split(' to ')[0]

    def add_population_category_high(self, row):
        return row['PopulationCategory'].split(' to ')[-1]
    
    def remove_up_str(self, row, col):
        if row[col] == 'up':
            return 0
        else:
            return row[col]
        
    def get_rural_low(self, row):
        if '-' in row['Rural']:
            return row['Rural'].split('-')[0]
        elif 'Less than or equal to' in row['Rural']:
            return 0
        elif 'Greater than or equal to' in row['Rural']:
            return re.search('\d+', row['Rural']).group(0)
        elif 'Missing information' in row['Rural']:
            return np.nan
        
    def get_rural_high(self, row):
        if '-' in row['Rural']:
            return row['Rural'].split('-')[-1].rstrip('% of the population')
        elif 'Less than or equal to' in row['Rural']:
            return re.search('\d+', row['Rural']).group(0)
        elif 'Greater than or equal to' in row['Rural']:
            return 100
        elif 'Missing information' in row['Rural']:
            return np.nan
        
    def get_caseload_size_low(self, row):
        if row['CaseloadSize'] == 'Under 200 Thousand':
            return 0
        elif row['CaseloadSize'] == '201 Thousand-500 Thousand':
            return 201000
        elif row['CaseloadSize'] == '501 Thousand-1 Million':
            return 501000
        elif row['CaseloadSize'] == '1.1 Million-3 Million':
            return 1100000
        elif row['CaseloadSize'] == '3.1 Million-6 Million':
            return 3100000
        elif row['CaseloadSize'] == 'Over 6 Million':
            return 6000000
    
    def get_caseload_size_high(self, row):
        if row['CaseloadSize'] == 'Under 200 Thousand':
            return 200000
        elif row['CaseloadSize'] == '201 Thousand-500 Thousand':
            return 500000
        elif row['CaseloadSize'] == '501 Thousand-1 Million':
            return 1000000
        elif row['CaseloadSize'] == '1.1 Million-3 Million':
            return 3000000
        elif row['CaseloadSize'] == '3.1 Million-6 Million':
            return 6000000
        elif row['CaseloadSize'] == 'Over 6 Million':
            return 10000000

    def add_state_name(self, row):
        return self.all_states_display[
            self.all_states_display['USStateID'] == row['USStateID']
            ]['USStateName'].values[0]

    def add_funding_description(self, row):
        return self.funding[
            self.funding['FundingID'] == row['FundingID']]['FundingDescription'].values[0]

    def add_court_level_description(self, row):
        return self.court_level[
            self.court_level['CourtLevelID'] == row['CourtLevelID']
            ]['CourtLevelDescription'].values[0]

    def correct_court_level_description(self, row, col):
        if row[col] == 'Court of Last Resource':
            return 'Court of Last Resort'
        else:
            return row[col]

    def format_bools_for_bokeh(self, row):
        if row['AppealFromAdminAgency'] == True:
            return 'Yes'
        elif row['AppealFromAdminAgency'] == False:
            return 'No'

    def add_state_name_using_court_id(self, row):
        try:
            return self.us_states_and_courts[
                self.us_states_and_courts['CourtID'] == row['CourtID']]['State'].values[0]
        except IndexError:
            return np.nan
    
    def add_panel_decision_description(self, row):
        return self.panel_decision[
            self.panel_decision['PanelDecisionID'] == row['PanelDecisionID']
        ]['PanelDecisionDescription'].values[0]

    def add_case_mgmt_description(self, row):
        return self.case_mgmt[
            self.case_mgmt['CaseManagementID'] == row['CaseManagementID']
            ]['CaseManagementDescription'].values[0]

    def replace_neg_98_neg_99_with_nan(self, row, col):
        if row[col] in ['-99', '-98', -99, -98]:
            return np.nan
        else:
            return row[col]

    def add_court_name(self, row):
        try:
            return self.names_of_courts_by_state[
                self.names_of_courts_by_state['CourtID'] == row['CourtID']
                ]['CourtNameName'].values[0]
        except IndexError:
            return np.nan

    def add_court_case_description(self, row):
        return self.case_type[
            self.case_type['CaseTypeID'] == row['CaseTypeID']
            ]['CaseTypeDescription'].values[0]

    def add_parent_child_court_state(self, row):
        try:
            return self.names_of_courts_by_state[
                self.names_of_courts_by_state['CourtID'] == row['ChildCourtID']
                ]['State'].values[0]
        except IndexError:
            return np.nan

    def add_child_court(self, row):
        try:
            return self.names_of_courts_by_state[
                self.names_of_courts_by_state['CourtID'] == row['ChildCourtID']
                ]['CourtNameName'].values[0]
        except IndexError:
            return np.nan
        
    def add_parent_court(self, row):
        try:
            return self.names_of_courts_by_state[
                self.names_of_courts_by_state['CourtID'] == row['ParentCourtID']
                ]['CourtNameName'].values[0]
        except IndexError:
            return np.nan

    # ========= Methods that generate CSV output files ====
    #
    def create_all_court_case_types_df(self):
        self.all_court_case_types = self.court_case_type.copy()
        self.all_court_case_types['State'] = self.all_court_case_types.apply(
            self.add_state_name_using_court_id, axis=1)
        self.all_court_case_types['CourtName'] = self.all_court_case_types.apply(
            self.add_court_name, axis=1)
        self.all_court_case_types['CaseTypeDescription'] = self.all_court_case_types.apply(
            self.add_court_case_description, axis=1)
        self.all_court_case_types.to_csv(
            'viz_a_thon_data_sources/all_court_case_types.csv', index=False)
    
    def create_names_of_courts_by_state_df(self):
        self.names_of_courts_by_state = self.court_court_names.copy()
        self.names_of_courts_by_state['State'] = self.names_of_courts_by_state.apply(
            self.add_state_name_using_court_id, axis=1)
        self.names_of_courts_by_state = pd.merge(
            self.names_of_courts_by_state, 
            self.court_names, on='CourtNameID')
        self.names_of_courts_by_state['PanelDecisionDescription'] = \
            self.names_of_courts_by_state.apply(
                self.add_panel_decision_description, axis=1)
        self.names_of_courts_by_state['CaseManagementDescription'] = \
            self.names_of_courts_by_state.apply(self.add_case_mgmt_description, axis=1)
        self.names_of_courts_by_state['NumberPanels'] = self.names_of_courts_by_state.apply(
            self.replace_neg_98_neg_99_with_nan, args=('NumberPanels',), axis=1)
        self.names_of_courts_by_state['NumberPanels'] = \
            self.names_of_courts_by_state['NumberPanels'].str.replace('-Jan', '')
        self.names_of_courts_by_state['NumberPanels'] = \
            self.names_of_courts_by_state['NumberPanels'].str.replace('-100', '')
        # self.names_of_courts_by_state['NumberOfIndividualCourts'] = \
        #     self.names_of_courts_by_state.apply(
        #         self.replace_neg_98_neg_99_with_nan, 
        #         args=('NumberOfIndividualCourts',), axis=1)
        self.names_of_courts_by_state.to_csv(
            'viz_a_thon_data_sources/names_of_courts_by_state.csv', index=False)

    def create_all_states_display_df(self):
        """Create DataFrame `all_states_display`."""
        self.all_states_display = self.us_state.copy()
        self.all_states_display['NeighboringStates'] = self.all_states_display.apply(self.get_states_and_neighbors_df, axis=1)
        self.all_states_display['NeighboringStates'] = self.all_states_display['NeighboringStates'].astype('str')
        self.all_states_display['NeighboringStates'] = self.all_states_display['NeighboringStates'].str.replace('[', '')
        self.all_states_display['NeighboringStates'] = self.all_states_display['NeighboringStates'].str.replace(']', '')
        self.all_states_display['PopulationDensity'] = self.all_states_display.apply(self.get_population_density, axis=1)
        self.all_states_display['PopulationCategory'] = self.all_states_display.apply(self.get_population_category, axis=1)
        self.all_states_display['Rural'] = self.all_states_display.apply(self.get_rural_description, axis=1)
        self.all_states_display['TrialStructure'] = self.all_states_display.apply(self.get_trial_structure, axis=1)
        self.all_states_display['AppCrimStructure'] = self.all_states_display.apply(self.add_appellate_crim_struct, axis=1)
        self.all_states_display['TrialCriminalProc'] = self.all_states_display.apply(self.add_trial_criminal_process, axis=1)
        self.all_states_display['DeathPenalty'] = self.all_states_display.apply(self.get_death_penalty, axis=1)
        self.all_states_display['CaseloadSize'] = self.all_states_display.apply(self.get_trial_caseload_size, axis=1)
        self.all_states_display['PopulationLow'] = self.all_states_display.apply(self.get_pop_density_low, axis=1)
        self.all_states_display['PopulationHigh'] = self.all_states_display.apply(self.get_pop_density_high, axis=1)
        self.all_states_display['PopulationHigh'] = self.all_states_display.apply(
            self.remove_highest_str, args=('PopulationHigh',), axis=1)
        self.all_states_display['PopulationLow'] = self.all_states_display['PopulationLow'].astype('float64')
        self.all_states_display['PopulationHigh'] = self.all_states_display['PopulationHigh'].astype('float64')
        self.all_states_display['PopulationCategoryLow'] = self.all_states_display.apply(
            self.add_population_category_low, axis=1)
        self.all_states_display['PopulationCategoryHigh'] = self.all_states_display.apply(
            self.add_population_category_high, axis=1)
        self.all_states_display['PopulationCategoryHigh'] = self.all_states_display.apply(
            self.remove_highest_str, args=('PopulationCategoryHigh',), axis=1)
        self.all_states_display['PopulationCategoryLow'] = self.all_states_display.apply(
            self.remove_up_str, args=('PopulationCategoryLow',), axis=1)
        self.all_states_display['PopulationCategoryLow'] = self.all_states_display['PopulationCategoryLow'].astype('float64')
        self.all_states_display['PopulationCategoryHigh'] = self.all_states_display['PopulationCategoryHigh'].astype('float64')
        self.all_states_display['RuralLow'] = self.all_states_display.apply(self.get_rural_low, axis=1)
        self.all_states_display['RuralLow'] = self.all_states_display['RuralLow'].astype('float64')
        self.all_states_display['RuralHigh'] = self.all_states_display.apply(self.get_rural_high, axis=1)
        self.all_states_display['RuralHigh'] = self.all_states_display['RuralHigh'].astype('float64')
        self.all_states_display['CaseloadLow'] = self.all_states_display.apply(self.get_caseload_size_low, axis=1)
        self.all_states_display['CaseloadHigh'] = self.all_states_display.apply(self.get_caseload_size_high, axis=1)
        self.all_states_display.to_csv('viz_a_thon_data_sources/all_states_display.csv', index=False)
    
    def create_us_states_and_courts_df(self):
        self.us_states_and_courts = pd.merge(self.us_state_court, self.courts, on='CourtID')
        self.us_states_and_courts['State'] = self.us_states_and_courts.apply(self.add_state_name, axis=1)
        self.us_states_and_courts['FundingDescription'] = self.us_states_and_courts.apply(
            self.add_funding_description, axis=1)
        self.us_states_and_courts['CourtLevelDescription'] = self.us_states_and_courts.apply(
            self.add_court_level_description, axis=1)
        self.us_states_and_courts['CourtLevelDescription'] = self.us_states_and_courts.apply(
            self.correct_court_level_description, args=('CourtLevelDescription',), axis=1)
        self.us_states_and_courts['AppealFromAdminAgency'] = self.us_states_and_courts.apply(
            self.format_bools_for_bokeh, axis=1)
        self.us_states_and_courts['Notes'] = self.us_states_and_courts['Notes'].str.replace('-99', '')
        self.us_states_and_courts.fillna('', inplace=True)
        # self.us_states_and_courts['URL'] = self.us_states_and_courts.apply(
        #     self.replace_neg_98_neg_99_with_nan, args=('Link',), axis=1)
        # self.us_states_and_courts['Link'] = self.us_states_and_courts['Link'].str.replace('-99', '')
        self.us_states_and_courts.to_csv('viz_a_thon_data_sources/us_states_and_courts.csv', index=False)

    def create_court_hierarchy_df(self):
        self.court_hierarchy = self.appeals.copy()
        self.court_hierarchy['State'] = self.court_hierarchy.apply(
            self.add_parent_child_court_state, axis=1)
        self.court_hierarchy['ChildCourtName'] = self.court_hierarchy.apply(
            self.add_child_court, axis=1)
        self.court_hierarchy['ParentCourtName'] = self.court_hierarchy.apply(
            self.add_parent_court, axis=1)
        self.court_hierarchy.drop_duplicates(inplace=True)
        self.court_hierarchy.to_csv(
            'viz_a_thon_data_sources/court_hierarchy.csv', index=False)

    # Main, runner function
    def generate_data(self):
        """Generate CSV files for use by Bokeh dashboard."""
        self.create_all_states_display_df()
        self.create_us_states_and_courts_df()
        self.create_names_of_courts_by_state_df()
        self.create_all_court_case_types_df()
        self.create_court_hierarchy_df()
