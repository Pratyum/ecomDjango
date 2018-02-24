import requests
import json

headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer sand_nQYG5uxLQWQrjyKchfc6+vQgPET/X1yUPoqxpe5Ed18='
}

google_api_key = "AIzaSyBChC6iDgmDJfEj0Ttdc7sQ0dfEFSj0RBk"
def get_ratio_and_savings(ordered_items, origin_postal_code, destination_postal_code):
    #ordered_items is an array of dicts which have weight, height, width, length and price of the items
    #Get the individual prices for the ordered items from easyship api
    individual_prices_cheap = []
    individual_prices_premium = []
    collated_weight = 0
    collated_height = 0
    collated_width = 0
    collated_length = 0
    #Intializing a common set of parameters for making the post request so that only the
    #value for 'items' key needs to change
    data_dict = {}
    data_dict = {"origin_country_alpha2": "SG", "destination_country_alpha2": "SG", "taxes_duties_paid_by":"Sender", "is_insured":False}
    data_dict["origin_postal_code"] = origin_postal_code
    data_dict["destination_postal_code"] = destination_postal_code

    for item in ordered_items:
        data_items_arr = []
        #####Possibly use the actual price of the product instead of hardcoding
        data_item = {"category": "audio_video", "declared_currency": "SGD", "declared_customs_value": 250}
        data_item["actual_weight"] = item["weight"]
        data_item["height"] = item["height"]
        data_item["width"] = item["width"]
        data_item["length"] = item["length"]
        data_items_arr.append(data_item)
        data_dict["items"] = data_items_arr

        #Updating the collated measures to be used later
        collated_weight += item["weight"]
        collated_height += item["height"]
        if collated_length < item["length"]:
            collated_length = item["length"]
        if collated_width < item["width"]:
            collated_width = item["width"]

        #Making the api request for a single item
        r = requests.post("https://api-sandbox.easyship.com/rate/v1/rates", data=json.dumps(data_dict), headers=headers)
        api_shipment_price_cheap = json.loads(r.text)["rates"][0]["shipment_charge_total"]
        individual_prices_cheap.append(api_shipment_price_cheap)

        api_shipment_price_premium = json.loads(r.text)["rates"][-1]["shipment_charge_total"]
        individual_prices_premium.append(api_shipment_price_premium)

    #Get the collated shipment price from easyship api
    data_items_collated_arr = []
    #####Use the collated price possibly
    data_item_collated = {"category": "audio_video", "declared_currency": "SGD", "declared_customs_value": 250}
    data_item_collated["actual_weight"] = collated_weight
    data_item_collated["height"] = collated_height
    data_item_collated["width"] = collated_width
    data_item_collated["length"] = collated_length
    data_items_collated_arr.append(data_item_collated)
    data_dict["items"] = data_items_collated_arr

    #Making the api request for the collated items list
    r = requests.post("https://api-sandbox.easyship.com/rate/v1/rates", data=json.dumps(data_dict), headers=headers)
    collated_price_cheap = json.loads(r.text)["rates"][0]["shipment_charge_total"]
    collated_price_premium = json.loads(r.text)["rates"][-1]["shipment_charge_total"]

    #Getting the predicted individual prices from the linear model

    #Learned coefficients from the trained linear model
    weight_coef = 3.3618435
    distance_coef = 1.02210429e-03
    intercept = 3.57886429833

    #Calculate the distance between the source and destination points using google api
    request_str = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins=%s&destinations=%s&key=%s' % (origin_postal_code, destination_postal_code, google_api_key)
    response = requests.get(request_str)
    try:
        distance = float(json.loads(response.text)['rows'][0]['elements'][0]['distance']['text'].split()[0].replace(",", ""))
    except:
        print 'error'

    predicted_prices = []
    for item in ordered_items:
        y = item["weight"]*weight_coef + distance*distance_coef + intercept
        predicted_prices.append(y)
    price_weights = []
    for p in predicted_prices:
        price_weights.append(p/sum(predicted_prices))

    #Calculate the savings
    # per_item_saving = []
    # for idx, w in enumerate(price_weights):
    #     saving = individual_prices[idx] - collated_price*w
    #     per_item_saving.append(saving)

    blitzkreig_prices_premium = [p*collated_price_premium for p in price_weights]

    return blitzkreig_prices_premium, individual_prices_cheap, individual_prices_premium
