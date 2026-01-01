import argparse
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT_DIR, "src")
sys.path.insert(0, SRC_DIR)

from config import Config
from display.display_manager import DisplayManager
from plugins.plugin_registry import load_plugins, get_plugin_instance


def parse_args():
    parser = argparse.ArgumentParser(description="Generate a weather image without running the server.")
    parser.add_argument("--units", choices=["imperial", "metric", "standard"], default="imperial")
    parser.add_argument("--weather-provider", choices=["OpenMeteo", "OpenWeatherMap"], default="OpenMeteo")
    parser.add_argument("--latitude", type=float)
    parser.add_argument("--longitude", type=float)
    parser.add_argument("--title-selection", choices=["location", "none", "custom"], default="location")
    parser.add_argument("--custom-title", default="")
    parser.add_argument("--forecast-days", type=int, choices=[3, 5, 7], default=5)
    parser.add_argument("--display-refresh-time", action="store_true", default=True)
    parser.add_argument("--no-display-refresh-time", dest="display_refresh_time", action="store_false")
    parser.add_argument("--display-forecast", action="store_true", default=True)
    parser.add_argument("--no-display-forecast", dest="display_forecast", action="store_false")
    parser.add_argument("--display-forecast-precip", action="store_true", default=False)
    parser.add_argument("--display-forecast-icons", action="store_true", default=True)
    parser.add_argument("--no-display-forecast-icons", dest="display_forecast_icons", action="store_false")
    parser.add_argument("--display-metric-icons", action="store_true", default=True)
    parser.add_argument("--no-display-metric-icons", dest="display_metric_icons", action="store_false")
    parser.add_argument("--display-metrics", action="store_true", default=True)
    parser.add_argument("--no-display-metrics", dest="display_metrics", action="store_false")
    parser.add_argument("--display-metric-sunrise", action="store_true", default=True)
    parser.add_argument("--no-display-metric-sunrise", dest="display_metric_sunrise", action="store_false")
    parser.add_argument("--display-metric-sunset", action="store_true", default=True)
    parser.add_argument("--no-display-metric-sunset", dest="display_metric_sunset", action="store_false")
    parser.add_argument("--display-metric-wind", action="store_true", default=True)
    parser.add_argument("--no-display-metric-wind", dest="display_metric_wind", action="store_false")
    parser.add_argument("--display-metric-humidity", action="store_true", default=True)
    parser.add_argument("--no-display-metric-humidity", dest="display_metric_humidity", action="store_false")
    parser.add_argument("--display-metric-pressure", action="store_true", default=True)
    parser.add_argument("--no-display-metric-pressure", dest="display_metric_pressure", action="store_false")
    parser.add_argument("--display-metric-uv-index", action="store_true", default=True)
    parser.add_argument("--no-display-metric-uv-index", dest="display_metric_uv_index", action="store_false")
    parser.add_argument("--display-metric-visibility", action="store_true", default=True)
    parser.add_argument("--no-display-metric-visibility", dest="display_metric_visibility", action="store_false")
    parser.add_argument("--display-metric-air-quality", action="store_true", default=True)
    parser.add_argument("--no-display-metric-air-quality", dest="display_metric_air_quality", action="store_false")
    parser.add_argument("--display-graph", action="store_true", default=True)
    parser.add_argument("--no-display-graph", dest="display_graph", action="store_false")
    parser.add_argument("--display-rain", action="store_true", default=False)
    parser.add_argument("--moon-phase", action="store_true", default=False)
    parser.add_argument("--weather-time-zone", choices=["locationTimeZone", "localTimeZone"], default="locationTimeZone")
    parser.add_argument("--use-24h-time", action="store_true", default=False)
    return parser.parse_args()


def build_settings(args):
    settings = {
        "units": args.units,
        "weatherProvider": args.weather_provider,
        "titleSelection": args.title_selection,
        "customTitle": args.custom_title,
        "displayRefreshTime": "true" if args.display_refresh_time else "false",
        "displayForecast": "true" if args.display_forecast else "false",
        "forecastDays": args.forecast_days,
        "displayForecastPrecip": "true" if args.display_forecast_precip else "false",
        "displayForecastIcons": "true" if args.display_forecast_icons else "false",
        "displayMetricIcons": "true" if args.display_metric_icons else "false",
        "displayMetrics": "true" if args.display_metrics else "false",
        "displayMetricSunrise": "true" if args.display_metric_sunrise else "false",
        "displayMetricSunset": "true" if args.display_metric_sunset else "false",
        "displayMetricWind": "true" if args.display_metric_wind else "false",
        "displayMetricHumidity": "true" if args.display_metric_humidity else "false",
        "displayMetricPressure": "true" if args.display_metric_pressure else "false",
        "displayMetricUvIndex": "true" if args.display_metric_uv_index else "false",
        "displayMetricVisibility": "true" if args.display_metric_visibility else "false",
        "displayMetricAirQuality": "true" if args.display_metric_air_quality else "false",
        "displayGraph": "true" if args.display_graph else "false",
        "displayRain": "true" if args.display_rain else "false",
        "moonPhase": "true" if args.moon_phase else "false",
        "weatherTimeZone": args.weather_time_zone,
        "use24hTime": "true" if args.use_24h_time else "false"
    }
    if args.latitude is not None:
        settings["latitude"] = args.latitude
    if args.longitude is not None:
        settings["longitude"] = args.longitude
    return settings


def main():
    args = parse_args()
    Config.config_file = os.path.join(Config.BASE_DIR, "config", "device_dev.json")
    device_config = Config()
    display_manager = DisplayManager(device_config)
    load_plugins(device_config.get_plugins())

    plugin_config = device_config.get_plugin("weather")
    plugin = get_plugin_instance(plugin_config)

    settings = build_settings(args)

    image = plugin.generate_image(settings, device_config)
    display_manager.display_image(image, image_settings=plugin_config.get("image_settings", []))
    print("Wrote mock_display_output/latest.png")


if __name__ == "__main__":
    main()
