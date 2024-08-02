import pytest
import pandas as pd
from project import load_data, load_country_codes, calculate_growth_rate, get_energy_use_2022, compare_energy_use, calculate_weighted_growth_rate

# Sample data to be used for testing
sample_data = pd.DataFrame({
    'Country': ['Australia', 'USA', 'Canada'],
    '1990': [100, 200, 300],
    '2022': [150, 300, 450],
    'Population': [20, 300, 30],
    'Nationality': ['Australian', 'American', 'Canadian']
})

sample_codes = {
    'Australia': 'AU',
    'USA': 'US',
    'Canada': 'CA'
}

def test_load_data():
    # Assuming the CSV content is the sample_data
    data = load_data('path_to_your_sample_data.csv')
    assert not data.empty
    assert set(data.columns) == set(sample_data.columns)

def test_load_country_codes():
    # Assuming the CSV content is the sample_codes
    codes = load_country_codes('path_to_your_sample_codes.csv')
    assert codes == sample_codes

def test_calculate_growth_rate():
    growth_rate = calculate_growth_rate(sample_data, 'Australia')
    assert growth_rate == 50

def test_get_energy_use_2022():
    energy_use_2022 = get_energy_use_2022(sample_data, 'Australia')
    assert energy_use_2022 == 150

def test_compare_energy_use():
    comparison_sentence, flags_count, larger_flag_country, smaller_flag_country = compare_energy_use(sample_data, 'Australia', 'USA')
    assert comparison_sentence == "1 Australian consumes as much energy as 0.50 Americans!"
    assert flags_count == 2
    assert larger_flag_country == 'USA'
    assert smaller_flag_country == 'Australia'

def test_calculate_weighted_growth_rate():
    weighted_growth_rate = calculate_weighted_growth_rate(sample_data, 'Australia', 'Population')
    assert weighted_growth_rate == 50

if __name__ == "__main__":
    pytest.main()
