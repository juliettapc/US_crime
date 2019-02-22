census_regions = {'Northeast' : ['Connecticut', 'Maine', 'Massachusetts', 'New Hampshire', \
                                 'Rhode Island', 'Vermont', 'New Jersey', 'New York', 'Pennsylvania'],
                  'South' : ['Delaware', 'Florida', 'Georgia', 'Maryland', 'North Carolina', \
                             'South Carolina', 'West virginia', 'Virginia', 'Washington D.C.', 'District of Columbia',\
                             'Alabama', 'Kentucky', 'Mississippi', 'Tennessee', 'Arkansas', 'Louisiana', 'Oklahoma', 'Texas'],
                  'Midwest' : ['Illinois', 'Indiana', 'Michigan', 'Ohio', 'Wisconsin', 'Iowa', 'Kansas', \
                               'Minnesota', 'Missouri', 'Nebraska', 'North Dakota', 'South Dakota'],
                  'West' : ['Alaska', 'Hawaii', 'California', 'Oregon', 'Washington', 'Idaho', 'Nevada', 'Arizona', \
                            'Utah', 'Montana', 'Wyoming', 'Colorado', 'New Mexico']
                 }

economic_regions = {
    'Non-contiguous' : ['Alaska', 'Hawaii'],
    'Pacific' : ['California', 'Oregon', 'Washington', 'Nevada'],
    'Rocky Mountain' : ['Utah', 'Idaho', 'Montana', 'Wyoming', 'Colorado'],
    'Southwest': ['Arizona', 'New Mexico', 'Texas', 'Oklahoma'],
    'Plains': ['North Dakota', 'South Dakota', 'Nebraska', 'Kansas', 'Missouri', 'Iowa', 'Minnesota'],
    'Great Lakes': ['Wisconsin', 'Illinois', 'Indiana', 'Michigan', 'Ohio'],
    'Southeast': ['Louisiana', 'Mississippi', 'Arkansas', 'Alabama', 'Georgia', 'Florida',
                  'South Carolina', 'North Carolina', 'Tennessee', 'Kentucky', 'West Virginia', 'Virginia'],
    'Mideast': ['Maryland', 'Delaware', 'Pennsylvania', 'New Jersey', 'New York', 'Washington D.C.', 'District of Columbia'],
    'New England': ['Connecticut', 'Rhode Island', 'Massachusetts', 'Vermont', 'New Hampshire', 'Maine']
}

mod_economic_regions = {
    'Non-contiguous' : ['Alaska', 'Hawaii'],
    'Pacific' : ['California', 'Oregon', 'Washington', 'Nevada'],
    'Rocky Mountain' : ['Utah', 'Idaho', 'Montana', 'Wyoming', 'Colorado'],
    'Southwest': ['Arizona', 'New Mexico', 'Texas', 'Oklahoma'],
    'Plains': ['North Dakota', 'South Dakota', 'Nebraska', 'Kansas', 'Missouri', 'Iowa', 'Minnesota'],
    'Great Lakes': ['Wisconsin', 'Illinois', 'Indiana', 'Michigan', 'Ohio'],
    'Southeast': ['Louisiana', 'Mississippi', 'Arkansas', 'Alabama', 'Georgia', 'Florida',
                  'South Carolina', 'North Carolina', 'Tennessee', 'Kentucky', 'West Virginia', 'Virginia'],
    'Northeast': ['Maryland', 'Delaware', 'Pennsylvania', 'New Jersey', 'New York', 'Washington D.C.', 'District of Columbia',\
                  'Connecticut', 'Rhode Island', 'Massachusetts', 'Vermont', 'New Hampshire', 'Maine']
}

def region_identifier(val, regions):
    '''
    Given a location, match the region
    '''
    import pandas as pd
    #Get the translation 
    abbrvdf = pd.read_csv('../../Data/geography/state_abbreviations.csv')
    abbrvtrans = dict( zip(abbrvdf.Abbreviation, abbrvdf.Name) )
    #Translate to the statename
    tval = abbrvtrans[val]
    #run through the regions
    for region, state_list in regions.items():
        for state in state_list:
            if state.lower() in tval.lower():
                #Check on Washington
                if state=='Washington':
                    if 'd.c.' not in tval.lower() and 'dc' not in tval.lower():
                        return region
                else:
                    return region
    print("Error (Undetected Region)", tval)


def add_census_regions(df):
    '''
    Add the census region as a column to the dataframe
    '''
    df['Region'] = df.State.apply(lambda x: region_identifier(x, census_regions))
    return df

def add_economic_regions(df):
    df['Region'] = df.State.apply(lambda x: region_identifier(x, economic_regions))
    return df

def add_mod_economic_regions(df):
    df['Region'] = df.State.apply(lambda x: region_identifier(x, mod_economic_regions))
    return df
