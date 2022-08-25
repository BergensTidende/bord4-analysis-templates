import requests
import shapely.wkt
import shapely.geometry
import xmltodict
from functools import partial
import pyproj
from shapely.ops import transform, linemerge


def format_vegref(roadref):
    roadref = "".join(roadref.split(" ")).upper()
    road_index = roadref.index("V") - 1
    hp_index = roadref.index("HP")
    meter_index = roadref.index("M")
    fylke = roadref[0:4]
    road_type = roadref[road_index : road_index + 2]
    road = roadref[road_index + 2 : hp_index]
    hp = roadref[hp_index + 2 : meter_index]
    meter = roadref[meter_index + 1 :]

    return (
        fylke
        + road_type
        + "{0:0>5}".format(str(road))
        + "{0:0>3}".format(str(hp))
        + "{0:0>5}".format(str(meter))
    )


def get_road_info(roadref):
    r = requests.get(
        "http://visveginfo-static.opentns.org/RoadInfoService/GetRoadDataAtReference?roadReference="
        + roadref
    )

    return xmltodict.parse(r.text)


def get_road_route(from_xy, to_xy):
    payload = {"AlignGeometriesWithRoute": True, "Points": [from_xy, to_xy]}
    road_r = requests.post(
        "http://visveginfo-static.opentns.org/RoadInfoService/GetRouteBetweenLocations",
        json=payload,
    )
    return xmltodict.parse(road_r.text)


def get_x_y(road_info):
    if isinstance(
        road_info["RoadDataCollection"]["RoadDataItems"]["RoadDataItem"], list
    ):
        road_data = road_info["RoadDataCollection"]["RoadDataItems"]["RoadDataItem"][0]
    else:
        road_data = road_info["RoadDataCollection"]["RoadDataItems"]["RoadDataItem"]

    x = road_data["RoadReferenceAtLocation"]["RoadNetPosition"]["X"]
    y = road_data["RoadReferenceAtLocation"]["RoadNetPosition"]["Y"]
    srid = road_data["RoadReferenceAtLocation"]["RoadNetPosition"]["SRID"]

    return {"SRID": srid, "X": x, "Y": y}


def get_geom(road_route):
    transform_coordinates = partial(
        pyproj.transform,
        pyproj.Proj(init="epsg:25833"),  # source coordinate system
        pyproj.Proj(init="epsg:4326"),
    )  # destination coordinate system

    if "RoadDataCollection" in road_route.keys():
        x = road_route["RoadDataCollection"]["RoadDataItems"]["RoadDataItem"][0][
            "RoadReferenceAtLocation"
        ]["RoadNetPosition"]["X"]
        y = road_route["RoadDataCollection"]["RoadDataItems"]["RoadDataItem"][0][
            "RoadReferenceAtLocation"
        ]["RoadNetPosition"]["Y"]
        srid = road_route["RoadDataCollection"]["RoadDataItems"]["RoadDataItem"][0][
            "RoadReferenceAtLocation"
        ]["RoadNetPosition"]["SRID"]

        p = shapely.geometry.Point(float(x), float(y))
        p_transformed = transform(transform_coordinates, p)

        return p_transformed
    elif "ArrayOfRoadReference" in road_route.keys():
        if isinstance(road_route["ArrayOfRoadReference"]["RoadReference"], list):
            segments = []
            for roadref in road_route["ArrayOfRoadReference"]["RoadReference"]:
                segment = shapely.wkt.loads(str(roadref["WKTGeometry"]))
                line_items = list(segment.coords)
                line_items = sorted(line_items, key=lambda k: [k[1], k[0]])
                segments.append(segment)

            merged = linemerge(segments)
            wkt = merged
            # wkt = shapely.geometry.LineString(line_items)

        else:
            wkt = shapely.wkt.loads(
                str(road_route["ArrayOfRoadReference"]["RoadReference"]["WKTGeometry"])
            )

        g_transformed = transform(transform_coordinates, wkt)

        return g_transformed


def get_route(from_vegref, to_vegref):
    print("Henter rute for " + from_vegref + " - " + to_vegref)
    from_visveg_ref = format_vegref(from_vegref)
    to_visveg_ref = format_vegref(to_vegref)

    from_road_info = get_road_info(from_visveg_ref)
    to_road_info = get_road_info(to_visveg_ref)

    from_xy = get_x_y(from_road_info)
    to_xy = get_x_y(to_road_info)

    route = get_road_route(from_xy, to_xy)

    return get_geom(route)


def _routes_iterator(row):
    return get_route(row["from_vegref"], row["to_vegref"])


def get_routes(_df, from_col="from_vegref", to_col="to_vegref"):
    _df["geometry"] = _df.apply(_routes_iterator, axis=1)

    return _df
