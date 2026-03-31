import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

def validate_inputs(inputs):
    """Validate deal inputs"""
    errors = []
    
    if inputs.get('coupon_rate', 0) <= 0:
        errors.append("Coupon rate must be positive")
    if inputs.get('autocall_trigger', 0) < inputs.get('coupon_barrier', 0):
        errors.append("Autocall trigger must be >= coupon barrier")
    if inputs.get('final_barrier', 0) >= 1.0:
        errors.append("Final barrier should be < 100%")
    if inputs.get('tenor', 0) <= 0:
        errors.append("Tenor must be positive")
    
    return errors

def generate_observation_dates(tenor_years, frequency, start_date=None):
    """Generate observation dates based on frequency"""
    if start_date is None:
        start_date = datetime(2026, 1, 1)
    
    dates = []
    current = start_date
    periods = int(tenor_years * 12 / frequency)
    
    for i in range(periods):
        dates.append(current)
        current += timedelta(days=30*frequency)
    
    return dates

def calculate_single_path(inputs, final_spot_pct):
    """Calculate payoff for single final spot scenario"""
    spot0 = inputs['initial_spot']
    notional = inputs['notional']
    coupon_rate = inputs['coupon_rate']
    coupon_freq = inputs['coupon_frequency']
    autocall_trigger = inputs['autocall_trigger']
    coupon_barrier = inputs['coupon_barrier']
    final_barrier = inputs['final_barrier']
    tenor = inputs['tenor']
    memory_coupon = inputs.get('memory_coupon', False)
    call_protection = inputs.get('call_protection_period', 0)
    
    # Generate observation dates
    dates = generate_observation_dates(tenor, coupon_freq)
    n_obs = len(dates)
    
    # Assume linear path to final spot for simplicity
    final_spot = spot0 * final_spot_pct
    path = np.linspace(1.0, final_spot_pct, n_obs)
    
    total_coupons = 0
    missed_coupons = 0
    autocall_date = None
    
    # Check each observation
    for i, obs_level in enumerate(path):
        obs_spot = spot0 * obs_level
        coupon_amount = notional * coupon_rate * (coupon_freq / 12)
        
        # Autocall check (skip protection period)
        if i >= call_protection and obs_level >= autocall_trigger:
            autocall_date = dates[i]
            total_coupons += coupon_amount * (i + 1)  # All accumulated coupons
            return {
                'autocall': True,
                'autocall_date': autocall_date,
                'total_coupons': total_coupons,
                'final_redemption': notional,
                'total_payoff': notional + total_coupons
            }
        
        # Coupon barrier check
        if obs_level >= coupon_barrier:
            total_coupons += coupon_amount
        else:
            if memory_coupon:
                missed_coupons += coupon_amount
    
    # Maturity payoff
    if final_spot_pct >= final_barrier:
        final_redemption = notional
    else:
        # Downside participation
        downside = (final_barrier - final_spot_pct) / final_barrier
        final_redemption = notional * (1 - downside * inputs['downside_participation'])
    
    # Add memory coupons if applicable
    if memory_coupon and final_spot_pct >= coupon_barrier:
        total_coupons += missed_coupons
    
    total_payoff = final_redemption + total_coupons
    
    return {
        'autocall': False,
        'autocall_date': None,
        'total_coupons': total_coupons,
        'final_redemption': final_redemption,
        'total_payoff': total_payoff
    }

def calculate_payoff_scenarios(inputs):
    """Calculate scenarios across final spot range"""
    if st.session_state.validation_errors:
        return None
    
    # Generate scenarios from 0% to 150%
    final_spots = np.linspace(0.0, 1.5, 101)
    
    results = []
    for spot_pct in final_spots:
        result = calculate_single_path(inputs, spot_pct)
        result['final_spot_pct'] = spot_pct
        results.append(result)
    
    df = pd.DataFrame(results)
    df['return_pct'] = (df['total_payoff'] / inputs['notional'] - 1) * 100
    st.session_state.scenarios = df
    return df
