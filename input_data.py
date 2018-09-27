"""This file creates DataFrames to serve as input for Bokeh Dashboard."""

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
        
    def format_crim_appeals_data(self):
        crim_appeals_struct = pd.read_csv('Vizathon-Data/AppellateCriminalStructure.csv')
        
    def format_case_mgmt_data(self):
        case_mgmt = pd.read_csv('Vizathon-Data/CaseManagement.csv')
        
    def format_case_type_data(self):
        case_type = pd.read_csv('Vizathon-Data/CaseType.csv')
        
    def format_caseload_size_data(self):
        caseload_size = pd.read_csv('Vizathon-Data/CaseloadSize.csv')
        
    def format_child_court_data(self):
        child_court = pd.read_csv('Vizathon-Data/ChildCourt.csv') 
    
    def format_courts_data(self):
        courts = pd.read_csv('Vizathon-Data/Court.csv')
        self.courts.drop('Unnamed: 9', axis=1, inplace=True)
        self.courts.drop('Unnamed: 10', axis=1, inplace=True)
    
    def format_court_case_types_data(self):
        court_case_type = pd.read_csv('Vizathon-Data/CourtCaseType.csv')
    
    def format_court_court_names_data(self):
        court_court_names = pd.read_csv('Vizathon-Data/CourtCourtName.csv')
        
    def format_court_level_data(self):
        court_level = pd.read_csv('Vizathon-Data/CourtLevel.csv')
    
    def format_court_names_data(self):
        court_names = pd.read_csv('Vizathon-Data/CourtName.csv')
        
    def format_death_penalty_data(self):
        death_penalty = pd.read_csv('Vizathon-Data/DeathPenalty.csv')  
    
    def format_e_filing_fee_data(self):
        e_filing_fee = pd.read_csv('Vizathon-Data/EFilingFee.csv')
    
    def format_e_filing_mandatory_data(self):
        e_filing_mandatory = pd.read_csv('Vizathon-Data/EfilingMandatory.csv')
    
    def format_funding_data(self):
        funding = pd.read_csv('Vizathon-Data/Funding.csv')
    
    def format_neighbor_data(self):
        neighbor = pd.read_csv('Vizathon-Data/Neighbor.csv')
    
    def format_neighbor_states_data(self):
        neighbor_states = pd.read_csv('Vizathon-Data/USStateNeighbor.csv')
    
    def format_panel_decision_data(self):
        panel_decision = pd.read_csv('Vizathon-Data/PanelDecision.csv')
    
    def format_pop_category_data(self):
        pop_category = pd.read_csv('Vizathon-Data/PopulationCategory.csv')
    
    def format_pop_density_data(self):
        pop_density = pd.read_csv('Vizathon-Data/PopulationDensity.csv')
    
    def format_rural_data(self):
        rural = pd.read_csv('Vizathon-Data/Rural.csv')
    
    def format_trial_criminal_proc_data(self):
        trial_criminal_proc = pd.read_csv('Vizathon-Data/TrialCriminalProcessing.csv')
    
    def format_trial_struct_data(self):
        trial_struct = pd.read_csv('Vizathon-Data/TrialStructure.csv')
    
    def format_us_state_data(self):
        us_state = pd.read_csv('Vizathon-Data/USState.csv')
        return us_state
    
    def format_us_state_court_data(self):
        us_state_court = pd.read_csv('Vizathon-Data/USStateCourt.csv')
    
    def format_us_state_neighbor_data(self):
        us_state_neighbor = pd.read_csv('Vizathon-Data/USStateNeighbor.csv')
    
    
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
                all_neighbor_states.append(us_state[
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
    
    def get_trial_structure(self.row):
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
            return 10000000 # <<< Arbitrary value
    
    # ========= Methods that generate CSV output files ====
    #
    def create_all_court_case_types_df(self):
        pass
    
    def create_names_of_courts_by_state_df(self):
        pass
    
    def create_all_states_display_df(self):
        """Create DataFrame `all_states_display`."""
        all_states_display = self.us_state.copy()
        all_states_display['NeighboringStates'] = all_states_display.apply(self.get_states_and_neighbors_df, axis=1)
        all_states_display['PopulationDensity'] = all_states_display.apply(self.get_population_density, axis=1)
        all_states_display['PopulationCategory'] = all_states_display.apply(self.get_population_category, axis=1)
        all_states_display['Rural'] = all_states_display.apply(self.get_rural_description, axis=1)
        all_states_display['TrialStructure'] = all_states_display.apply(self.get_trial_structure, axis=1)
        all_states_display['AppCrimStructure'] = all_states_display.apply(self.add_appellate_crim_struct, axis=1)
        all_states_display['TrialCriminalProc'] = all_states_display.apply(self.add_trial_criminal_process, axis=1)
        all_states_display['DeathPenalty'] = all_states_display.apply(self.get_death_penalty, axis=1)
        all_states_display['CaseloadSize'] = all_states_display.apply(self.get_trial_caseload_size, axis=1)
        all_states_display['PopulationLow'] = all_states_display.apply(self.get_pop_density_low, axis=1)
        all_states_display['PopulationHigh'] = all_states_display.apply(self.get_pop_density_high, axis=1)
        all_states_display['PopulationHigh'] = all_states_display.apply(
            self.remove_highest_str, args=('PopulationHigh',), axis=1)
        all_states_display['PopulationLow'] = all_states_display['PopulationLow'].astype('float64')
        all_states_display['PopulationHigh'] = all_states_display['PopulationHigh'].astype('float64')
        all_states_display['PopulationCategoryLow'] = all_states_display.apply(self.add_population_category_low, axis=1)
        all_states_display['PopulationCategoryHigh'] = all_states_display.apply(self.add_population_category_high, axis=1)
        all_states_display['PopulationCategoryHigh'] = all_states_display.apply(
            self.remove_highest_str, args=('PopulationCategoryHigh',), axis=1)
        all_states_display['PopulationCategoryLow'] = all_states_display.apply(
            self.remove_up_str, args=('PopulationCategoryLow',), axis=1)
        all_states_display['PopulationCategoryLow'] = all_states_display['PopulationCategoryLow'].astype('float64')
        all_states_display['PopulationCategoryHigh'] = all_states_display['PopulationCategoryHigh'].astype('float64')
        all_states_display['RuralLow'] = all_states_display.apply(self.get_rural_low, axis=1)
        all_states_display['RuralLow'] = all_states_display['RuralLow'].astype('float64')
        all_states_display['RuralHigh'] = all_states_display.apply(self.get_rural_high, axis=1)
        all_states_display['RuralHigh'] = all_states_display['RuralHigh'].astype('float64')
        all_states_display['CaseloadLow'] = all_states_display.apply(self.get_caseload_size_low, axis=1)
        all_states_display['CaseloadHigh'] = all_states_display.apply(self.get_caseload_size_high, axis=1)
        all_states_display.to_csv('viz_a_thon_data_sources/all_states_display.csv', index=False)
    
    def create_us_states_and_courts_df(self):
        pass
    
    def create_court_hierarchy_df(self):
        pass

