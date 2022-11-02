#%%
from typing import List
from .models import *
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
from django.db import transaction

#%%
import os
import json
from tqdm import tqdm
#%%
@transaction.atomic
def create_places_of_interest(model: PlaceOfInterest, data: List, informant: Informant):

    places = []
    for place in (progress := tqdm(data['features'])):

        place_str = json.dumps(place['geometry'])

        # Create the geometries from geojson
        geometry    = GEOSGeometry(place_str)

        # Create the place
        place_of_interest, _ = model.objects.get_or_create(geometry=geometry, comment="This place was originally automatically uploaded from Open Street Map source data.")

        # Fetch the names, if any
        osm_name_english = place['properties'].get('name', None)
        osm_name_french  = place['properties'].get('name:fr', None)
        
        progress.set_description(f"Processing {osm_name_english}/{osm_name_french}")

        # Create name objects (just English or French)
        # The English name
        if osm_name_english:
            name_english, _ = Name.objects.get_or_create(
                text=osm_name_english, 
                note="Name crowd-sourced from Open Street Map.",
                )

            name_english.informants.add(informant)
            name_english.languages.add(Language.objects.get(name='English'))
            name_english.save()

            place_of_interest.names.add(name_english)


        # The French name
        if osm_name_french:
            name_french, _ = Name.objects.get_or_create(
                text=osm_name_french,
                note="Name crowd-sourced from Open Street Map.",
                )

            name_french.informants.add(informant)
            name_french.languages.add(Language.objects.get(name='French'))
            name_french.save()


            place_of_interest.names.add(name_french)
        
        place_of_interest.save()

        places.append(place_of_interest)

    return places





@transaction.atomic
def features(
    building_path='/home/vws/Projects/diana-backend/apps/rwanda/local_data/building_features.geojson',
    street_path='/home/vws/Projects/diana-backend/apps/rwanda/local_data/street_features.geojson'
    ):

    # Delete everything
    Informant.objects.all().delete()
    Author.objects.all().delete()
    Street.objects.all().delete()
    Building.objects.all().delete()
    Name.objects.all().delete()
    Language.objects.all().delete()
    # Period.objects.all().delete()
    # Image.objects.all().delete()
    # Text.objects.all().delete()


    informant, _ = Informant.objects.get_or_create(custom_id="OSM", note="The OSM informant representents the crowd of informants contributing to the Open Street Map.")

    # Create the different languages
    for name, abbreviation in (('English', 'en'), ('French', 'fr'), ('Kinyarwanda', 'rw'), ('Kiswahili', 'sw')):
        language, _ = Language.objects.get_or_create(name=name, abbreviation=abbreviation)

    # Read the data
    with open(building_path, 'r') as f:
        buildings_osm = json.load(f)

    with open(street_path, 'r') as f:
        streets_osm = json.load(f)

    # Build the data
    buildings = create_places_of_interest(Building, buildings_osm, informant)
    streets   = create_places_of_interest(Street, streets_osm, informant)
    

    
    