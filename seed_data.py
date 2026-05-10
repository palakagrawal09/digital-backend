

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid
from datetime import datetime, timezone

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

async def seed_database():
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("🌱 Starting database seeding...")
    
    # Clear existing data
    print("Clearing existing collections...")
    await db.products.delete_many({})
    await db.product_categories.delete_many({})
    await db.services.delete_many({})
    await db.clients.delete_many({})
    await db.page_content.delete_many({})
    
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
            "name": "Inspection Systems",
            "icon": "Search",
            "sort_order": 2,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Surveillance Systems",
            "icon": "Eye",
            "sort_order": 3,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Simulators",
            "icon": "Gamepad2",
            "sort_order": 4,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
    ]
    await db.product_categories.insert_many(categories)
    
    # Get category IDs
    fire_control_id = categories[0]["id"]
    inspection_id = categories[1]["id"]
    surveillance_id = categories[2]["id"]
    simulators_id = categories[3]["id"]
    
    # Seed Products
    print("Seeding products...")
    products = [
        # Fire Control Systems
        {
            "id": str(uuid.uuid4()),
            "name": "AMFDC MK-II",
            "category_id": fire_control_id,
            "description": "Automatic Mortar Fire Data Controller for 81mm Mortar - Handheld battery-operated device for infantry operations. Calculates firing data, provides digital plotter mode, and GPS integration.",
            "specifications": "• 81mm Mortar calculations\n• GPS integration\n• Digital plotter mode\n• Battery operated\n• Rugged design for field use",
            "images": [],
            "published": True,
            "sort_order": 1,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "name": "AMFDC MK-III",
            "category_id": fire_control_id,
            "description": "Advanced Automatic Mortar Fire Data Controller with enhanced plotter mode and GPS capabilities. Improved ergonomics and faster calculation speed.",
            "specifications": "• Enhanced plotter mode\n• High-precision GPS\n• Faster processing\n• Improved battery life\n• Compact design",
            "images": [],
            "published": True,
            "sort_order": 2,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "name": "TEEVRA FDC",
            "category_id": fire_control_id,
            "description": "Fire Data Computer for Company Support Weapons - Advanced ballistic computation platform for quick response fire support.",
            "specifications": "• Real-time ballistic calculations\n• Multi-weapon support\n• Digital mapping integration\n• Rugged MIL-STD design\n• Quick deployment",
            "images": [],
            "published": True,
            "sort_order": 3,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        # Inspection Systems
        {
            "id": str(uuid.uuid4()),
            "name": "GBInP-17 Universal",
            "category_id": inspection_id,
            "description": "Gun Barrel Inspection Platform for 105mm to 155mm field guns. Uses advanced optics and sensors to detect barrel wear, cracks, and defects.",
            "specifications": "• 105mm to 155mm compatibility\n• High-resolution imaging\n• Automated defect detection\n• Portable design\n• Real-time reporting",
            "images": [],
            "published": True,
            "sort_order": 1,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "name": "LCGB-HMRSV-21-XG",
            "category_id": inspection_id,
            "description": "Latest generation Gun Barrel Inspection system with AI/ML algorithms for predictive maintenance and advanced defect classification.",
            "specifications": "• AI-powered analysis\n• Predictive maintenance\n• 3D imaging\n• Cloud connectivity\n• Advanced reporting",
            "images": [],
            "published": True,
            "sort_order": 2,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        # Surveillance Systems
        {
            "id": str(uuid.uuid4()),
            "name": "FSD Flexible / INVSS",
            "category_id": surveillance_id,
            "description": "Flexible Surveillance Device for Counter-Insurgency operations. Portable, flexible camera system for covert surveillance and reconnaissance.",
            "specifications": "• Flexible camera probe\n• Night vision capable\n• Compact and portable\n• Real-time video feed\n• Rugged construction",
            "images": [],
            "published": True,
            "sort_order": 1,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        # Simulators
        {
            "id": str(uuid.uuid4()),
            "name": "ATGM SV21 Simulator",
            "category_id": simulators_id,
            "description": "Anti-Tank Guided Missile Crew Training Simulator. Realistic training platform for ATGM crew training with various scenarios.",
            "specifications": "• Realistic simulations\n• Multiple scenario modes\n• Performance tracking\n• Cost-effective training\n• Portable setup",
            "images": [],
            "published": True,
            "sort_order": 1,
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
            "title": "Annual Maintenance Contracts (AMC)",
            "description": "Comprehensive maintenance support for all our defence electronics systems. Includes preventive maintenance, calibration, and priority repair services.",
            "published": True,
            "sort_order": 1,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Repair & Refurbishment",
            "description": "Expert repair services for defence-grade electronics. Factory-trained technicians ensure equipment meets original specifications.",
            "published": True,
            "sort_order": 2,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Technical Consultancy",
            "description": "Engineering consultancy for defence electronics, industrial automation, and embedded systems. From concept to deployment.",
            "published": True,
            "sort_order": 3,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Custom Development",
            "description": "Bespoke development of defence electronics and automation solutions tailored to specific operational requirements.",
            "published": True,
            "sort_order": 4,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Training Programs",
            "description": "Comprehensive training programs for equipment operation, maintenance, and troubleshooting. Conducted by experienced engineers.",
            "published": True,
            "sort_order": 5,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
    ]
    await db.services.insert_many(services)
    
    # Seed Clients (Government organizations)
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
    
    # Seed Page Content
    print("Seeding page content...")
    page_contents = [
        {
            "id": str(uuid.uuid4()),
            "page": "homepage",
            "section": "hero",
            "content_key": "headline",
            "content_value": "Mission-Critical Defence Electronics & Automation",
            "published": True,
            "sort_order": 1,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "page": "homepage",
            "section": "hero",
            "content_key": "description",
            "content_value": "Organisation dedicated to product development. Complete solutions for Defence, Industrial Automation, Simulators & Training Systems since 1990.",
            "published": True,
            "sort_order": 2,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
    "id": str(uuid.uuid4()),
    "page": "homepage",
    "section": "hero",
    "content_key": "badge",
    "content_value": "Est. 1990 • ISO 9001:2015 Certified",
    "published": True,
    "sort_order": 3,
    "created_at": datetime.now(timezone.utc).isoformat(),
    "updated_at": datetime.now(timezone.utc).isoformat(),
},
{
    "id": str(uuid.uuid4()),
    "page": "homepage",
    "section": "about",
    "content_key": "title",
    "content_value": "Engineering Trust Through Indigenous Defence Innovation",
    "published": True,
    "sort_order": 4,
    "created_at": datetime.now(timezone.utc).isoformat(),
    "updated_at": datetime.now(timezone.utc).isoformat(),
},
{
    "id": str(uuid.uuid4()),
    "page": "homepage",
    "section": "about",
    "content_key": "description",
    "content_value": "Digital Integrator Pvt. Ltd. is dedicated to defence electronics, industrial automation, simulators, and training systems with decades of engineering experience.",
    "published": True,
    "sort_order": 5,
    "created_at": datetime.now(timezone.utc).isoformat(),
    "updated_at": datetime.now(timezone.utc).isoformat(),
},
{
    "id": str(uuid.uuid4()),
    "page": "homepage",
    "section": "capabilities",
    "content_key": "title",
    "content_value": "Our Core Capabilities",
    "published": True,
    "sort_order": 6,
    "created_at": datetime.now(timezone.utc).isoformat(),
    "updated_at": datetime.now(timezone.utc).isoformat(),
},
{
    "id": str(uuid.uuid4()),
    "page": "homepage",
    "section": "contact_cta",
    "content_key": "title",
    "content_value": "Ready to Discuss Your Requirement?",
    "published": True,
    "sort_order": 7,
    "created_at": datetime.now(timezone.utc).isoformat(),
    "updated_at": datetime.now(timezone.utc).isoformat(),
},
{
    "id": str(uuid.uuid4()),
    "page": "homepage",
    "section": "contact_cta",
    "content_key": "description",
    "content_value": "Connect with our team for product enquiries, support, repair requests, or custom defence electronics solutions.",
    "published": True,
    "sort_order": 8,
    "created_at": datetime.now(timezone.utc).isoformat(),
    "updated_at": datetime.now(timezone.utc).isoformat(),
},
    ]
    await db.page_content.insert_many(page_contents)
    
    print("✅ Database seeding completed successfully!")
    print(f"   - {len(categories)} product categories")
    print(f"   - {len(products)} products")
    print(f"   - {len(services)} services")
    print(f"   - {len(clients)} clients")
    print(f"   - {len(page_contents)} page content entries")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
