from app.models.attractions import Attractions

def seed_attractions(db):
    attractions = [
        Attractions(
            name="Phi Phi Islands", 
            description="Phi Phi Islands are a group of islands in Thailand between the large island of Phuket and the Malacca Coastal Strait of Thailand.",
            cover_image=None,
            location="Thailand",
            is_active=True
        ),
        Attractions(
            name="Eiffel Tower", 
            description="Eiffel Tower is one of the most famous structures in the world. Eiffel Tower is named after a leading French architect and engineer. It was built as a symbol of the World Fair in 1889.",
            cover_image=None,
            location="France",
            is_active=True
        ),
        Attractions(
            name="Times Square", 
            description="Times Square has become a global landmark and has become a symbol of New York City. This is a result of Times Square being a modern, futuristic venue, with huge advertising screens dotting its surroundings.",
            cover_image=None,
            location="USA",
            is_active=True
        ),
        Attractions(
            name="Great Wall of China", 
            description="The Great Wall of China is a series of fortifications that stretch across northern China. It was built to protect Chinese states and empires against invasions and raids from nomadic groups from the Eurasian Steppe.",
            cover_image=None,
            location="China",
            is_active=True
        )
    ]

    for a in attractions:
        exists = db.query(Attractions).filter_by(name=a.name).first()
        if not exists:
            db.add(a)

    db.commit()
