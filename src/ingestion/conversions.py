import numpy as np
import math


def kelvin_to_celcius(k: float) -> float:
    """
    Convert Kelvin to Celcius

    Parameters:
        k: Temperature in Kelvin
    Returns:
        Temperature in Celcius
    See also:
        https://en.wikipedia.org/wiki/Kelvin
    """
    return k - 273.15


def meters_to_mm(m: float) -> float:
    """
    Convert meters to mm

    Parameters:
        m: Meter
    Returns:
        millimeter
    """
    return m * 1000


def daily_gdd(t2m_max: float, t2m_min: float, t2m_base: float = 10) -> float:
    """
    Calculate the Growing degree days (GDD)

    Parameters:
        t2m_max: maximum air temperature in Celcius
        t2m_min: maximum air temperature in Celcius
        t2m_base: plant dependent baseline temperature.
    Returns:
        GDD
    See also:
        https://en.wikipedia.org/wiki/Growing_degree-day
    """
    return (t2m_max + t2m_min) / 2 - t2m_base


def actual_vapour_pressure(tdc: float) -> float:
    """
    Compute the actual vapour pressure (AVP)

    Parameters:
        tc: Dewpoint temperature in Celcius
    Returns:
        actual vapour pressure
    See also:
        https://glossary.ametsoc.org/wiki/Tetens%27s_formula
    """
    return 0.61078 * np.exp((17.2694 * tdc) / (237.7 + tdc))


def saturated_vapour_pressure(tc: float) -> float:
    """
    Compute the actual vapour pressure (AVP)

    Parameters:
        tc: Air temperature in Celcius
    Returns:
        saturated vapour pressure
    See also:
        https://glossary.ametsoc.org/wiki/Tetens%27s_formula
    """
    return 0.61078 * np.exp((17.2694 * tc) / (237.7 + tc))


def relative_humidity(avp: float, svp: float) -> float:
    """
    Compute the relative humidity (RH)

    Parameters:
        avp: Actual vapour pressure
        svp: Saturated vapour pressure
    Returns:
        relative humidity as a percentage
    See also:
        http://ww2010.atmos.uiuc.edu/(Gh)/guides/mtr/cld/dvlp/rh.rxml
    """
    return (avp / svp) * 100


def wind_speed_from_u_v(u: float, v: float) -> float:
    """
    Compute wind speed from u- and v- wind components

    Parameters:
        u: u-component of wind
        v: v-component of wind
    Returns:
        wind speed
    See also:
        https://confluence.ecmwf.int/pages/viewpage.action?pageId=133262398
        https://www.researchgate.net/figure/BEAUFORT-SCALE-AND-ITS-DETAILS_tbl2_329584182
    """
    return np.sqrt(u**2 + v**2)


def wind_speed_10m_2m(ws: float) -> float:
    """
    Convert 10m wind speed to 2m wind speed by estimation

    Parameters:
        ws: wind speed at 10 meter
    Returns:
        wind speed
    See also:
        https://www.nature.com/articles/s41597-021-01003-9
    """
    return ws * (4.87 / (np.log(67.8 * 10 - 5.42)))


def net_radation(rs: float, rt: float):
    """
    Compute net radiation

    Parameters:
        rs: net solar radiation
        rt: net thermal radiation
    Returns:
        net radiation
    See also:
        https://www.nature.com/articles/s41597-021-01003-9
    """
    return rs + rt


def calculate_pet(
    surface_pressure_KPa,  # surface pressure KPa
    temperature2m_C,  # Daily mean temperature at 2 m
    dewpoint2m_C,  # Daily mean dewpoint temperature at 2 m
    windspeed2m_m_s,  # Windspeed at 2 m
    net_radiation_MJ_m2,  # Total daily net downward radiation MJ/m2/day
    soil_hf,  # factor used to get the soil heat flux
    pet_time,
):  # 'daily' or 'hourly'  ETo value
    """
    Compute PET using the fao56 penman monteith equation.
    This function is copied from the research paper from nature!

    Parameters:
        surface_pressure_KPa: surface pressure KPa
        temperature2m_C: daily mean temperature at 2 m
        dewpoint2m_C: daily mean dewpoint temperature at 2 m
        windspeed2m_m_s: windspeed at 2 m
        net_radiation_MJ_m2: total daily net downward radiation MJ/m2/day
        soil_hf: factor used to get the soil heat flux
        pet_time: 'daily' or 'hourly'  ETo value
    Returns:
        PET
    See also:
        https://www.nature.com/articles/s41597-021-01003-9]
        https://github.com/Dagmawi-TA/hPET/branches
        https://www.fao.org/3/x0490e/x0490e06.htm
    """
    # Constants.
    lmbda = 2.45  # Latent heat of vaporization [MJ kg -1] (simplification in the FAO PenMon (latent heat of about 20°C)
    cp = 1.013e-3  # Specific heat at constant pressure [MJ kg-1 °C-1]
    eps = 0.622  # Ratio molecular weight of water vapour/dry air

    # Soil heat flux density [MJ m-2 day-1] - set to 0 following eq 42 in FAO
    G = soil_hf

    # Atmospheric pressure [kPa] eq 7 in FAO.
    P_kPa = surface_pressure_KPa  # 101.3*((293.0-0.0065*height_m) / 293.0)**5.26

    # Psychrometric constant (gamma symbol in FAO) eq 8 in FAO.
    psychometric_kPa_c = cp * P_kPa / (eps * lmbda)

    # Saturation vapour pressure, eq 11 in FAO.
    svp_kPa = 0.6108 * np.exp((17.27 * temperature2m_C) / (temperature2m_C + 237.3))

    # Delta (slope of saturation vapour pressure curve) eq 13 in FAO.
    delta_kPa_C = 4098.0 * svp_kPa / (temperature2m_C + 237.3) ** 2

    # Actual vapour pressure, eq 14 in FAO.
    avp_kPa = 0.6108 * np.exp((17.27 * dewpoint2m_C) / (dewpoint2m_C + 237.3))

    # Saturation vapour pressure deficit.
    svpdeficit_kPa = svp_kPa - avp_kPa

    if pet_time == "daily":
        # Calculate ET0, equation 6 in FAO
        numerator = (
            0.408 * delta_kPa_C * (net_radiation_MJ_m2 - G)
            + psychometric_kPa_c
            * (900 / (temperature2m_C + 273))
            * windspeed2m_m_s
            * svpdeficit_kPa
        )
        denominator = delta_kPa_C + psychometric_kPa_c * (1 + 0.34 * windspeed2m_m_s)

        ET0_mm_day = numerator / denominator
        return ET0_mm_day

    elif pet_time == "hourly":
        # Calculate ET0, equation 53 in FAO
        numerator = (
            0.408 * delta_kPa_C * (net_radiation_MJ_m2 - G)
            + psychometric_kPa_c
            * (37 / (temperature2m_C + 273))
            * windspeed2m_m_s
            * svpdeficit_kPa
        )
        denominator = delta_kPa_C + psychometric_kPa_c * (1 + 0.34 * windspeed2m_m_s)

        ET0_mm_hr = numerator / denominator
        return ET0_mm_hr

    else:
        raise ValueError("time only takes 'daily' or 'hourly'")
