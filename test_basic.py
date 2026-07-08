"""Basic tests for Wenli Carbon Calculator"""

def calculate_carbon_electricity(kwh, om_factor=0.4044):
    """Calculate CO2 from electricity consumption"""
    return kwh * om_factor

def calculate_carbon_gas(m3, emission_factor=2.17):
    """Calculate CO2 from natural gas consumption"""
    return m3 * emission_factor

def test_electricity_calculation():
    """Test basic electricity carbon calculation"""
    assert abs(calculate_carbon_electricity(1000, 0.4044) - 404.4) < 1e-9

def test_om_factor():
    """Test Hubei OM factor is correctly applied"""
    assert abs(calculate_carbon_electricity(1, 0.4044) - 0.4044) < 1e-9

def test_gas_calculation():
    """Test basic gas carbon calculation"""
    assert calculate_carbon_gas(100) == 217.0

if __name__ == "__main__":
    test_electricity_calculation()
    test_om_factor()
    test_gas_calculation()
    print("All basic tests passed.")
