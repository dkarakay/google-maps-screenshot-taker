from main import create_map


def take_screenshot(lat: float, long: float, row: int, col: int, number: int, file_name: str):
    """

    Args:
        lat: Latitude of the left corner
        long: Longitude of the left corner
        row: Row count
        col: Column count
        number: Numbering to output file

    Returns:

    """
    create_map(
        lat_start=lat,
        long_start=long,
        zoom=20,
        number_rows=row,
        number_cols=col,
        scale=0.5,
        sleep_time=2,
        offset_left=0,
        offset_top=0.17,
        offset_right=0,
        offset_bottom=0.10,
        outfile=file_name,
        number=number,
    )


# Example: 5x5 -> 25 images
take_screenshot(
    lat=40.0100192,  # Top left corner latitude
    long=-83.0134145,  # Top left corner longitude
    row=3,  # 5 rows
    col=3,  # 5 columns
    file_name="image",  # Map image: "image-map-{number}.png"
    number=0,  # Starting from 0 like image-0.png, image-1.png ...
)
