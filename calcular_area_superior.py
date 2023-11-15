import json
import requests
import base64
from PIL import Image
import io
import numpy as np
import rasterio.features
import shapely.geometry
import cv2




API_URL = "https://api-inference.huggingface.co/models/nvidia/segformer-b0-finetuned-ade-512-512"
headers = {"Authorization": "Bearer "}


def stringToRGB(base64_string):
    # convert base64 string to numpy array
    imgdata = base64.b64decode(str(base64_string))
    image = Image.open(io.BytesIO(imgdata))
    return np.array(image)


def convert_strMasks(result):
    # Convert string masks to arrays and return masks + mask_labels
    masks = [stringToRGB(r["mask"]).astype('int') for r in result]
    mask_labels = [r["label"] for r in result]

    return masks, mask_labels


def convert_bMask_to_polygon(binary_mask):
    # Binary mask should be a Numpy Array
    shapes = rasterio.features.shapes(binary_mask)
    polygons = [shapely.geometry.Polygon(shape[0]["coordinates"][0]) for shape in shapes if shape[1] == 255]

    return polygons


def polygons_to_lol(polygon_list):
    # Shapely polygons to List of numpy arrays defining the polygon

    list_of_lists = []
    
    for idx, polygon in enumerate(polygon_list):
        output = np.array(polygon[idx].exterior.coords, dtype='int32')
        list_of_lists.append(output)
    
    return list_of_lists


def visualize_polygons(polygon_list, image):
    # Draw polygons for predictions on image
    poly_list = polygons_to_lol(polygon_list=polygon_list)
    colors = [(255, 0, 0), (0, 255, 0)]
    raw_image = image.copy()
    for idx, poly in enumerate(poly_list):
    # Use fillPoly() function and give input as
    # image, end points,color of polygon
    # Here color of polygon will blue and green
        color = colors[idx]
        image_poly_added = cv2.fillPoly(raw_image, pts=[poly], color=color)
        alpha = 0.4  # Transparency factor.
        # Following line overlays transparent rectangle
        # over the image
        image = cv2.addWeighted(image_poly_added, alpha, image, 1 - alpha, 0)
        
    # Displaying the image
    resize_img = cv2.resize(image, (500, 500))
    cv2.imshow("Resultado de Segmentacion", resize_img)
    
    cv2.waitKey(0)


def query(filename):
    '''
    Send filename as data to Hugging Face Server.
    The Server will process the data with a Segmentation Machine Learning model.
    The results will be returned as a JSON response.
    '''
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()


def calculate_areas(polygon_map):

    earth_polygon_area = 0
    plant_polygon_area = 0

    for label, polygon_list in polygon_map.items():
        if label == 'earth':
            for polygon in polygon_list:
                earth_polygon_area += polygon.area

        elif label == 'plant':
            for polygon in polygon_list:
                plant_polygon_area += polygon.area

    return earth_polygon_area, plant_polygon_area    


def convert_pixel_area_to_real_area(earth_area, plant_area):
    '''
    Converts area for earth and plants from pixels^2 to m^2
    '''
    # Camera width and height in pixels (Resolution of images taken by webcam)
    camera_width = 1920
    camera_height = 1080

    # Real width and Height in meters (To be Calibrated later)
    real_width = 16
    real_height = 9

    # Number that converts from px^2 to m^2
    px_to_m_conversion_factor = (real_width*real_height)/(camera_width*camera_height)

    real_earth_area = earth_area*px_to_m_conversion_factor
    real_plant_area = plant_area*px_to_m_conversion_factor

    return real_earth_area, real_plant_area


def output_areas():
    # Actual Running Code
    image_path = "images/rabano-rojo-ejemplo.jpg"
    segmentation_data = query(filename=image_path)

    rabano_image = cv2.imread(image_path)

    masks, mask_labels = convert_strMasks(result=segmentation_data)

    polygon_list = []
    polygon_map = {}
    for mask, label in zip(masks, mask_labels):
        if label == 'plant' or label == 'earth':
            print("label", label)
            polygon_list.append(convert_bMask_to_polygon(mask))
            polygon_map[label] = convert_bMask_to_polygon(mask)

    print(len(polygon_list))
    visualize_polygons(polygon_list=polygon_list, image=rabano_image)

    earth_area, plant_area = calculate_areas(polygon_map=polygon_map)

    real_earth_area, real_plant_area = convert_pixel_area_to_real_area(earth_area=earth_area,
                                                                    plant_area=plant_area)

    print('Area de Tierra: ', f'{real_earth_area: .2f} m^2')
    print('Area de Plantas: ', f'{real_plant_area: .2f} m^2')

    return real_earth_area, real_plant_area
