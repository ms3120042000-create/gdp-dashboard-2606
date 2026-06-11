import streamlit as st
import pandas as pd
import math
from pathlib import Path

st.set_page_config(
    page_title='GDP dashboard',
    page_icon=':earth_americas:',
)

# World Bank region classification by ISO 3166 alpha-3 code
REGION_MAP = {
    # East Asia & Pacific
    'BRN': 'East Asia & Pacific', 'CHN': 'East Asia & Pacific', 'HKG': 'East Asia & Pacific',
    'IDN': 'East Asia & Pacific', 'JPN': 'East Asia & Pacific', 'KHM': 'East Asia & Pacific',
    'KOR': 'East Asia & Pacific', 'LAO': 'East Asia & Pacific', 'MAC': 'East Asia & Pacific',
    'MMR': 'East Asia & Pacific', 'MNG': 'East Asia & Pacific', 'MYS': 'East Asia & Pacific',
    'PHL': 'East Asia & Pacific', 'PRK': 'East Asia & Pacific', 'SGP': 'East Asia & Pacific',
    'THA': 'East Asia & Pacific', 'TLS': 'East Asia & Pacific', 'VNM': 'East Asia & Pacific',
    'AUS': 'East Asia & Pacific', 'FJI': 'East Asia & Pacific', 'FSM': 'East Asia & Pacific',
    'KIR': 'East Asia & Pacific', 'MHL': 'East Asia & Pacific', 'NRU': 'East Asia & Pacific',
    'NZL': 'East Asia & Pacific', 'PLW': 'East Asia & Pacific', 'PNG': 'East Asia & Pacific',
    'SLB': 'East Asia & Pacific', 'TON': 'East Asia & Pacific', 'TUV': 'East Asia & Pacific',
    'VUT': 'East Asia & Pacific', 'WSM': 'East Asia & Pacific',
    # Europe & Central Asia
    'ALB': 'Europe & Central Asia', 'AND': 'Europe & Central Asia', 'ARM': 'Europe & Central Asia',
    'AUT': 'Europe & Central Asia', 'AZE': 'Europe & Central Asia', 'BEL': 'Europe & Central Asia',
    'BGR': 'Europe & Central Asia', 'BIH': 'Europe & Central Asia', 'BLR': 'Europe & Central Asia',
    'CHE': 'Europe & Central Asia', 'CYP': 'Europe & Central Asia', 'CZE': 'Europe & Central Asia',
    'DEU': 'Europe & Central Asia', 'DNK': 'Europe & Central Asia', 'ESP': 'Europe & Central Asia',
    'EST': 'Europe & Central Asia', 'FIN': 'Europe & Central Asia', 'FRA': 'Europe & Central Asia',
    'FRO': 'Europe & Central Asia', 'GBR': 'Europe & Central Asia', 'GEO': 'Europe & Central Asia',
    'GRC': 'Europe & Central Asia', 'HRV': 'Europe & Central Asia', 'HUN': 'Europe & Central Asia',
    'IRL': 'Europe & Central Asia', 'ISL': 'Europe & Central Asia', 'ITA': 'Europe & Central Asia',
    'KAZ': 'Europe & Central Asia', 'KGZ': 'Europe & Central Asia', 'LIE': 'Europe & Central Asia',
    'LTU': 'Europe & Central Asia', 'LUX': 'Europe & Central Asia', 'LVA': 'Europe & Central Asia',
    'MCO': 'Europe & Central Asia', 'MDA': 'Europe & Central Asia', 'MKD': 'Europe & Central Asia',
    'MLT': 'Europe & Central Asia', 'MNE': 'Europe & Central Asia', 'NLD': 'Europe & Central Asia',
    'NOR': 'Europe & Central Asia', 'POL': 'Europe & Central Asia', 'PRT': 'Europe & Central Asia',
    'ROU': 'Europe & Central Asia', 'RUS': 'Europe & Central Asia', 'SMR': 'Europe & Central Asia',
    'SRB': 'Europe & Central Asia', 'SVK': 'Europe & Central Asia', 'SVN': 'Europe & Central Asia',
    'SWE': 'Europe & Central Asia', 'TJK': 'Europe & Central Asia', 'TKM': 'Europe & Central Asia',
    'TUR': 'Europe & Central Asia', 'UKR': 'Europe & Central Asia', 'UZB': 'Europe & Central Asia',
    'XKX': 'Europe & Central Asia',
    # Latin America & Caribbean
    'ABW': 'Latin America & Caribbean', 'ARG': 'Latin America & Caribbean',
    'ATG': 'Latin America & Caribbean', 'BHS': 'Latin America & Caribbean',
    'BLZ': 'Latin America & Caribbean', 'BOL': 'Latin America & Caribbean',
    'BRA': 'Latin America & Caribbean', 'BRB': 'Latin America & Caribbean',
    'CHL': 'Latin America & Caribbean', 'COL': 'Latin America & Caribbean',
    'CRI': 'Latin America & Caribbean', 'CUB': 'Latin America & Caribbean',
    'CUW': 'Latin America & Caribbean', 'DMA': 'Latin America & Caribbean',
    'DOM': 'Latin America & Caribbean', 'ECU': 'Latin America & Caribbean',
    'GRD': 'Latin America & Caribbean', 'GTM': 'Latin America & Caribbean',
    'GUY': 'Latin America & Caribbean', 'HND': 'Latin America & Caribbean',
    'HTI': 'Latin America & Caribbean', 'JAM': 'Latin America & Caribbean',
    'KNA': 'Latin America & Caribbean', 'LCA': 'Latin America & Caribbean',
    'MEX': 'Latin America & Caribbean', 'NIC': 'Latin America & Caribbean',
    'PAN': 'Latin America & Caribbean', 'PER': 'Latin America & Caribbean',
    'PRY': 'Latin America & Caribbean', 'PRI': 'Latin America & Caribbean',
    'SLV': 'Latin America & Caribbean', 'SUR': 'Latin America & Caribbean',
    'TTO': 'Latin America & Caribbean', 'URY': 'Latin America & Caribbean',
    'VCT': 'Latin America & Caribbean', 'VEN': 'Latin America & Caribbean',
    # Middle East & North Africa
    'BHR': 'Middle East & N. Africa', 'DJI': 'Middle East & N. Africa',
    'DZA': 'Middle East & N. Africa', 'EGY': 'Middle East & N. Africa',
    'IRN': 'Middle East & N. Africa', 'IRQ': 'Middle East & N. Africa',
    'ISR': 'Middle East & N. Africa', 'JOR': 'Middle East & N. Africa',
    'KWT': 'Middle East & N. Africa', 'LBN': 'Middle East & N. Africa',
    'LBY': 'Middle East & N. Africa', 'MAR': 'Middle East & N. Africa',
    'OMN': 'Middle East & N. Africa', 'PSE': 'Middle East & N. Africa',
    'QAT': 'Middle East & N. Africa', 'SAU': 'Middle East & N. Africa',
    'SYR': 'Middle East & N. Africa', 'TUN': 'Middle East & N. Africa',
    'ARE': 'Middle East & N. Africa', 'YEM': 'Middle East & N. Africa',
    # North America
    'BMU': 'North America', 'CAN': 'North America', 'GRL': 'North America',
    'USA': 'North America',
    # South Asia
    'AFG': 'South Asia', 'BGD': 'South Asia', 'BTN': 'South Asia',
    'IND': 'South Asia', 'LKA': 'South Asia', 'MDV': 'South Asia',
    'NPL': 'South Asia', 'PAK': 'South Asia',
    # Sub-Saharan Africa
    'AGO': 'Sub-Saharan Africa', 'BDI': 'Sub-Saharan Africa', 'BEN': 'Sub-Saharan Africa',
    'BFA': 'Sub-Saharan Africa', 'BWA': 'Sub-Saharan Africa', 'CAF': 'Sub-Saharan Africa',
    'CIV': 'Sub-Saharan Africa', 'CMR': 'Sub-Saharan Africa', 'COD': 'Sub-Saharan Africa',
    'COG': 'Sub-Saharan Africa', 'COM': 'Sub-Saharan Africa', 'CPV': 'Sub-Saharan Africa',
    'ERI': 'Sub-Saharan Africa', 'ETH': 'Sub-Saharan Africa', 'GAB': 'Sub-Saharan Africa',
    'GHA': 'Sub-Saharan Africa', 'GIN': 'Sub-Saharan Africa', 'GMB': 'Sub-Saharan Africa',
    'GNB': 'Sub-Saharan Africa', 'GNQ': 'Sub-Saharan Africa', 'KEN': 'Sub-Saharan Africa',
    'LBR': 'Sub-Saharan Africa', 'LSO': 'Sub-Saharan Africa', 'MDG': 'Sub-Saharan Africa',
    'MLI': 'Sub-Saharan Africa', 'MOZ': 'Sub-Saharan Africa', 'MRT': 'Sub-Saharan Africa',
    'MUS': 'Sub-Saharan Africa', 'MWI': 'Sub-Saharan Africa', 'MYT': 'Sub-Saharan Africa',
    'NAM': 'Sub-Saharan Africa', 'NER': 'Sub-Saharan Africa', 'NGA': 'Sub-Saharan Africa',
    'RWA': 'Sub-Saharan Africa', 'SDN': 'Sub-Saharan Africa', 'SEN': 'Sub-Saharan Africa',
    'SLE': 'Sub-Saharan Africa', 'SOM': 'Sub-Saharan Africa', 'SSD': 'Sub-Saharan Africa',
    'STP': 'Sub-Saharan Africa', 'SWZ': 'Sub-Saharan Africa', 'SYC': 'Sub-Saharan Africa',
    'TCD': 'Sub-Saharan Africa', 'TGO': 'Sub-Saharan Africa', 'TZA': 'Sub-Saharan Africa',
    'UGA': 'Sub-Saharan Africa', 'ZAF': 'Sub-Saharan Africa', 'ZMB': 'Sub-Saharan Africa',
    'ZWE': 'Sub-Saharan Africa',
}


@st.cache_data
def get_gdp_data():
    DATA_FILENAME = Path(__file__).parent / 'data/gdp_data.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 1960
    MAX_YEAR = 2022

    gdp_df = raw_gdp_df.melt(
        ['Country Name', 'Country Code'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'GDP',
    )
    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])
    gdp_df['Region'] = gdp_df['Country Code'].map(REGION_MAP).fillna('Aggregates/Other')
    return gdp_df


gdp_df = get_gdp_data()

# -----------------------------------------------------------------------------
# Page header

'''
# :earth_americas: GDP dashboard

Browse GDP data from the [World Bank Open Data](https://data.worldbank.org/) website. As you'll
notice, the data only goes to 2022 right now, and datapoints for certain years are often missing.
But it's otherwise a great (and did I mention _free_?) source of data.
'''

''
''

# -----------------------------------------------------------------------------
# Filters

min_value = gdp_df['Year'].min()
max_value = gdp_df['Year'].max()

from_year, to_year = st.slider(
    'Which years are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value],
)

all_regions = sorted(gdp_df['Region'].unique())
default_regions = [r for r in all_regions if r != 'Aggregates/Other']

selected_regions = st.multiselect(
    'Filter by region:',
    all_regions,
    default=default_regions,
)

region_filtered_df = gdp_df[gdp_df['Region'].isin(selected_regions)]
available_countries = sorted(region_filtered_df['Country Name'].unique())

default_names = ['Germany', 'France', 'United Kingdom', 'Brazil', 'Mexico', 'Japan']
default_selection = [c for c in default_names if c in available_countries]

selected_countries = st.multiselect(
    'Which countries would you like to view?',
    available_countries,
    default_selection,
)

if not selected_countries:
    st.warning("Select at least one country")
    st.stop()

unit_label = st.radio(
    'GDP unit:',
    ['Billion (B)', 'Trillion (T)', 'Million (M)'],
    horizontal=True,
)
UNIT_DIVISOR = {'Billion (B)': 1e9, 'Trillion (T)': 1e12, 'Million (M)': 1e6}
UNIT_SUFFIX = {'Billion (B)': 'B', 'Trillion (T)': 'T', 'Million (M)': 'M'}
divisor = UNIT_DIVISOR[unit_label]
suffix = UNIT_SUFFIX[unit_label]

''
''
''

# -----------------------------------------------------------------------------
# Filtered dataset

filtered_gdp_df = gdp_df[
    (gdp_df['Country Name'].isin(selected_countries))
    & (gdp_df['Year'] <= to_year)
    & (from_year <= gdp_df['Year'])
]

# -----------------------------------------------------------------------------
# Charts (tabbed)

tab1, tab2, tab3, tab4 = st.tabs(['GDP over time', 'YoY Growth (%)', 'GDP Ranking', 'Normalized Growth'])

with tab1:
    st.header('GDP over time', divider='gray')
    ''
    st.line_chart(filtered_gdp_df, x='Year', y='GDP', color='Country Name')

with tab2:
    st.header('Year-over-Year Growth Rate (%)', divider='gray')
    ''
    yoy_df = filtered_gdp_df.sort_values(['Country Name', 'Year']).copy()
    yoy_df['YoY Growth (%)'] = yoy_df.groupby('Country Name')['GDP'].pct_change() * 100
    yoy_df = yoy_df.dropna(subset=['YoY Growth (%)'])
    if not yoy_df.empty:
        st.line_chart(yoy_df, x='Year', y='YoY Growth (%)', color='Country Name')
    else:
        st.info("Not enough data to calculate growth rates.")

with tab3:
    st.header(f'GDP Ranking in {to_year}', divider='gray')
    ''
    rank_df = (
        gdp_df[
            (gdp_df['Country Name'].isin(selected_countries))
            & (gdp_df['Year'] == to_year)
        ]
        .dropna(subset=['GDP'])
        .sort_values('GDP', ascending=False)
    )
    rank_df[f'GDP ({suffix})'] = rank_df['GDP'] / divisor
    if not rank_df.empty:
        st.bar_chart(rank_df.set_index('Country Name')[[f'GDP ({suffix})']])
    else:
        st.info(f"No data available for {to_year}.")

with tab4:
    st.header(f'Normalized GDP Growth (Base: {from_year} = 100)', divider='gray')
    ''
    base_gdp = (
        gdp_df[
            (gdp_df['Country Name'].isin(selected_countries))
            & (gdp_df['Year'] == from_year)
        ][['Country Name', 'GDP']]
        .rename(columns={'GDP': 'Base GDP'})
    )
    norm_df = filtered_gdp_df.merge(base_gdp, on='Country Name')
    norm_df['Normalized GDP (Base=100)'] = norm_df['GDP'] / norm_df['Base GDP'] * 100
    norm_df = norm_df.dropna(subset=['Normalized GDP (Base=100)'])
    if not norm_df.empty:
        st.line_chart(norm_df, x='Year', y='Normalized GDP (Base=100)', color='Country Name')
    else:
        st.info(f"No base year data available for {from_year}.")

''
''

# -----------------------------------------------------------------------------
# Metric cards

first_year_data = gdp_df[gdp_df['Year'] == from_year]
last_year_data = gdp_df[gdp_df['Year'] == to_year]

st.header(f'GDP in {to_year}', divider='gray')
''

n_cols = min(4, len(selected_countries))
cols = st.columns(n_cols)

for i, country in enumerate(selected_countries):
    col = cols[i % n_cols]
    with col:
        first_row = first_year_data[first_year_data['Country Name'] == country]['GDP']
        last_row = last_year_data[last_year_data['Country Name'] == country]['GDP']

        first_val = first_row.iloc[0] if len(first_row) > 0 else float('nan')
        last_val = last_row.iloc[0] if len(last_row) > 0 else float('nan')

        first_gdp = float('nan') if pd.isna(first_val) else first_val / divisor
        last_gdp = float('nan') if pd.isna(last_val) else last_val / divisor

        if math.isnan(first_gdp) or math.isnan(last_gdp) or first_gdp == 0:
            growth = 'n/a'
            delta_color = 'off'
        else:
            growth = f'{last_gdp / first_gdp:,.2f}x'
            delta_color = 'normal'

        st.metric(
            label=f'{country} GDP',
            value=f'{last_gdp:,.2f}{suffix}' if not math.isnan(last_gdp) else 'N/A',
            delta=growth,
            delta_color=delta_color,
        )

''
''

# -----------------------------------------------------------------------------
# Download

st.header('Download Data', divider='gray')
''

csv_data = (
    filtered_gdp_df[['Country Name', 'Country Code', 'Region', 'Year', 'GDP']]
    .to_csv(index=False)
    .encode('utf-8')
)

st.download_button(
    label='Download filtered data as CSV',
    data=csv_data,
    file_name=f'gdp_data_{from_year}_{to_year}.csv',
    mime='text/csv',
)
