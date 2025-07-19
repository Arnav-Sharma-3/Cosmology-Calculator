import streamlit as st
from math import *

def run_cosmology_calculator(z, H0, WM, WV, verbose):
    h = H0 / 100.
    WR = 4.165E-5 / (h * h)
    WK = 1 - WM - WR - WV
    az = 1.0 / (1.0 + z)
    Tyr = 977.8
    c = 299792.458

    n = 1000
    age = 0.0
    for i in range(n):
        a = az * (i + 0.5) / n
        adot = sqrt(WK + (WM / a) + (WR / (a * a)) + (WV * a * a))
        age += 1.0 / adot
    zage = az * age / n
    zage_Gyr = (Tyr / H0) * zage

    DTT = 0.0
    DCMR = 0.0
    for i in range(n):
        a = az + (1 - az) * (i + 0.5) / n
        adot = sqrt(WK + (WM / a) + (WR / (a * a)) + (WV * a * a))
        DTT += 1.0 / adot
        DCMR += 1.0 / (a * adot)
    DTT = (1.0 - az) * DTT / n
    DCMR = (1.0 - az) * DCMR / n

    age = DTT + zage
    age_Gyr = age * (Tyr / H0)
    DTT_Gyr = (Tyr / H0) * DTT
    DCMR_Gyr = (Tyr / H0) * DCMR
    DCMR_Mpc = (c / H0) * DCMR

    # Angular diameter distance
    x = sqrt(abs(WK)) * DCMR
    if x > 0.1:
        if WK > 0:
            ratio = 0.5 * (exp(x) - exp(-x)) / x
        else:
            ratio = sin(x) / x
    else:
        y = x * x
        if WK < 0:
            y = -y
        ratio = 1. + y / 6. + y * y / 120.

    DCMT = ratio * DCMR
    DA = az * DCMT
    DA_Mpc = (c / H0) * DA
    DA_Gyr = (Tyr / H0) * DA
    kpc_DA = DA_Mpc / 206.264806
    DL = DA / (az * az)
    DL_Mpc = (c / H0) * DL
    DL_Gyr = (Tyr / H0) * DL
    distance_modulus = 5 * log10(DL_Mpc * 1e6) - 5

    return {
        'age_Gyr': age_Gyr,
        'zage_Gyr': zage_Gyr,
        'DTT_Gyr': DTT_Gyr,
        'DCMR_Mpc': DCMR_Mpc,
        'DCMR_Gyr': DCMR_Gyr,
        'DA_Mpc': DA_Mpc,
        'DA_Gyr': DA_Gyr,
        'kpc_DA': kpc_DA,
        'DL_Mpc': DL_Mpc,
        'DL_Gyr': DL_Gyr,
        'distance_modulus': distance_modulus
    }

# ---------------------------
# STREAMLIT APP INTERFACE
# ---------------------------

st.title("Cosmology Calculator 🌌")

z = st.slider("Redshift (z)", 0.01, 20.0, 3.0, step=0.01)
H0 = st.number_input("Hubble Constant (H₀)", value=70.0)
WM = st.slider("Ω Matter (Ωₘ)", 0.0, 1.5, 0.3)
WV = st.slider("Ω Vacuum / Lambda (Ω_Λ)", 0.0, 1.5, 0.7)
verbose = st.checkbox("Verbose Output", value=True)

if st.button("Calculate"):
    results = run_cosmology_calculator(z, H0, WM, WV, verbose)

    if verbose:
        st.markdown("### Results:")
        st.write(f"**Age of Universe now:** {results['age_Gyr']:.2f} Gyr")
        st.write(f"**Age at redshift z:** {results['zage_Gyr']:.2f} Gyr")
        st.write(f"**Light travel time:** {results['DTT_Gyr']:.2f} Gyr")
        st.write(f"**Comoving radial distance:** {results['DCMR_Mpc']:.2f} Mpc")
        st.write(f"**Angular diameter distance D_A:** {results['DA_Mpc']:.2f} Mpc ({results['DA_Gyr']:.2f} Gly)")
        st.write(f"**Scale:** {results['kpc_DA']:.2f} kpc/arcsec")
        st.write(f"**Luminosity distance D_L:** {results['DL_Mpc']:.2f} Mpc ({results['DL_Gyr']:.2f} Gly)")
        st.write(f"**Distance modulus (m - M):** {results['distance_modulus']:.2f}")
    else:
        st.write(f"{results['zage_Gyr']:.2f}, {results['DCMR_Mpc']:.2f}, {results['kpc_DA']:.2f}, {results['distance_modulus']:.2f}")
