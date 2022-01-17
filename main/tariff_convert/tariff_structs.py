from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional

from datetime import datetime, time
import holidays



class Holidays:

    def __init__(
        self,
        country: Optional[str] = None,
        state: Optional[str] = None,
        year: Optional[int] = None,
        dates: Optional[List[datetime]] = None,
    ):

        self.country = country
        self.state = state
        self.year = year
        self.dates = dates

        if not self.dates:
            if not(self.country) or not(self.year):
                ValueError(" at least one of the  dates or the country/year for holidays must be specified")

            self._holidays = holidays.CountryHoliday(country, state=state, years= year)

    
    def get_dates(self):
        self.dates = list(self._holidays.keys())
        return
  

    def is_holiday(self,date: datetime):
        return date in self._holidays

@dataclass
class Period:
    start: time
    end: time

@dataclass
class DatePeriod:
    start: datetime
    end: datetime


@dataclass
class ChargeRate:
    unit: str
    value: float


@dataclass
class VoltageDiscount:
    voltage_discount_2k_to_50k: Optional[ChargeRate] = None
    voltage_discount_50k_to_220k: Optional[ChargeRate] = None
    voltage_discount_220k: Optional[ChargeRate] = None


@dataclass
class PeriodEnergyCharge:
    summer_season: Optional[bool] = False
    peak: Optional[ChargeRate] = None
    midpeak: Optional[ChargeRate] = None
    offpeak: Optional[ChargeRate] = None
    voltage_dsicount: Optional[VoltageDiscount] = None

    def get_period_energy_charges(self, tariff_period):

        #toDo: For now, I will not get into applying the voltage discounts, 
        # probably will need to revise the way we define those objects too

        if self.summer_season == tariff_period.summer_season:

            if tariff_period.peak_period:
                return (self.peak.value, self.peak.unit)
            elif tariff_period.midpeak_period:
                return (self.midpeak.value, self.midpeak.unit)
            else:
                return (self.offpeak.value, self.offpeak.unit)

        else: 
            return (0, self.peak.unit)


@dataclass
class PeriodDemandCharge:
    summer_season: Optional[bool] = False
    facility_charge: Optional[ChargeRate] = None
    voltage_dsicount: Optional[VoltageDiscount] = None


    def get_period_demand_charges(self, tariff_period):

        #toDo: For now, I will not get into applying the voltage discounts, 
        # probably will need to revise the way we define those objects too

        if self.summer_season == tariff_period.summer_season:
            return (self.facility_charge.value, self.facility_charge.unit)
        else: 
            return (0, self.facility_charge.unit)

                   
@dataclass
class PeriodCharge:

    demand_charges: Optional[List[PeriodDemandCharge]] = None
    energy_charges: Optional[List[PeriodEnergyCharge]] = None


    def get_period_charges(self, tariff_period):

        period_demand_charge_list =list ()
        period_energy_charge_list =list ()

        for demand_charge in self.demand_charges:
            period_demand_charge_list.append(
                demand_charge.get_period_demand_charges(tariff_period)
            )
        
        for energy_charge in self.energy_charges:
            period_energy_charge_list.append(
                energy_charge.get_period_energy_charges(tariff_period)
            )
        
        def accumulate_charges(charge_list):
            net_period_charges = None
            net_period_charges_unit = None
            for charge, charge_unit in charge_list:
                if not net_period_charges:
                    net_period_charges = charge
                    net_period_charges_unit = charge_unit
                else:
                    assert(net_period_charges_unit == charge_unit)
                    net_period_charges += charge
            return net_period_charges, net_period_charges_unit
        
        net_period_demand_charges,net_period_demand_charges_unit  = accumulate_charges(period_demand_charge_list)
        net_period_energy_charges, net_period_energy_charges_unit = accumulate_charges(period_energy_charge_list)

        return(
            net_period_demand_charges,
            net_period_demand_charges_unit,
            net_period_energy_charges, 
            net_period_energy_charges_unit,
        )


@dataclass
class TariffPeriodTypes:
    summer_peak_periods: List[Period]
    summer_midpeak_periods: List[Period]
    summer_offpeak_periods: List[Period]
    winter_peak_periods: List[Period]
    winter_midpeak_periods: List[Period]
    winter_offpeak_periods: List[Period]
    summer_season: DatePeriod
    include_weekend: Optional[bool] = False
    inlcude_holidays: Optional[bool] = False
    holidays: Holidays = None

    def is_holiday(self, period):
        return self.holidays.is_holiday(period.interval_ending)

    def is_weekend(self, period ):
        # Monday weekday being 0
        return period.interval_ending.weekday() > 4
    
    def is_summer_season(self, period ):
        assert(period.interval_ending.year == self.summer_season.start.year)
        return(
            (period.interval_ending > self.summer_season.start) and (period.interval_ending < self.summer_season.end)
        )

    def is_peak(self, period):

        if self.is_summer_season(period):
            peak_periods = self.summer_peak_periods
        else:
            peak_periods= self.winter_peak_periods
        
        for peak_period in peak_periods:
            if (
                (period.interval_ending.time() < peak_period.end) and 
                (period.interval_beginning.time() > peak_period.start)
                ) and not(self.is_holiday(period)) and not(self.is_weekend(period)):
                return True
                
        return False

    def is_midpeak(self, period):

        if self.is_summer_season(period):
            midpeak_periods = self.summer_midpeak_periods
        else:
            midpeak_periods= self.winter_midpeak_periods
        
        for midpeak_period in midpeak_periods:
            if (
                (period.interval_ending.time() < midpeak_period.end) and 
                (period.interval_beginning.time() > midpeak_period.start)
                ) and not(self.is_holiday(period)) and not(self.is_weekend(period)):
                return True     
        return False
        

                


        pass


@dataclass
class TariffPeriod:
    interval_ending: datetime
    interval_beginning: datetime
    summer_season: Optional[bool] = None
    peak_period: Optional[bool] = None
    midpeak_period: Optional[bool] = None
    weakend : Optional[bool] = None
    holiday: Optional[bool] = None
    demand_charge_rate: Optional[float] = None
    demand_charge_unit: Optional[str] = None
    energy_charge_rate: Optional[float] = None
    energy_charge_unit: Optional[str] = None


    def set_tariff_period_types(self, tariff_period_type: TariffPeriodTypes):
        self.summer_season = tariff_period_type.is_summer_season(self)
        self.peak_period = tariff_period_type.is_peak(self)
        self.midpeak_period = tariff_period_type.is_midpeak(self)
        self.holiday = tariff_period_type.is_holiday(self)
        return
    
    def set_tariff_period_charges(self, tariff_period_charges: PeriodCharge):

        (
            self.demand_charge_rate, 
            self.demand_charge_unit,
            self.energy_charge_rate,
            self.energy_charge_unit,
        ) = tariff_period_charges.get_period_charges(self)
