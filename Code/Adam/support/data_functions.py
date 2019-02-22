def load_all_census(indir = '../../Data/census/'):
    import glob
    import pandas as pd
    import statsmodels.formula.api as smf
    import sys
    sys.path.append('..')
    import support.geography as geo
    #Races
    races =  ['WhitePop', 'BlackPop', 'NativePop', 'HispanicPop', 'AsianPop']
    years = [1960, 1970, 1980, 1990, 2000, 2010]
    #Loading
    tdfs = []
    for fname in glob.glob(indir + '/*csv'):
        tdf = pd.read_csv(fname)
        #Calculate the YoY changes
        tdf.sort_values('Year', inplace=True)
        #Calculate the shares
        for race_label in races:
            tdf[race_label + 'Frac'] = tdf[race_label] / tdf['TotalPop']
            tdf[race_label + 'YoY'] = tdf[race_label + 'Frac'].diff() / 10
            fitted = smf.ols(formula = race_label + 'Frac ~ Year', data = tdf).fit()
            tdf[race_label + 'Slope'] = fitted.params.Year 
        #Calculate the longitudinal slope for hte total pop
        fitted = smf.ols(formula = 'TotalPop ~ Year', data = tdf).fit()
        tdf['TotalPopSlope'] = fitted.params.Year 
        #Append the dataframe
        tdfs.append( tdf)
    #Concatenate
    fulldf = pd.concat(tdfs)
    fulldf = geo.add_mod_economic_regions(fulldf)
    #Calculate the YoY slope of population changes
    return fulldf

def infer_single_census(fname, form=None):
    import glob
    import pandas as pd
    import numpy as np
    import statsmodels.formula.api as smf
    import sys
    sys.path.append('..')
    import support.geography as geo
    #Races
    races =  ['WhitePop', 'BlackPop', 'NativePop', 'HispanicPop', 'AsianPop']
    years = [1960, 1970, 1980, 1990, 2000, 2010]
    #Load the real data
    tdf = pd.read_csv(fname)
    tdf.replace(0, np.nan)
    #Calculate the YoY changes
    tdf.sort_values('Year', inplace=True)
    #Create the new dataframe
    pred_df = pd.DataFrame(list(range(1960, 2011)), columns = ['Year'])
    #Get the state and city
    pred_df['State'] = tdf['State'].values[0]
    pred_df['City'] = tdf['City'].values[0]
    #Run the routine
    pred_df = pop_inference_routine(pred_df, tdf, form = form)
    return pred_df

def infer_all_census(indir = '../../Data/census/', restrict_pop = True):
    '''
    inputs:
        * indir - directory of census files
        * restrict_pop - only include cities with >50k total population
    output:
        * fulldf - census and homicide data
    '''
    import glob
    import pandas as pd
    import numpy as np
    import statsmodels.formula.api as smf
    import sys
    sys.path.append('..')
    import support.geography as geo
    #Races
    races =  ['WhitePop', 'BlackPop', 'NativePop', 'HispanicPop', 'AsianPop']
    years = [1960, 1970, 1980, 1990, 2000, 2010]
    #Loading
    tdfs = []
    for fname in glob.glob(indir + '/*csv'):
        #Load the real data
        tdf = pd.read_csv(fname)
        tdf.replace(0, np.nan)
        #Check if the city meets the inclusion criteria
        if restrict_pop == True:
            #Do a temporary query
            aggdf = tdf[tdf.TotalPop > 50000]
            #Make sure we still have all six years, if we don't break out of hte loop for this city
            if len(aggdf.BlackPop) != 6:
                continue
        #Calculate the YoY changes
        tdf.sort_values('Year', inplace=True)
        #Create the new dataframe
        pred_df = pd.DataFrame(list(range(1960, 2011)), columns = ['Year'])
        #Get the state and city
        pred_df['State'] = tdf['State'].values[0]
        pred_df['City'] = tdf['City'].values[0]
        #Run the inference routine
        pred_df = pop_inference_routine(pred_df, tdf)
        #Append the dataframe
        tdfs.append( pred_df )
    #Concatenate
    fulldf = pd.concat(tdfs)
    fulldf = geo.add_mod_economic_regions(fulldf)
    return fulldf

def pop_inference_routine(pred_df, tdf, form = None):
    import numpy as np
    import pandas as pd
    import statsmodels.formula.api as smf
    #Races
    races =  ['WhitePop', 'BlackPop', 'NativePop', 'HispanicPop', 'AsianPop']
    years = [1960, 1970, 1980, 1990, 2000, 2010]
    #Formulas
    lin_form = '%s ~ Year'
    quad_form = '%s ~ Year + np.power(Year, 2)'
    cub_form = '%s ~ Year + np.power(Year, 2) + np.power(Year, 3)'
    quart_form = '%s ~ Year + np.power(Year, 2) + np.power(Year, 3) + np.power(Year, 4)'
    #Run the fit
    pred_df['TotalPop'] = smf.ols(formula = lin_form % 'TotalPop', data = tdf).fit().predict(pred_df)
    #Calculate the shares
    for i, (race_label) in enumerate(races):
        row_count = len(tdf[tdf[race_label] > 0])
        start_year = years[row_count - 6]
        #Set up the formula to use
        if form == None:
            if race_label == 'AsianPop' or race_label == 'NativePop':
                form = lin_form
            else:
                form = quad_form
        #Create the fit
        fitted = smf.ols(formula = form % race_label, data = tdf.loc[:, [race_label, 'Year']].dropna()).fit()
        pred_df[race_label] = fitted.predict(pred_df)
        pred_df.loc[pred_df.Year < start_year, race_label] = np.nan
        #Now calculate the other metrics
        pred_df[race_label + 'Frac'] = pred_df[race_label] / pred_df['TotalPop']
        pred_df[race_label + 'YoY'] = pred_df[race_label + 'Frac'].diff() 
        fitted = smf.ols(formula = race_label + 'Frac ~ Year', data = pred_df).fit()
        pred_df[race_label + 'Slope'] = fitted.params.Year 
    #Calculate the longitudinal slope for hte total pop
    fitted = smf.ols(formula = 'TotalPop ~ Year', data = pred_df).fit()
    pred_df['TotalPopSlope'] = fitted.params.Year 
    return pred_df

def load_all_crime(indir = '../../Data/crime/'):
    import glob
    import pandas as pd
    tdfs = []
    for fname in glob.glob(indir + '/*csv'):
        splitname = fname.split('/')[-1].split('.csv')[0].split('_')
        state = splitname[0]
        city = ''.join(splitname[1:])
        tdf = pd.read_csv(fname)
        tdf['State'] = state
        tdf['City'] = city
        tdfs.append(tdf)
    fulldf = pd.concat(tdfs)
    return fulldf

def produce_merged_dataframe(census_inference=False):
    import pandas as pd
    if census_inference == True:
        censusdf = infer_all_census()
    else:
        censusdf = load_all_census()
    crimedf = load_all_crime()
    mdf = pd.merge(censusdf, crimedf, on= ['Year', 'State', 'City'])
    #Calculate the crime rates
    for crime_label in ['Murder', 'Robbery', 'Assault', 'Burglary']:
        mdf[crime_label + 'Rate'] = mdf[crime_label] / (mdf['TotalPop'] / 10000)
    return mdf


#########
# Veterans
########
def load_veteran_population(infile = '../../Data/veterans/populations.xlsx'):
    '''
    Loads the veteran population data
    input:
        * infile - file of populations. years are separate sheets and each year is broken out by conflict
    output:
        * vetpop - DataFrame, columns are: Conflict,Estimate,Error,Year
    '''
    import pandas as pd
    sheet_years = range(2005, 2016)
    dfs = []
    for sheet_year in sheet_years:
        tdf = pd.read_excel(infile, sheetname = str(sheet_year))
        tdf['Year'] = sheet_year
        dfs.append( tdf )
    vetpop = pd.concat(dfs)
    return vetpop

def load_veteran_population_by_conflict():
    '''
    Separates the veteran populations into separate dataframes for each conflict
    input: 
        None
    output:
        * conflict_vetpop - dictionary, {'conflict' : dataframe, ...}
    '''
    vetpop = load_veteran_population()
    conflicts = vetpop.Conflict.unique().tolist()
    conflict_vetpop = {}
    for conflict in conflicts:
        conflict_vetpop[conflict] = vetpop[vetpop.Conflict == conflict][:]
    return conflict_vetpop

def load_veteran_incarceration(infile = '../../Data/veterans/incarceration.xlsx'):
    '''
    input:
        * infile - incarceration population data
    returns:
        * nat_vetpop - dict, {'Population': df, 'Prison': df, 'Jail': df}
    '''
    import pandas as pd
    sheet_names = ['Population', 'Prison', 'Jail']
    nat_vetpop = {}
    for sheetname in sheet_names:
        nat_vetpop[sheetname] = pd.read_excel(infile, sheetname = sheetname)
    return nat_vetpop

def load_city_unemployment(indir = '../../Data/unemployment/'):
    '''
    input:
        * indir - directory of unemployment 
    output:
        * city_unem - dataframe, monthly
        * agg_city_unem - datafram, yearly
    '''
    import pandas as pd
    import glob
    import numpy as np

    dfset, aggdfset = [], []
    for fname in glob.glob(indir + '*csv'):
        city, state = fname.split('/')[-1].split('.csv')[0].split('_')
        tdf = pd.read_csv(fname)
        tdf.replace('-', np.nan, inplace=True)
        tdf.dropna(inplace=True)
        #Change it out to cut the LAU work
        newdf = tdf.loc[:, ['Year', 'Period']]
        #Rename unemployment over
        newdf['Unemployment'] = pd.to_numeric(tdf.Value)
        #Set City and State
        newdf['City'] = city
        newdf['State'] = state
        #Append it out
        dfset.append(newdf)
        #aggregate by year
        aggdf = newdf.groupby('Year').agg('mean')
        aggdf.reset_index(inplace=True)
        aggdf['City'] = city
        aggdf['State'] = state
        aggdfset.append(aggdf)
    #Concat
    city_unem = pd.concat(dfset)
    #Concat the aggs
    agg_city_unem = pd.concat(aggdfset)
    return city_unem, agg_city_unem

