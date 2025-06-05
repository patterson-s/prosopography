import json

# Create a mapping dictionary based on the PDF information - VERIFIED
hlp_mapping = {
    # High-Level Panel on Threats, Challenges and Change (2004) — 15 Members
    "Anand Panyarachun": {"hlp": "Threats, Challenges and Change", "hlp_year": 2004},
    "Robert Badinter": {"hlp": "Threats, Challenges and Change", "hlp_year": 2004},
    "Gro Harlem Brundtland": {"hlp": "Threats, Challenges and Change", "hlp_year": 2004},
    "Mary Chinery-Hesse": {"hlp": "Threats, Challenges and Change", "hlp_year": 2004},
    "Gareth Evans": {"hlp": "Threats, Challenges and Change", "hlp_year": 2004},
    "David Hannay": {"hlp": "Threats, Challenges and Change", "hlp_year": 2004},
    "Enrique Iglesias": {"hlp": "Threats, Challenges and Change", "hlp_year": 2004},
    "Amre Moussa": {"hlp": "Threats, Challenges and Change", "hlp_year": 2004},
    "Satish Nambiar": {"hlp": "Threats, Challenges and Change", "hlp_year": 2004},
    "Sadako Ogata": {"hlp": "Threats, Challenges and Change", "hlp_year": 2004},
    "Yevgeny Primakov": {"hlp": "Threats, Challenges and Change", "hlp_year": 2004},
    "Qian Qichen": {"hlp": "Threats, Challenges and Change", "hlp_year": 2004},
    "Nafis Sadik": {"hlp": "Threats, Challenges and Change", "hlp_year": 2004},
    "Salim Ahmed Salim": {"hlp": "Threats, Challenges and Change", "hlp_year": 2004},
    "Brent Scowcroft": {"hlp": "Threats, Challenges and Change", "hlp_year": 2004},
    
    # High-Level Panel on Digital Cooperation (2020) — 22 Members
    "Melinda Gates": {"hlp": "Digital Cooperation", "hlp_year": 2020},  # Listed as "Melinda French Gates" in PDF
    "Jack Ma": {"hlp": "Digital Cooperation", "hlp_year": 2020},
    "Mohammad Abdullah Al Gergawi": {"hlp": "Digital Cooperation", "hlp_year": 2020},
    "Yuichiro Anzai": {"hlp": "Digital Cooperation", "hlp_year": 2020},
    "Nikolai Astrup": {"hlp": "Digital Cooperation", "hlp_year": 2020},
    "Vinton Cerf": {"hlp": "Digital Cooperation", "hlp_year": 2020},
    "Fadi Chehadé": {"hlp": "Digital Cooperation", "hlp_year": 2020},
    "Sophie Soowon Eom": {"hlp": "Digital Cooperation", "hlp_year": 2020},
    "Isabel Guerrero Pulgar": {"hlp": "Digital Cooperation", "hlp_year": 2020},
    "Marina Kaljurand": {"hlp": "Digital Cooperation", "hlp_year": 2020},
    "Bogolo Kenewendo": {"hlp": "Digital Cooperation", "hlp_year": 2020},
    "Marina Kolesnik": {"hlp": "Digital Cooperation", "hlp_year": 2020},
    "Doris Leuthard": {"hlp": "Digital Cooperation", "hlp_year": 2020},
    "Cathy Mulligan": {"hlp": "Digital Cooperation", "hlp_year": 2020},
    "Akaliza Keza Ntwari": {"hlp": "Digital Cooperation", "hlp_year": 2020},
    "Edson Prestes": {"hlp": "Digital Cooperation", "hlp_year": 2020},
    "Kira Radinsky": {"hlp": "Digital Cooperation", "hlp_year": 2020},
    "Nanjira Sambuli": {"hlp": "Digital Cooperation", "hlp_year": 2020},
    "Dhananjayan Sriskandarajah": {"hlp": "Digital Cooperation", "hlp_year": 2020},
    "Jean Tirole": {"hlp": "Digital Cooperation", "hlp_year": 2020},
    "Amandeep Singh Gill": {"hlp": "Digital Cooperation", "hlp_year": 2020},  # Executive Director
    "Jovan Kurbalija": {"hlp": "Digital Cooperation", "hlp_year": 2020},     # Executive Director
    
    # High-Level Panel of Eminent Persons on the Post-2015 Development Agenda (2012) — 27 Members
    "Susilo Bambang Yudhoyono": {"hlp": "Post-2015 Development Agenda", "hlp_year": 2012},
    "Ellen Johnson Sirleaf": {"hlp": "Post-2015 Development Agenda", "hlp_year": 2012},
    "David Cameron": {"hlp": "Post-2015 Development Agenda", "hlp_year": 2012},
    "Fulbert Gero Amoussouga": {"hlp": "Post-2015 Development Agenda", "hlp_year": 2012},
    "Izabella Teixeira": {"hlp": "Post-2015 Development Agenda", "hlp_year": 2012},
    "Yingfan Wang": {"hlp": "Post-2015 Development Agenda", "hlp_year": 2012},
    "Maria Angela Holguin": {"hlp": "Post-2015 Development Agenda", "hlp_year": 2012},
    "Gisela Alonso": {"hlp": "Post-2015 Development Agenda", "hlp_year": 2012},
    "Jean-Michel Severino": {"hlp": "Post-2015 Development Agenda", "hlp_year": 2012},
    "Horst Kohler": {"hlp": "Post-2015 Development Agenda", "hlp_year": 2012},
    "Naoto Kan": {"hlp": "Post-2015 Development Agenda", "hlp_year": 2012},
    "Queen Rania of Jordan": {"hlp": "Post-2015 Development Agenda", "hlp_year": 2012},
    "Betty Maina": {"hlp": "Post-2015 Development Agenda", "hlp_year": 2012},
    "Abhijit Banerjee": {"hlp": "Post-2015 Development Agenda", "hlp_year": 2012},
    "Andris Piebalgs": {"hlp": "Post-2015 Development Agenda", "hlp_year": 2012},
    "Patricia Espinosa": {"hlp": "Post-2015 Development Agenda", "hlp_year": 2012},
    "Paul Polman": {"hlp": "Post-2015 Development Agenda", "hlp_year": 2012},
    "Ngozi Okonjo-Iweala": {"hlp": "Post-2015 Development Agenda", "hlp_year": 2012},
    "Elvira Nabiullina": {"hlp": "Post-2015 Development Agenda", "hlp_year": 2012},
    "Graca Machel": {"hlp": "Post-2015 Development Agenda", "hlp_year": 2012},
    "Sung-Hwan Kim": {"hlp": "Post-2015 Development Agenda", "hlp_year": 2012},
    "Gunilla Carlsson": {"hlp": "Post-2015 Development Agenda", "hlp_year": 2012},
    "Emilia Pires": {"hlp": "Post-2015 Development Agenda", "hlp_year": 2012},
    "Kadir Topbas": {"hlp": "Post-2015 Development Agenda", "hlp_year": 2012},
    "John Podesta": {"hlp": "Post-2015 Development Agenda", "hlp_year": 2012},
    "Tawakel Karman": {"hlp": "Post-2015 Development Agenda", "hlp_year": 2012},  # Also written as "Tawakkol Karman"
    "Amina J. Mohammed": {"hlp": "Post-2015 Development Agenda", "hlp_year": 2012},
    
    # High-Level Panel on System-Wide Coherence in the Areas of Development, Humanitarian Assistance, and the Environment (2007) — 15 Members
    "Shaukat Aziz": {"hlp": "System-Wide Coherence", "hlp_year": 2007},
    "Luísa Dias Diogo": {"hlp": "System-Wide Coherence", "hlp_year": 2007},
    "Jens Stoltenberg": {"hlp": "System-Wide Coherence", "hlp_year": 2007},
    "Gordon Brown": {"hlp": "System-Wide Coherence", "hlp_year": 2007},
    "Mohamed T. El-Ashry": {"hlp": "System-Wide Coherence", "hlp_year": 2007},
    "Robert Greenhill": {"hlp": "System-Wide Coherence", "hlp_year": 2007},
    "Ruth Jacoby": {"hlp": "System-Wide Coherence", "hlp_year": 2007},
    "Ricardo Lagos": {"hlp": "System-Wide Coherence", "hlp_year": 2007},
    "Louis Michel": {"hlp": "System-Wide Coherence", "hlp_year": 2007},
    "Benjamin W. Mkapa": {"hlp": "System-Wide Coherence", "hlp_year": 2007},
    "Jean-Michel Severino": {"hlp": "System-Wide Coherence", "hlp_year": 2007},  # Note: appears in both 2007 and 2012 panels
    "Josette S. Sheeran": {"hlp": "System-Wide Coherence", "hlp_year": 2007},
    "Keizo Takemi": {"hlp": "System-Wide Coherence", "hlp_year": 2007},
    "Lennart Båge": {"hlp": "System-Wide Coherence", "hlp_year": 2007},
    "Kemal Derviş": {"hlp": "System-Wide Coherence", "hlp_year": 2007},
}

def add_hlp_metadata(data):
    """
    Add HLP (High-Level Panel) metadata to the dataset
    
    Args:
        data: The loaded JSON data from your dataset
    
    Returns:
        Modified data with HLP information added
    """
    
    # Iterate through each entry in the dataset
    for entry in data:
        if isinstance(entry, list):
            # Handle the case where the entry is a list (as in your example)
            for person_data in entry:
                if "person" in person_data and "name" in person_data["person"]:
                    person_name = person_data["person"]["name"]
                    
                    # Add HLP metadata if person is found in mapping
                    if person_name in hlp_mapping:
                        person_data["person"]["metadata"]["hlp"] = hlp_mapping[person_name]["hlp"]
                        person_data["person"]["metadata"]["hlp_year"] = hlp_mapping[person_name]["hlp_year"]
                        print(f"Added HLP metadata for {person_name}")
                    else:
                        print(f"Warning: No HLP mapping found for {person_name}")
        
        elif isinstance(entry, dict) and "person" in entry:
            # Handle the case where the entry is a dictionary
            person_name = entry["person"]["name"]
            
            if person_name in hlp_mapping:
                entry["person"]["metadata"]["hlp"] = hlp_mapping[person_name]["hlp"]
                entry["person"]["metadata"]["hlp_year"] = hlp_mapping[person_name]["hlp_year"]
                print(f"Added HLP metadata for {person_name}")
            else:
                print(f"Warning: No HLP mapping found for {person_name}")
    
    return data

# Example usage:
if __name__ == "__main__":
    with open(r"C:\Users\spatt\Desktop\consultocracy_dashboard\data\career_trajectories_03_dates_normalized.json", 'r') as f:
        dataset = json.load(f)
    
    # Add HLP metadata
    updated_dataset = add_hlp_metadata(dataset)
    
    # Save the updated dataset
    with open(r"C:\Users\spatt\Desktop\consultocracy_dashboard\data\career_trajectories_03_dates_normalized_with_hlp.json", 'w') as f:
        json.dump(updated_dataset, f, indent=2)
    
    print("Dataset updated with HLP metadata!")