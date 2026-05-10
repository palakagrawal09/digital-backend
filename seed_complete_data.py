"""
Complete Database Seeding Script - All Products with Images and Specifications
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid
from datetime import datetime, timezone

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

async def seed_complete_database():
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("🌱 Starting complete database seeding...")
    
    # Clear existing data
    print("Clearing existing collections...")
    await db.products.delete_many({})
    await db.product_categories.delete_many({})
    await db.services.delete_many({})
    await db.clients.delete_many({})
    
    # Seed Product Categories
    print("Seeding product categories...")
    categories = [
        {
            "id": str(uuid.uuid4()),
            "name": "Fire Control Systems",
            "icon": "Target",
            "sort_order": 1,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Inspection & Safety Systems",
            "icon": "Search",
            "sort_order": 2,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Counter-Insurgency & Surveillance",
            "icon": "Eye",
            "sort_order": 3,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Simulators & Training",
            "icon": "Gamepad2",
            "sort_order": 4,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
    ]
    await db.product_categories.insert_many(categories)
    
    fire_control_id = categories[0]["id"]
    inspection_id = categories[1]["id"]
    surveillance_id = categories[2]["id"]
    simulators_id = categories[3]["id"]
    
    # Seed Complete Products with Images and Specifications
    print("Seeding complete product catalog...")
    products = [
        # Fire Control Systems
        {
            "id": str(uuid.uuid4()),
            "name": "AMFDC MK-II (Discontinued)",
            "category_id": fire_control_id,
            "description": "Automatic Mortar Fire Data Controller/Computer is a small hand held wonder power, which was a requirement of Infantry. Gives immediate calculations and data to MFC for firing mortar.",
            "specifications": """• Capacity to store Mortar positions MP Grid reference
• Capacity to store Target positions IM Grid reference
• Capacity to store pre-stored safe zones (2 points & 3 points both methods)
• Capacity to store pre-stored crest (1 points & 2 points both method)
• Getting environmental temperature using temperature probe (External)
• LCD display with backlight for night vision
• Compact and Rugged design for field operations""",
            "images": ["/assets/amfdc-device.jpg", "/assets/artillery-firing.jpg"],
            "published": True,
            "sort_order": 1,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "name": "AMFDC MK-III",
            "category_id": fire_control_id,
            "description": "Advanced handheld device with plotter mode and GPS capabilities. High brightness sunlight readable LCD display. IP 65 compliant. Up to 8 Hrs battery backup. Shock/Vibration, Drop, Rain, Temp test passed.",
            "specifications": """• High brightness sunlight readable LCD display
• IP 65 compliant
• Up to 8 Hrs battery backup
• Shock/Vibration, Drop, Rain, Temp test passed
• Supports Standard AMFDC & Plotter mode
• GPS interface for exact OWN location
• Zoom capability for target area corrections
• Store 100 MP, IM positions, safe zones, crest data
• Map range and Trajectory range display
• Ammunition swapping capability
• Built-in GPS module
• 5V DC power input, 3.7V 5000mAh battery
• Dimensions: 105 x 185 x 60mm
• MIL-STD-810F compliant""",
            "images": ["/assets/amfdc-device.jpg"],
            "published": True,
            "sort_order": 2,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "name": "TEEVRA FDC",
            "category_id": fire_control_id,
            "description": "Firing Data Computer for Company Support Weapons (CSWs). Calculates data for MMG, AGL, and AGS-30 automatically and accurately without manually referring to range tables.",
            "specifications": """• Calculates data for MMG, AGL, and AGS-30 firing
• Store multiple targets in one equipment
• Integrated GPS for own location lat-long
• Crest clearance calculation facility
• Quick availability of accurate firing data
• No need to refer range tables
• Compact and easy to carry
• High Speed CPU & GPS
• Eliminates human calculation errors
• Supports full range of company support weapon systems""",
            "images": ["/assets/teevra-device.jpg", "/assets/gun-barrel-firing.jpg"],
            "published": True,
            "sort_order": 3,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        
        # Inspection & Safety Systems
        {
            "id": str(uuid.uuid4()),
            "name": "GBInP-17 Universal",
            "category_id": inspection_id,
            "description": "Gun Barrel Inspection System universally designed for inspecting barrels of Field Guns (105mm, 120mm, 125mm, 130mm & 155mm). Integration of electronics, optic sensors and mechanical design.",
            "specifications": """• Universal design for 105mm to 155mm barrels
• 3.5/4.3" display, 640x480 resolution
• Real-time operating system
• Composite video output
• SD Card storage for video/images
• 9mm probe diameter, 3M working length
• 2-way/4-way articulation with joystick
• Brightness, Contrast, Color adjustable
• Chargeable 7.4V battery / 12V adapter
• Detects cracks, pits, and barrel defects early""",
            "images": ["/assets/gbinp-probe.jpg", "/assets/gun-barrel-firing.jpg"],
            "published": True,
            "sort_order": 1,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "name": "LCGB-HMRSV-21-XG",
            "category_id": inspection_id,
            "description": "Advanced Gun Barrel Inspection System with AI/ML algorithms. Industrial Grade Computing Platform with 8-12\" display, i7 processor, 8GB RAM, 1TB storage.",
            "specifications": """• Compatible for 105mm to 155mm & ATAGS barrels
• Indigenously developed by ARDE, Pune
• Real-time images with Angular & Linear Data
• Auto/Manual sensor module operation
• Video recording and snapshot facility
• Measuring size/Area of defects (Cracks, Pits)
• AI & ML based analysis and comparison
• Report generation capability
• 8-12" display, i7 processor, 8GB RAM, 1TB storage
• Rugged IGCP Industrial Grade Computing Platform
• 2/4/5/8 MP image resolution
• LED adjustable illumination, Auto/Manual focus""",
            "images": ["/assets/lcgb-system.jpg"],
            "published": True,
            "sort_order": 2,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "name": "IAPS (Integrated Accident Prevention System)",
            "category_id": inspection_id,
            "description": "Designed by MCTE, manufactured by DIPL. Detects hazardous levels of Carbon Monoxide, LPG leakage, Fire, High Temperature and Proximity to heating appliances.",
            "specifications": """• Wireless CO sensor unit and multi-sensor unit
• Detects: Carbon Monoxide, LPG, Fire, Temperature, Proximity
• Industrial grade high quality sensors
• Fully automatic operation
• Dual alarm generation (point of use & central locator)
• Portable & ruggedized design
• Rechargeable battery powered
• Indoor/Outdoor central alert unit
• Adjustable configuration/calibration
• Suitable for FRPs/Tents/Shelter/Bunkers in HAA""",
            "images": ["/assets/iaps-system.jpg"],
            "published": True,
            "sort_order": 3,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        
        # Counter-Insurgency & Surveillance
        {
            "id": str(uuid.uuid4()),
            "name": "FSD Flexible / INVSS",
            "category_id": surveillance_id,
            "description": "Flexible Surveillance Device for Counter-Insurgency operations. Used in CI ops of enemy hideouts & difficult to reach locations. Also used for NDT inspection.",
            "specifications": """• 3.5/4.3" display, 640x480 resolution
• Real-time operating system
• Composite video format, CCIR image format
• SD Card storage
• Brightness, Contrast, Color adjustable
• 9mm probe diameter, 3M working length
• 2-way/4-way articulation with joystick
• 7.4V rechargeable battery / 12V adapter
• Suitable for CI operations and NDT inspection
• Portable and rugged design""",
            "images": ["/assets/fsd-flexible.jpg"],
            "published": True,
            "sort_order": 1,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Electronic Multi-Function Target System",
            "category_id": surveillance_id,
            "description": "Firing Display Unit (FDU) for Indoor-Outdoor firing ranges. Tabs with Wi-Fi connectivity for live firing results display.",
            "specifications": """• 8-10 inch tablet screen
• High sensitive Wi-Fi connectivity
• Adjustable customized display stand
• Live firing results display
• Bullet hit monitoring
• Firing score and grouping result display
• Zeroing result with MPI display
• Error calculation (x-direction, y-direction)
• Proposed corrections display
• Individual displays for firer, firing officer, armorer""",
            "images": ["/assets/target-system.jpg"],
            "published": True,
            "sort_order": 2,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Telemetry Bomb",
            "category_id": surveillance_id,
            "description": "Advanced telemetry system for bomb trajectory analysis and performance monitoring.",
            "specifications": """• Real-time telemetry data transmission
• Trajectory analysis capability
• Performance monitoring
• Rugged design for field conditions
• Wireless data transmission""",
            "images": ["/assets/telemetry-bomb.jpg"],
            "published": True,
            "sort_order": 3,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        
        # Simulators
        {
            "id": str(uuid.uuid4()),
            "name": "ATGM (SV21) Simulator",
            "category_id": simulators_id,
            "description": "100% indigenously developed ATGM Crew Training Simulator. Comprehensive 3D CGI scenarios with realistic missile dynamics.",
            "specifications": """• 100% indigenously developed
• Comprehensive 3D CGI scenario database
• Realistic missile dynamics simulation
• Technical fault simulation on missiles
• Different target offerings
• Environmental effects: rain, fog, visibility, cloud, temperature, wind
• Realistic sound simulation
• Night training provision
• Scenario-based training environments
• Performance tracking and scoring""",
            "images": ["/assets/atgm-missile.jpg", "/assets/atgm-simulator-scope.jpg"],
            "published": True,
            "sort_order": 1,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "name": "81mm Mortar Simulator",
            "category_id": simulators_id,
            "description": "Training simulator for 81mm mortar crew operations. Realistic weapon dynamics and scenario-based training.",
            "specifications": """• Realistic mortar operation simulation
• Scenario-based training environments
• Performance tracking and scoring
• Cost-effective alternative to live-fire training
• Weapon dynamics simulation
• Recoil simulation
• Multiple training scenarios
• Weather-independent indoor operation""",
            "images": ["/assets/mortar-firing.jpg"],
            "published": True,
            "sort_order": 2,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "name": "84RL Simulator",
            "category_id": simulators_id,
            "description": "84mm Recoilless Launcher (Carl Gustaf) training simulator. Realistic engagement training with accurate weapon handling.",
            "specifications": """• Realistic weapon handling simulation
• Recoil simulation
• Target acquisition training
• Engagement training
• Multiple scenario environments
• Performance evaluation and scoring
• Cost-effective training solution
• Indoor operation capable""",
            "images": ["/assets/target-system.jpg"],
            "published": True,
            "sort_order": 3,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
    ]
    
    await db.products.insert_many(products)
    
    # Seed Services
    print("Seeding services...")
    services = [
        {
            "id": str(uuid.uuid4()),
            "title": "Design & Development",
            "description": "End-to-end design and development of custom electronics, embedded systems, and automation solutions tailored to specific operational requirements.",
            "published": True,
            "sort_order": 1,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Integration & Testing",
            "description": "Comprehensive system integration and rigorous testing to ensure all components operate seamlessly in mission-critical environments.",
            "published": True,
            "sort_order": 2,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Repair & Maintenance",
            "description": "Expert repair and maintenance services to keep your defence and industrial systems operating at peak performance with minimal downtime.",
            "published": True,
            "sort_order": 3,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "AMC & Field Support",
            "description": "Annual Maintenance Contracts and dedicated field support teams for continuous operational readiness and rapid response.",
            "published": True,
            "sort_order": 4,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
    ]
    await db.services.insert_many(services)
    
    # Seed Clients
    print("Seeding clients...")
    clients = [
        {
            "id": str(uuid.uuid4()),
            "name": "Ministry of Defence, India",
            "logo_url": "",
            "published": True,
            "sort_order": 1,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Ordnance Factory Board",
            "logo_url": "",
            "published": True,
            "sort_order": 2,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "name": "DRDO",
            "logo_url": "",
            "published": True,
            "sort_order": 3,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Indian Army",
            "logo_url": "",
            "published": True,
            "sort_order": 4,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
    ]
    await db.clients.insert_many(clients)
    
    print("✅ Complete database seeding finished!")
    print(f"   - {len(categories)} product categories")
    print(f"   - {len(products)} products with images and specifications")
    print(f"   - {len(services)} services")
    print(f"   - {len(clients)} clients")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_complete_database())