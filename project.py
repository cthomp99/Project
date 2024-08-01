import pandas as pd
import streamlit as st

def load_data(file_url=None):
    """
    Load data from a CSV file.
    """
    try:
        data = pd.read_csv(file_url)
    except FileNotFoundError:
        st.error(f"The file {file_url} was not found.")
        data = None
    return data

def load_country_codes(file_url):
    """
    Load country codes from a CSV file.
    """
    try:
        codes = pd.read_csv(file_url)
        codes.columns = codes.columns.str.strip()  # Remove any extra spaces from column names
        code_dict = dict(zip(codes['Country'].str.strip(), codes['Code'].str.strip()))
    except FileNotFoundError:
        st.error(f"The file {file_url} was not found.")
        code_dict = {}
    except KeyError as e:
        st.error(f"Key error: {e}. Available columns: {codes.columns.tolist()}")
        code_dict = {}
    return code_dict

def calculate_growth_rate(data, country):
    """
    Calculate the total growth rate in energy use per capita from 1990 to 2022 for a specific country.
    """
    country_data = data[data['Country'] == country]
    growth_rate = ((country_data['2022'].values[0] - country_data['1990'].values[0]) / country_data['1990'].values[0]) * 100
    return round(growth_rate)

def get_energy_use_2022(data, country):
    """
    Get the energy use per capita for 2022 for a specific country.
    """
    country_data = data[data['Country'] == country]
    energy_use_2022 = country_data['2022'].values[0]
    return energy_use_2022

def compare_energy_use(data, country1, country2):
    """
    Compare energy use per capita between two countries in 2022.
    Returns a string describing the comparison and the ratio of flags.
    """
    energy_use_2022_country1 = get_energy_use_2022(data, country1)
    energy_use_2022_country2 = get_energy_use_2022(data, country2)
    nationality1 = data[data['Country'] == country1]['Nationality'].values[0]
    nationality2 = data[data['Country'] == country2]['Nationality'].values[0]
    comparison = energy_use_2022_country1 / energy_use_2022_country2
    
    if comparison >= 1:
        comparison_sentence = f"1 {nationality1} consumes as much energy as {comparison:.2f} {nationality2}s!"
        larger_flag_country = country1
        smaller_flag_country = country2
        flags_count = round(comparison)
    else:
        inverse_comparison = 1 / comparison
        comparison_sentence = f"1 {nationality2} consumes as much energy as {inverse_comparison:.2f} {nationality1}s"
        larger_flag_country = country2
        smaller_flag_country = country1
        flags_count = round(inverse_comparison)
        
    return comparison_sentence, flags_count, larger_flag_country, smaller_flag_country

def main():
    st.title("Global Energy Use per Capita")
    st.write("Compare the energy use per capita between two countries.")
    
    # Load the data
    data_url = 'https://raw.githubusercontent.com/cthomp99/Project/main/country_tracker.csv'
    data = load_data(data_url)
    
    # Load the country codes
    codes_url = 'https://raw.githubusercontent.com/cthomp99/Project/main/country_codes.csv'
    country_to_code = load_country_codes(codes_url)

    if data is not None and country_to_code:
        # Get list of countries
        countries = data['Country'].unique()

        # Create dropdown menus for country selection, defaulting to Australia for the first country
        country1 = st.selectbox("Select the first country:", countries, index=list(countries).index('Australia'))
        country2 = st.selectbox("Select the second country:", countries)

        # Display energy use for 2022, growth rates, and flags after both countries are selected
        if country1 and country2:
            comparison_sentence, flags_count, larger_flag_country, smaller_flag_country = compare_energy_use(data, country1, country2)
            
            flag_width = 200  # Standard width for a single flag
            smaller_flag_width = flag_width // flags_count
            
            col1, col2 = st.columns(2)

            for col, country, is_larger in [(col1, country1, larger_flag_country == country1), (col2, country2, larger_flag_country == country2)]:
                with col:
                    st.markdown(f"### {country}", unsafe_allow_html=True)
                    energy_use = get_energy_use_2022(data, country)
                    st.markdown(f"**Energy Use in 2022: {energy_use} Gj per capita**", unsafe_allow_html=True)
                    growth_rate = calculate_growth_rate(data, country)
                    st.markdown(f"**Growth Rate: {growth_rate}%**", unsafe_allow_html=True)
                    # Display flag with custom size
                    flag_code = country_to_code.get(country, '').lower()
                    if flag_code:
                        if is_larger:
                            st.markdown(f'<img src="https://flagcdn.com/w320/{flag_code}.png" style="width:{flag_width}px;">', unsafe_allow_html=True)
                        else:
                            flags_html = ''.join([f'<img src="https://flagcdn.com/w320/{flag_code}.png" style="width:{smaller_flag_width}px; margin-right: 5px; margin-bottom: 5px;">' for _ in range(flags_count)])
                            st.markdown(flags_html, unsafe_allow_html=True)
                    else:
                        st.write("Flag not found.")

            # Display comparative energy use sentence
            st.markdown(f"<div class='centered-text'><h2>{comparison_sentence}</h2></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
