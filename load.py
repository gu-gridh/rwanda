#%%
from typing import List
from .models import *
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
from django.db import transaction
from typing import Union
#%%
import os
import json
from tqdm import tqdm

#%%
@transaction.atomic
def create_places_of_interest(model: PlaceOfInterest, name_model: Name, data: List, informant: Informant, place_type: PlaceType):

    props_to_keep = (
        'amenity',
        'name',
        'name:fr',
        'shop',
        'railway',
        'tourism',
        'highway',
        'office',
        'type',
    )

    places = []
    for place in (progress := tqdm(data['features'])):
        
        # Only keep certain properties
        props = {k: v for k, v in place['properties'].items() if k in props_to_keep}

        description = "\n".join([prop for key, prop in props.items() if (prop and key not in ('name', 'name:fr'))])

        # If it is a street route, ignore it
        if props.get('type', None):
            if props['type'] == 'route':
                continue

        # Create the geometries from geojson
        place_str = json.dumps(place['geometry'])
        geometry    = GEOSGeometry(place_str)

        # Create the place
        place_of_interest, _ = model.objects.get_or_create(
            geometry=geometry, 
            comment="This place was originally automatically uploaded from Open Street Map source data.",
            description=description,
            type=place_type,
            )

        # Fetch the names, if any
        osm_name_english = props.get('name', None)
        osm_name_french  = props.get('name:fr', None)
        
        progress.set_description(f"Processing {osm_name_english}/{osm_name_french}")

        # Create name objects (just English or French)
        # The English name
        if osm_name_english:
            name_english = name_model.objects.create(
                text=osm_name_english, 
                note="Name crowd-sourced from Open Street Map.",
                referent=place_of_interest
                )

            name_english.informants.add(informant)
            name_english.languages.add(Language.objects.get(name='English'))
            name_english.save()

        # The French name
        if osm_name_french:
            name_french = name_model.objects.create(
                text=osm_name_french,
                note="Name crowd-sourced from Open Street Map.",
                referent=place_of_interest
                )

            name_french.informants.add(informant)
            name_french.languages.add(Language.objects.get(name='French'))
            name_french.save()
        
        places.append(place_of_interest)

    # place_of_interest.objects.bulk_create(places)

    return places





@transaction.atomic
def features(
    building_path,
    street_path
    ):

    # Delete everything
    Informant.objects.all().delete()
    Author.objects.all().delete()
    PlaceOfInterest.objects.all().delete()
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
    for osm, place_type_str in ((buildings_osm, "building"), (streets_osm, "street")):
        place_type, _ = PlaceType.objects.get_or_create(text=place_type_str)
        places = create_places_of_interest(PlaceOfInterest, Name, osm, informant, place_type)
    

    
    