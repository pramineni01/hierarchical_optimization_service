from datetime import time, datetime, timedelta
import logging

from tariff_convert.tariff_structs import(
    TariffPeriodTypes,
    Period,
    DatePeriod,
    Holidays,
    PeriodEnergyCharge,
    PeriodDemandCharge,
    VoltageDiscount,
    PeriodCharge,
    ChargeRate,
    TariffPeriod,
)

from economics_pb2 import(
    InputPrice,
    InputPriceGroup,
    InputEconomics,
) 

from utils_pb2 import(
    IntervalDataFormat1,
    UnitType
)

# from google.protobuf.timestamp_pb2 import Timestamp
# import google.protobuf.timestamp_pb2.TimeStamp as TimeStamp_pb2

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

def set_period_types():

    summer_peak_periods = [
        Period(
            start= time(hour=12, minute=0),
            end= time(hour=18, minute=0),
        ),
    ]
    summer_midpeak_periods = [
        Period(
            start= time(hour=8, minute=0),
            end= time(hour=12, minute=0),
        ),
        Period(
            start= time(hour=18, minute=0),
            end= time(hour=23, minute=0),
        ),
        
    ]
    summer_offpeak_periods = [
        Period(
            start= time(hour=0, minute=0),
            end= time(hour=8, minute=0),
        ),
        Period(
            start= time(hour=23, minute=0),
            end= time(hour=0, minute=0),
        ),

    ]
    winter_midpeak_periods = [
        Period(
            start= time(hour=8, minute=0),
            end= time(hour=21, minute=0),
        ),
    ]
    winter_offpeak_periods = [
        Period(
            start= time(hour=0, minute=0),
            end= time(hour=8, minute=0),
        ),
        Period(
            start= time(hour=21, minute=0),
            end= time(hour=0, minute=0),
        ),
    ]
    summer_season = DatePeriod(
        start = datetime(year=2021, month=6, day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=None),
        end = datetime(year=2021, month=10, day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)

    )
    
    sce_perioed_types = TariffPeriodTypes(
        summer_peak_periods=summer_peak_periods,
        summer_midpeak_periods=summer_midpeak_periods,
        summer_offpeak_periods= summer_offpeak_periods,
        winter_peak_periods=[],
        winter_midpeak_periods=winter_midpeak_periods,
        winter_offpeak_periods=winter_offpeak_periods,
        summer_season=summer_season,
        include_weekend = False,
        inlcude_holidays = False,
        holidays = Holidays(country = 'US', year=2021),
    )

    return sce_perioed_types


def set_charge_rates():

    sce_energy_charge_rates_summer = PeriodEnergyCharge(
        summer_season = True,
        peak = ChargeRate(value=0.07771, unit= UnitType.DOLLAR_PER_MWH),
        midpeak = ChargeRate(value=0.07771, unit= UnitType.DOLLAR_PER_MWH),
        offpeak = ChargeRate(value=0.07771, unit= UnitType.DOLLAR_PER_MWH),
    )

    sce_energy_charge_rates_winter = PeriodEnergyCharge(
        summer_season = False,
        peak = ChargeRate(value=0.05482, unit= UnitType.DOLLAR_PER_MWH),
        midpeak = ChargeRate(value=0.05482, unit= UnitType.DOLLAR_PER_MWH),
        offpeak = ChargeRate(value=0.05482, unit= UnitType.DOLLAR_PER_MWH),
    )

    sce_demand_charge_rates_summer = PeriodDemandCharge(
        summer_season = True,
        facility_charge = ChargeRate(value=16.0, unit= UnitType.DOLLAR_PER_MW),
    )
    sce_demand_charge_rates_winter = PeriodDemandCharge(
        summer_season = False,
        facility_charge = ChargeRate(value=13.55, unit= UnitType.DOLLAR_PER_MW),
    )

    sce_charge_rates = PeriodCharge(
        demand_charges=[
            sce_demand_charge_rates_summer,
            sce_demand_charge_rates_winter,
        ],
        energy_charges=[
            sce_energy_charge_rates_summer,
            sce_energy_charge_rates_winter
        ]
    )

    return sce_charge_rates


def set_basic_periods(
    period: DatePeriod,
    resolution:timedelta = timedelta(hours=1),
):

    interval_list = list()
    current_interval = period.start
    while current_interval < period.end:
        interval_list.append(current_interval)
        current_interval = current_interval + resolution

    sce_tariff_periods = list()
    for item in interval_list:
        sce_tariff_periods.append(
            TariffPeriod(
                interval_beginning = item,
                interval_ending= item+resolution,
            )
        )
    return sce_tariff_periods


def set_volumetric_price_proto(tariff_period_list):
    volumetric_price = InputPrice()

    volumetric_price.key = "10"
    volumetric_price.name = "sce_gs2_energy_charge"
    volumetric_price.type =  InputPrice.PriceType.PRICE_TYPE_ENERGY
    # volumetric_price.properties_price_energy.venue_key = "Venue/10"

    volumetric_price.properties_price_energy.price_values.interval_values_fmt_1.unit = \
        tariff_period_list[0].energy_charge_unit
    
    for tariff_period in tariff_period_list:
        price_interval = IntervalDataFormat1()
        price_interval.value = tariff_period.energy_charge_rate

        price_interval.interval_start_time.FromDatetime(
            dt = tariff_period.interval_beginning
        )   
        price_interval.interval_end_time.FromDatetime(
            dt = tariff_period.interval_ending
        )
        volumetric_price.properties_price_energy.price_values.interval_values_fmt_1.values.append(
            price_interval
        )

    return volumetric_price


def set_peak_demand_price_proto(tariff_period_list):
    peak_demand_price = InputPrice()
    peak_demand_price.key = "20"
    peak_demand_price.name = "sce_gs2_demand_charge"
    peak_demand_price.type =  InputPrice.PriceType.PRICE_TYPE_PEAK

    peak_demand_price.properties_price_peak.price_values.constant_value_over_horizon.unit = \
        tariff_period_list[0].demand_charge_unit

    peak_demand_price.properties_price_peak.price_values.constant_value_over_horizon.value = \
        tariff_period_list[0].demand_charge_rate
    
    # for tariff_period in tariff_period_list:
    #     price_interval = IntervalDataFormat1()
    #     price_interval.value = tariff_period.demand_charge_rate

    #     price_interval.interval_start_time.FromDatetime(
    #         dt = tariff_period.interval_beginning
    #     )   
    #     price_interval.interval_end_time.FromDatetime(
    #         dt = tariff_period.interval_ending
    #     )
    #     peak_demand_price.properties_price_energy.price_values.interval_values_fmt_1.values.append(
    #         price_interval
    #     )

    return peak_demand_price


def set_tariff_price_groups():

    retail_tariff_structure = InputPriceGroup()

    retail_tariff_structure.key = "10"
    retail_tariff_structure.name = "sce_gs2_retail_tariff_structure"
    retail_tariff_structure.type = InputPriceGroup.PriceGroupType.PRICEGROUP_TYPE_BTM_TARIFF

    retail_tariff_structure.price_keys.append("Price/10")
    retail_tariff_structure.price_keys.append("Price/20")

    # ToDo: we won't use this for now, in the general case instead of price_values 
    # we could go for using the geneability tarif inputs and use this option as well.
    # retail_tariff_structure.properties_btm_tariff 

    return retail_tariff_structure

def set_tariff_charges_in_proto(tariff_period_list):
    economics_proto = InputEconomics()
    volumetric_price_proto = set_volumetric_price_proto(tariff_period_list)
    peak_demand_price_proto = set_peak_demand_price_proto(tariff_period_list)
    tariff_price_group_proto = set_tariff_price_groups()
    economics_proto.prices.append(volumetric_price_proto)
    economics_proto.prices.append(peak_demand_price_proto)
    economics_proto.price_groups.append(tariff_price_group_proto)
    return economics_proto

def get_economics_proto_for_simulation_period(
    simulation_start_dt = datetime(2021, 7, 1, hour=0, minute=0, second=0, microsecond=0, tzinfo=None),
    simulation_end_dt =  datetime(2021, 8, 1, hour=0, minute=0, second=0, microsecond=0, tzinfo=None),
):

    sce_period_types = set_period_types()
    sce_charge_rates = set_charge_rates()
    sce_basic_tariff_periods = set_basic_periods(
        period= DatePeriod(
            start = simulation_start_dt,
            end = simulation_end_dt
        ),
        resolution = timedelta(hours=1),
    )

    for tariff_period in sce_basic_tariff_periods:
        tariff_period.set_tariff_period_types(sce_period_types)
        tariff_period.set_tariff_period_charges(sce_charge_rates)
    
    economics_proto = set_tariff_charges_in_proto(sce_basic_tariff_periods)
    return economics_proto
    
def main():
    economics_proto = get_economics_proto_for_simulation_period(
        simulation_start_dt = datetime(2021, 7, 1, hour=0, minute=0, second=0, microsecond=0, tzinfo=None),
        simulation_end_dt =  datetime(2021, 8, 1, hour=0, minute=0, second=0, microsecond=0, tzinfo=None),
    )

  
if __name__ == "__main__":
    main()


    logging.info("tarrif period conversion complete")

