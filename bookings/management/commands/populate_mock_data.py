from django.core.management.base import BaseCommand
from bookings.models import City, Package, Place, Circuit, CircuitStop
from django.db import transaction

class Command(BaseCommand):
    help = 'Populates the database with mock data for testing.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating mock data...")
        
        with transaction.atomic():
            # Create Cities
            cities_data = [
                "Madurai", "Trichy", "Tanjore", "Thanjavur",
                "Ooty", "Nilgiris", "Kodaikanal",
                "Chennai", "Kanchipuram", "Rameswaram", "Dhanushkodi"
            ]
            city_objs = {}
            for name in cities_data:
                city, _ = City.objects.get_or_create(name=name)
                city_objs[name] = city

            # Create Packages
            packages_data = [
                {
                    "name": "Tamil Nadu Heritage Package",
                    "description": "Explore the rich cultural and architectural heritage of Tamil Nadu through its ancient temples and historic cities."
                },
                {
                    "name": "Nilgiris Nature Retreat Package",
                    "description": "Escape to the misty hills and lush greenery of the Nilgiris for a peaceful and refreshing mountain getaway."
                },
                {
                    "name": "Coastal Tamil Nadu package",
                    "description": "Experience the beauty of the Bay of Bengal coastline, historic port towns, and sacred seaside temples."
                }
            ]
            pkg_objs = {}
            for pkg_info in packages_data:
                pkg, _ = Package.objects.get_or_create(
                    name=pkg_info["name"],
                    defaults={"description": pkg_info["description"]}
                )
                pkg_objs[pkg.name] = pkg

            # Create Places
            places_data = [
                {"name": "Meenakshi Amman Temple", "city": city_objs["Madurai"], "description": "A historic Hindu temple located on the southern bank of the Vaigai River."},
                {"name": "Rockfort Temple", "city": city_objs["Trichy"], "description": "A historic fortification and temple complex built on an ancient rock."},
                {"name": "Brihadisvara Temple", "city": city_objs["Tanjore"], "description": "A UNESCO World Heritage site and one of the largest South Indian temples."},
                {"name": "Botanical Garden", "city": city_objs["Ooty"], "description": "A vast garden featuring a diverse collection of temperate and sub-tropical plants."},
                {"name": "Coaker's Walk", "city": city_objs["Kodaikanal"], "description": "A scenic pedestrian path offering breathtaking views of the valley."},
                {"name": "Marina Beach", "city": city_objs["Chennai"], "description": "One of the longest urban beaches in the world."},
                {"name": "Ramanathaswamy Temple", "city": city_objs["Rameswaram"], "description": "A sacred Hindu temple dedicated to Lord Shiva, located on Rameswaram island."}
            ]
            place_objs = {}
            for p_info in places_data:
                place, _ = Place.objects.get_or_create(
                    name=p_info["name"],
                    defaults={"city": p_info["city"], "description": p_info["description"]}
                )
                place_objs[place.name] = place

            # Create Circuits
            circuits_data = [
                {
                    "package": pkg_objs["Tamil Nadu Heritage Package"],
                    "name": "Temple Trail of the South",
                    "description": "A journey through the grandest temples of Madurai and Tanjore.",
                    "base_price": 15000.00,
                    "stops": ["Meenakshi Amman Temple", "Brihadisvara Temple"]
                },
                {
                    "package": pkg_objs["Nilgiris Nature Retreat Package"],
                    "name": "Mist and Mountains",
                    "description": "Relax in the serene hills of Ooty and Kodaikanal.",
                    "base_price": 12000.00,
                    "stops": ["Botanical Garden", "Coaker's Walk"]
                },
                {
                    "package": pkg_objs["Coastal Tamil Nadu package"],
                    "name": "Azure Coastline Journey",
                    "description": "Explore the sandy shores and spiritual sites along the coast.",
                    "base_price": 10000.00,
                    "stops": ["Marina Beach", "Ramanathaswamy Temple"]
                }
            ]

            for c_info in circuits_data:
                circuit, _ = Circuit.objects.get_or_create(
                    name=c_info["name"],
                    defaults={
                        "package": c_info["package"],
                        "description": c_info["description"],
                        "base_price": c_info["base_price"]
                    }
                )
                # Add stops
                for i, place_name in enumerate(c_info["stops"]):
                    CircuitStop.objects.get_or_create(
                        circuit=circuit,
                        place=place_objs[place_name],
                        defaults={"order": i + 1}
                    )

        self.stdout.write(self.style.SUCCESS("Successfully populated mock data!"))
