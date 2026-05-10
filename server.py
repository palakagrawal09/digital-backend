from fastapi import FastAPI, APIRouter, HTTPException, Depends, UploadFile, File, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone, timedelta
import jwt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
import shutil
from fastapi.staticfiles import StaticFiles

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# JWT Configuration
JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key')
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

# Admin Credentials
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')

# Email Configuration
USE_SIMULATED_OTP = os.environ.get('USE_SIMULATED_OTP', 'true').lower() == 'true'
SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_EMAIL = os.environ.get('SMTP_EMAIL')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')

# Create the main app
app = FastAPI()
api_router = APIRouter(prefix="/api")
security = HTTPBearer()

uploads_dir = Path("uploads")
uploads_dir.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== MODELS ====================

class HomePageContent(BaseModel):
    id: Optional[str] = None
    section: str
    content: dict
    published: bool = True

class AdminLoginRequest(BaseModel):
    username: str
    password: str

class AdminLoginResponse(BaseModel):
    token: str
    message: str

class OTPSendRequest(BaseModel):
    email: EmailStr
    form_type: str = "enquiry"

class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp_code: str

class AboutCategory(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    slug: str = ""
    description: str = ""
    sort_order: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AboutSection(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    category_id: str
    description: str = ""
    image_url: str = ""
    designation: str = ""
    published: bool = True
    sort_order: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class EnquirySubmission(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    phone: str
    organization: Optional[str] = ""
    subject: str
    product_interest: str
    message: str
    read: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class RepairSubmission(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    phone: str
    organization: Optional[str] = ""
    equipment_category: str
    equipment_variant: Optional[str] = ""
    serial_number: Optional[str] = ""
    issue_description: str
    image_urls: List[str] = []
    read: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class PageContent(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    page: str
    section: str
    content_key: str
    content_value: str = ""
    published: bool = True
    sort_order: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Product(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    category_id: str
    description: str = ""
    specifications: str = ""
    images: List[str] = []
    published: bool = True
    sort_order: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ProductCategory(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    icon: str = ""
    sort_order: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Service(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str = ""
    published: bool = True
    sort_order: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Client(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    logo_url: str = ""
    published: bool = True
    sort_order: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class NewsArticle(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    content: str = ""
    image_url: str = ""
    published: bool = True
    published_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Employee(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    designation: str = ""
    department: str = ""
    email: str = ""
    phone: str = ""
    status: str = "active"
    join_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class OfficeInfo(BaseModel):
    title: str
    address_line_1: str
    address_line_2: str
    address_line_3: str


class StatutoryInfo(BaseModel):
    cin: str
    gst_no: str
    registration_no: str
    roc: str


class CTAInfo(BaseModel):
    title: str
    description: str
    button_text: str


class ContactPageSchema(BaseModel):
    registered_office: OfficeInfo
    corporate_office: OfficeInfo
    email: str
    phone: str
    statutory_info: StatutoryInfo
    map_embed_url: str
    cta: CTAInfo
    certifications: List[str] = []
default_contact_data = {
    "registered_office": {
        "title": "Registered Office",
        "address_line_1": "46 Electronic Complex",
        "address_line_2": "Pardeshipura, Indore",
        "address_line_3": "Madhya Pradesh - 452010, India"
    },
    "corporate_office": {
        "title": "Corporate Office",
        "address_line_1": "46 Electronic Complex",
        "address_line_2": "Pardeshipura, Indore",
        "address_line_3": "Madhya Pradesh - 452010, India"
    },
    "email": "info@diplindia.com",
    "phone": "+91-731-4255200",
    "statutory_info": {
        "cin": "U31909MP1997PTC012011",
        "gst_no": "23AAACD9928P1Z5",
        "registration_no": "12011",
        "roc": "Gwalior"
    },
    "map_embed_url": "https://www.google.com/maps/embed?pb=...",
    "cta": {
        "title": "Need Assistance?",
        "description": "For product enquiries, support requirements, or repair requests, please use our dedicated submission form.",
        "button_text": "Submit Enquiry / Repair Request"
    },
    "certifications": ["ISO 9001:2015", "Defence Grade", "GeM Registered"]
}




# ==================== HELPER FUNCTIONS ====================

def generate_otp() -> str:
    """Generate 6-digit OTP"""
    return "".join(random.choices(string.digits, k=6))


async def send_email_otp(email: str, otp_code: str) -> bool:
    """
    Development-safe OTP sender.
    - If USE_SIMULATED_OTP = true, OTP terminal me print hoga
    - Otherwise SMTP use hoga
    """
    try:
        if USE_SIMULATED_OTP:
            logger.info("=" * 80)
            logger.info("📧 SIMULATED OTP EMAIL")
            logger.info(f"To: {email}")
            logger.info(f"OTP Code: {otp_code}")
            logger.info("This code will expire in 10 minutes")
            logger.info("=" * 80)
            print(f"\n🔐 OTP for {email}: {otp_code}\n")
            return True

        msg = MIMEMultipart()
        msg["From"] = SMTP_EMAIL
        msg["To"] = email
        msg["Subject"] = "Email Verification - Digital Integrator Pvt Ltd"

        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2 style="color: #1a1a1a;">Email Verification Code</h2>
                <p>Your verification code is:</p>
                <h1 style="color: #D4AF37; font-size: 32px; letter-spacing: 5px;">{otp_code}</h1>
                <p>This code will expire in 10 minutes.</p>
                <p>If you didn't request this code, please ignore this email.</p>
                <hr>
                <p style="color: #666; font-size: 12px;">
                    Digital Integrator Private Limited<br>
                    46-A, Electronic Complex Pardeshipura, Indore, MP - 452001
                </p>
            </body>
        </html>
        """

        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)

        logger.info(f"OTP sent successfully to {email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send OTP email to {email}: {str(e)}")
        return False


def send_custom_email(to_email: str, subject: str, html_body: str) -> bool:
    """
    For acknowledgement / team notification emails.
    Failure ko caller handle karega.
    """
    try:
        if USE_SIMULATED_OTP:
            logger.info("=" * 80)
            logger.info("📧 SIMULATED CUSTOM EMAIL")
            logger.info(f"To: {to_email}")
            logger.info(f"Subject: {subject}")
            logger.info("Email body generated successfully")
            logger.info("=" * 80)
            print(f"\n📨 Simulated email to {to_email}\nSubject: {subject}\n")
            return True

        msg = MIMEMultipart()
        msg["From"] = SMTP_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(html_body, "html"))

        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()

        logger.info(f"Email sent to {to_email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return False


def enquiry_ack_email(enquiry):
    return f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <h2>Thank you for contacting us</h2>
        <p>Dear {enquiry.name},</p>
        <p>Your enquiry has been received successfully.</p>
        <p>We will get back to you shortly.</p>
        <br />
        <p><b>Digital Integrator Pvt Ltd</b></p>
      </body>
    </html>
    """


def enquiry_team_email(enquiry):
    return f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <h2>New Enquiry Received</h2>
        <p><b>Name:</b> {enquiry.name}</p>
        <p><b>Email:</b> {enquiry.email}</p>
        <p><b>Phone:</b> {enquiry.phone}</p>
        <p><b>Organization:</b> {enquiry.organization}</p>
        <p><b>Subject:</b> {enquiry.subject}</p>
        <p><b>Product:</b> {enquiry.product_interest}</p>
        <p><b>Message:</b><br>{enquiry.message}</p>
      </body>
    </html>
    """


def repair_ack_email(repair):
    return f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <h2>Repair Request Received</h2>
        <p>Dear {repair.name},</p>
        <p>Your repair request has been received successfully.</p>
        <p>Our team will review it and contact you shortly.</p>
        <br />
        <p><b>Digital Integrator Pvt Ltd</b></p>
      </body>
    </html>
    """


def repair_team_email(repair):
    return f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <h2>New Repair Request Received</h2>
        <p><b>Name:</b> {repair.name}</p>
        <p><b>Email:</b> {repair.email}</p>
        <p><b>Phone:</b> {repair.phone}</p>
        <p><b>Organization:</b> {repair.organization}</p>
        <p><b>Equipment Category:</b> {repair.equipment_category}</p>
        <p><b>Equipment Variant:</b> {repair.equipment_variant}</p>
        <p><b>Serial Number:</b> {repair.serial_number}</p>
        <p><b>Issue:</b><br>{repair.issue_description}</p>
      </body>
    </html>
    """


def create_jwt_token(username: str) -> str:
    """Create JWT token"""
    payload = {
        "username": username,
        "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verify JWT token"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def serialize_datetime(doc: dict) -> dict:
    """Convert datetime objects to ISO strings"""
    for key, value in doc.items():
        if isinstance(value, datetime):
            doc[key] = value.isoformat()
    return doc


def serialize_datetime(doc: dict) -> dict:
    """Convert datetime objects to ISO strings"""
    for key, value in doc.items():
        if isinstance(value, datetime):
            doc[key] = value.isoformat()
    return doc
# ===================== HOME PAGE ===========================
@app.get("/api/home")
async def get_home():
    data = await db.home.find({"published": True}).to_list(100)
    return data
@app.post("/api/home")
async def create_home(content: HomePageContent):
    content_dict = content.dict()
    content_dict["id"] = str(uuid.uuid4())
    await db.home.insert_one(content_dict)
    return content_dict
@app.put("/api/home/{id}")
async def update_home(id: str, content: HomePageContent):
    await db.home.update_one(
        {"id": id},
        {"$set": content.dict()}
    )
    return {"message": "updated"}
@app.delete("/api/home/{id}")
async def delete_home(id: str):
    await db.home.delete_one({"id": id})
    return {"message": "deleted"}
# ==================== ADMIN AUTH ROUTES ====================

@api_router.post("/admin/login", response_model=AdminLoginResponse)
async def admin_login(request: AdminLoginRequest):
    """Admin login endpoint"""
    if request.username == ADMIN_USERNAME and request.password == ADMIN_PASSWORD:
        token = create_jwt_token(request.username)
        return AdminLoginResponse(token=token, message="Login successful")
    raise HTTPException(status_code=401, detail="Invalid credentials")

@api_router.get("/admin/verify")
async def verify_admin(payload: dict = Depends(verify_jwt_token)):
    """Verify admin token"""
    return {"valid": True, "username": payload['username']}


# ==================== OTP ROUTES ====================


@api_router.post("/otp/send")
async def send_otp(request: OTPSendRequest):
    """Send OTP to email"""
    try:
        otp_code = generate_otp()
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)

        await db.otp_verifications.delete_many({"email": request.email})

        otp_doc = {
            "id": str(uuid.uuid4()),
            "email": request.email,
            "otp_code": otp_code,
            "form_type": request.form_type,
            "verified": False,
            "expires_at": expires_at.isoformat(),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        await db.otp_verifications.insert_one(otp_doc)

        email_sent = await send_email_otp(request.email, otp_code)

        if not email_sent:
            raise HTTPException(
                status_code=500,
                detail="Failed to send email. Please check SMTP configuration."
            )

        logger.info(f"OTP generated for {request.email}: {otp_code}")
        return {"message": "OTP sent successfully", "email": request.email}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending OTP: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/otp/verify")
async def verify_otp(request: OTPVerifyRequest):
    """Verify OTP code"""
    try:
        otp_doc = await db.otp_verifications.find_one({
            "email": request.email,
            "otp_code": request.otp_code,
            "verified": False
        })

        if not otp_doc:
            raise HTTPException(status_code=400, detail="Invalid OTP code")

        expires_at = datetime.fromisoformat(otp_doc["expires_at"])
        if datetime.now(timezone.utc) > expires_at:
            raise HTTPException(status_code=400, detail="OTP has expired")

        await db.otp_verifications.update_one(
            {"_id": otp_doc["_id"]},
            {"$set": {"verified": True}}
        )

        return {"message": "Email verified successfully", "verified": True}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error verifying OTP: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== ENQUIRY & REPAIR ROUTES ====================

@api_router.post("/enquiry/submit")
async def submit_enquiry(enquiry: EnquirySubmission):
    """Submit enquiry form"""
    try:
        verified = await db.otp_verifications.find_one({
            "email": enquiry.email,
            "verified": True
        })

        if not verified:
            raise HTTPException(status_code=400, detail="Email not verified")

        doc = enquiry.model_dump()
        doc["created_at"] = doc["created_at"].isoformat()
        await db.contact_submissions.insert_one(doc)

        try:
            send_custom_email(
                to_email=enquiry.email,
                subject="We received your enquiry",
                html_body=enquiry_ack_email(enquiry)
            )
        except Exception as e:
            logger.error(f"Acknowledgement email failed: {str(e)}")

        try:
            send_custom_email(
                to_email=SMTP_EMAIL,
                subject="New enquiry received",
                html_body=enquiry_team_email(enquiry)
            )
        except Exception as e:
            logger.error(f"Team notification email failed: {str(e)}")

        logger.info(f"Enquiry submitted by {enquiry.email}")
        return {"message": "Enquiry submitted successfully", "id": enquiry.id}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting enquiry: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/repair/submit")
async def submit_repair(repair: RepairSubmission):
    """Submit repair request"""
    try:
        verified = await db.otp_verifications.find_one({
            "email": repair.email,
            "verified": True
        })

        if not verified:
            raise HTTPException(status_code=400, detail="Email not verified")

        doc = repair.model_dump()
        doc["created_at"] = doc["created_at"].isoformat()
        await db.repair_submissions.insert_one(doc)

        try:
            send_custom_email(
                to_email=repair.email,
                subject="We received your repair request",
                html_body=repair_ack_email(repair)
            )
        except Exception as e:
            logger.error(f"Repair acknowledgement email failed: {str(e)}")

        try:
            send_custom_email(
                to_email=SMTP_EMAIL,
                subject="New repair request received",
                html_body=repair_team_email(repair)
            )
        except Exception as e:
            logger.error(f"Repair team notification email failed: {str(e)}")

        logger.info(f"Repair request submitted by {repair.email}")
        return {"message": "Repair request submitted successfully", "id": repair.id}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting repair: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/enquiries")
async def get_enquiries(payload: dict = Depends(verify_jwt_token)):
    """Get all enquiries (Admin only)"""
    enquiries = await db.contact_submissions.find({}, {"_id": 0}).sort("created_at", -1).to_list(1000)
    for enq in enquiries:
        if isinstance(enq.get("created_at"), str):
            enq["created_at"] = datetime.fromisoformat(enq["created_at"]).isoformat()
    return enquiries


@api_router.get("/repairs")
async def get_repairs(payload: dict = Depends(verify_jwt_token)):
    """Get all repair requests (Admin only)"""
    repairs = await db.repair_submissions.find({}, {"_id": 0}).sort("created_at", -1).to_list(1000)
    for rep in repairs:
        if isinstance(rep.get("created_at"), str):
            rep["created_at"] = datetime.fromisoformat(rep["created_at"]).isoformat()
    return repairs

# ==================== FILE UPLOAD ====================

@api_router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload file (images for repair forms)"""
    try:
        # Create uploads directory if not exists
        upload_dir = ROOT_DIR/"uploads"
        upload_dir.mkdir(exist_ok=True)
        
        # Generate unique filename
        file_ext = Path(file.filename).suffix
        filename = f"{uuid.uuid4()}{file_ext}"
        file_path = upload_dir / filename
        
        # Save file
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Return file URL
        file_url = f"/uploads/{filename}"
        return {"url": file_url, "filename": filename}
    
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== PAGE CONTENT ROUTES ====================

@api_router.get("/page-content")
async def get_page_content(page: Optional[str] = None):
    """Get page content"""
    query = {"published": True}
    if page:
        query["page"] = page
    
    content = await db.page_content.find(query, {"_id": 0}).sort("sort_order", 1).to_list(1000)
    return content

@api_router.put("/page-content/{content_id}")
async def update_page_content(content_id: str, updates: Dict[str, Any], payload: dict = Depends(verify_jwt_token)):
    """Update page content (Admin only)"""
    updates['updated_at'] = datetime.now(timezone.utc).isoformat()
    result = await db.page_content.update_one({"id": content_id}, {"$set": updates})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Content not found")
    return {"message": "Content updated successfully"}

@api_router.post("/page-content")
async def create_page_content(content: PageContent, payload: dict = Depends(verify_jwt_token)):
    """Create page content (Admin only)"""
    doc = content.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc['updated_at'] = doc['updated_at'].isoformat()
    await db.page_content.insert_one(doc)
    return {"message": "Content created successfully", "id": content.id}

# ==================== PRODUCT ROUTES ====================

@api_router.get("/products")
async def get_products(category_id: Optional[str] = None, published: bool = True):
    """Get all products"""
    query = {"published": published} if published else {}
    if category_id:
        query["category_id"] = category_id
    
    products = await db.products.find(query, {"_id": 0}).sort("sort_order", 1).to_list(1000)
    return products

@api_router.get("/products/{product_id}")
async def get_product(product_id: str):
    """Get single product"""
    product = await db.products.find_one({"id": product_id}, {"_id": 0})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@api_router.post("/products")
async def create_product(product: Product, payload: dict = Depends(verify_jwt_token)):
    """Create product (Admin only)"""
    doc = product.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc['updated_at'] = doc['updated_at'].isoformat()
    await db.products.insert_one(doc)
    return {"message": "Product created successfully", "id": product.id}

@api_router.put("/products/{product_id}")
async def update_product(product_id: str, updates: Dict[str, Any], payload: dict = Depends(verify_jwt_token)):
    """Update product (Admin only)"""
    updates['updated_at'] = datetime.now(timezone.utc).isoformat()
    result = await db.products.update_one({"id": product_id}, {"$set": updates})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product updated successfully"}

@api_router.delete("/products/{product_id}")
async def delete_product(product_id: str, payload: dict = Depends(verify_jwt_token)):
    """Delete product (Admin only)"""
    result = await db.products.delete_one({"id": product_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

# ==================== PRODUCT CATEGORY ROUTES ====================


@api_router.get("/product-categories")
async def get_product_categories():
    """Get all product categories"""
    categories = await db.product_categories.find({}, {"_id": 0}).sort("sort_order", 1).to_list(100)
    return categories

@api_router.post("/product-categories")
async def create_product_category(category: ProductCategory, payload: dict = Depends(verify_jwt_token)):
    """Create product category (Admin only)"""
    doc = category.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc['updated_at'] = doc['updated_at'].isoformat()
    await db.product_categories.insert_one(doc)
    return {"message": "Category created successfully", "id": category.id}

@api_router.put("/product-categories/{category_id}")
async def update_product_category(category_id: str, updates: Dict[str, Any], payload: dict = Depends(verify_jwt_token)):
    """Update product category (Admin only)"""
    updates['updated_at'] = datetime.now(timezone.utc).isoformat()
    result = await db.product_categories.update_one({"id": category_id}, {"$set": updates})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category updated successfully"}

@api_router.delete("/product-categories/{category_id}")
async def delete_product_category(category_id: str, payload: dict = Depends(verify_jwt_token)):
    """Delete product category (Admin only)"""
    result = await db.product_categories.delete_one({"id": category_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}

# ==================== SERVICE ROUTES ====================

@api_router.get("/services")
async def get_services(published: bool = True):
    """Get all services"""
    query = {"published": published} if published else {}
    services = await db.services.find(query, {"_id": 0}).sort("sort_order", 1).to_list(1000)
    return services

@api_router.post("/services")
async def create_service(service: Service, payload: dict = Depends(verify_jwt_token)):
    """Create service (Admin only)"""
    doc = service.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc['updated_at'] = doc['updated_at'].isoformat()
    await db.services.insert_one(doc)
    return {"message": "Service created successfully", "id": service.id}

@api_router.put("/services/{service_id}")
async def update_service(service_id: str, updates: Dict[str, Any], payload: dict = Depends(verify_jwt_token)):
    """Update service (Admin only)"""
    updates['updated_at'] = datetime.now(timezone.utc).isoformat()
    result = await db.services.update_one({"id": service_id}, {"$set": updates})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"message": "Service updated successfully"}

@api_router.delete("/services/{service_id}")
async def delete_service(service_id: str, payload: dict = Depends(verify_jwt_token)):
    """Delete service (Admin only)"""
    result = await db.services.delete_one({"id": service_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"message": "Service deleted successfully"}

# ==================== CLIENT ROUTES ====================

@api_router.get("/clients")
async def get_clients(published: bool = True):
    """Get all clients"""
    query = {"published": published} if published else {}
    clients = await db.clients.find(query, {"_id": 0}).sort("sort_order", 1).to_list(1000)
    return clients

@api_router.post("/clients")
async def create_client(client: Client, payload: dict = Depends(verify_jwt_token)):
    """Create client (Admin only)"""
    doc = client.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc['updated_at'] = doc['updated_at'].isoformat()
    await db.clients.insert_one(doc)
    return {"message": "Client created successfully", "id": client.id}

@api_router.put("/clients/{client_id}")
async def update_client(client_id: str, updates: Dict[str, Any], payload: dict = Depends(verify_jwt_token)):
    """Update client (Admin only)"""
    updates['updated_at'] = datetime.now(timezone.utc).isoformat()
    result = await db.clients.update_one({"id": client_id}, {"$set": updates})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"message": "Client updated successfully"}

@api_router.delete("/clients/{client_id}")
async def delete_client(client_id: str, payload: dict = Depends(verify_jwt_token)):
    """Delete client (Admin only)"""
    result = await db.clients.delete_one({"id": client_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"message": "Client deleted successfully"}

# =================== ABOUT CATEGORY ROUTES =====================

@api_router.get("/about-categories")
async def get_about_categories():
    """Get all about categories"""
    categories = await db.about_categories.find({}, {"_id": 0}).sort("sort_order", 1).to_list(100)
    return categories


@api_router.get("/about-categories/{category_id}")
async def get_about_category(category_id: str):
    """Get single about category"""
    category = await db.about_categories.find_one({"id": category_id}, {"_id": 0})
    if not category:
        raise HTTPException(status_code=404, detail="About category not found")
    return category


@api_router.post("/about-categories")
async def create_about_category(
    category: AboutCategory,
    payload: dict = Depends(verify_jwt_token)
):
    """Create about category (Admin only)"""
    doc = category.model_dump()

    if not doc["slug"]:
        doc["slug"] = doc["name"].strip().lower().replace(" ", "-")

    doc["created_at"] = doc["created_at"].isoformat()
    doc["updated_at"] = doc["updated_at"].isoformat()

    await db.about_categories.insert_one(doc)
    return {"message": "About category created successfully", "id": category.id}


@api_router.put("/about-categories/{category_id}")
async def update_about_category(
    category_id: str,
    updates: Dict[str, Any],
    payload: dict = Depends(verify_jwt_token)
):
    """Update about category (Admin only)"""
    updates["updated_at"] = datetime.now(timezone.utc).isoformat()

    if "name" in updates and "slug" not in updates:
        updates["slug"] = updates["name"].strip().lower().replace(" ", "-")

    result = await db.about_categories.update_one({"id": category_id}, {"$set": updates})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="About category not found")

    return {"message": "About category updated successfully"}


@api_router.delete("/about-categories/{category_id}")
async def delete_about_category(
    category_id: str,
    payload: dict = Depends(verify_jwt_token)
):
    """Delete about category (Admin only)"""
    result = await db.about_categories.delete_one({"id": category_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="About category not found")

    await db.about_sections.delete_many({"category_id": category_id})

    return {"message": "About category and linked sections deleted successfully"}


# ==================== ABOUT SECTION ROUTES ====================

@api_router.get("/about-sections")
async def get_about_sections(
    category_id: Optional[str] = None,
    published: bool = True
):
    """Get all about sections"""
    query = {"published": published}

    if category_id:
        query["category_id"] = category_id

    sections = await db.about_sections.find(query, {"_id": 0}).sort("sort_order", 1).to_list(1000)
    return sections


@api_router.get("/about-sections/{section_id}")
async def get_about_section(section_id: str):
    """Get single about section"""
    section = await db.about_sections.find_one({"id": section_id}, {"_id": 0})
    if not section:
        raise HTTPException(status_code=404, detail="About section not found")
    return section


@api_router.post("/about-sections")
async def create_about_section(
    section: AboutSection,
    payload: dict = Depends(verify_jwt_token)
):
    """Create about section (Admin only)"""
    category = await db.about_categories.find_one({"id": section.category_id})
    if not category:
        raise HTTPException(status_code=404, detail="Linked about category not found")

    doc = section.model_dump()
    doc["created_at"] = doc["created_at"].isoformat()
    doc["updated_at"] = doc["updated_at"].isoformat()

    await db.about_sections.insert_one(doc)
    return {"message": "About section created successfully", "id": section.id}


@api_router.put("/about-sections/{section_id}")
async def update_about_section(
    section_id: str,
    updates: Dict[str, Any],
    payload: dict = Depends(verify_jwt_token)
):
    """Update about section (Admin only)"""
    if "category_id" in updates:
        category = await db.about_categories.find_one({"id": updates["category_id"]})
        if not category:
            raise HTTPException(status_code=404, detail="Linked about category not found")

    updates["updated_at"] = datetime.now(timezone.utc).isoformat()

    result = await db.about_sections.update_one({"id": section_id}, {"$set": updates})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="About section not found")

    return {"message": "About section updated successfully"}


@api_router.delete("/about-sections/{section_id}")
async def delete_about_section(
    section_id: str,
    payload: dict = Depends(verify_jwt_token)
):
    """Delete about section (Admin only)"""
    result = await db.about_sections.delete_one({"id": section_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="About section not found")

    return {"message": "About section deleted successfully"}

# ==================== NEWS ROUTES ====================

@api_router.get("/news")
async def get_news(published: bool = True):
    """Get all news articles"""
    query = {"published": published} if published else {}
    news = await db.news_articles.find(query, {"_id": 0}).sort("published_at", -1).to_list(1000)
    return news

@api_router.post("/news")
async def create_news(article: NewsArticle, payload: dict = Depends(verify_jwt_token)):
    """Create news article (Admin only)"""
    doc = article.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc['updated_at'] = doc['updated_at'].isoformat()
    if doc.get('published_at'):
        doc['published_at'] = doc['published_at'].isoformat()
    await db.news_articles.insert_one(doc)
    return {"message": "News article created successfully", "id": article.id}

@api_router.put("/news/{news_id}")
async def update_news(news_id: str, updates: Dict[str, Any], payload: dict = Depends(verify_jwt_token)):
    """Update news article (Admin only)"""
    updates['updated_at'] = datetime.now(timezone.utc).isoformat()
    result = await db.news_articles.update_one({"id": news_id}, {"$set": updates})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="News article not found")
    return {"message": "News article updated successfully"}

@api_router.delete("/news/{news_id}")
async def delete_news(news_id: str, payload: dict = Depends(verify_jwt_token)):
    """Delete news article (Admin only)"""
    result = await db.news_articles.delete_one({"id": news_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="News article not found")
    return {"message": "News article deleted successfully"}

# ==================== EMPLOYEE ROUTES ====================

@api_router.get("/employees")
async def get_employees(status: Optional[str] = None):
    """Get all employees"""
    query = {}
    if status:
        query["status"] = status
    employees = await db.employees.find(query, {"_id": 0}).sort("name", 1).to_list(1000)
    return employees

@api_router.post("/employees")
async def create_employee(employee: Employee, payload: dict = Depends(verify_jwt_token)):
    """Create employee (Admin only)"""
    doc = employee.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc['updated_at'] = doc['updated_at'].isoformat()
    if doc.get('join_date'):
        doc['join_date'] = doc['join_date'].isoformat()
    await db.employees.insert_one(doc)
    return {"message": "Employee created successfully", "id": employee.id}

@api_router.put("/employees/{employee_id}")
async def update_employee(employee_id: str, updates: Dict[str, Any], payload: dict = Depends(verify_jwt_token)):
    """Update employee (Admin only)"""
    updates['updated_at'] = datetime.now(timezone.utc).isoformat()
    result = await db.employees.update_one({"id": employee_id}, {"$set": updates})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee updated successfully"}

@api_router.delete("/employees/{employee_id}")
async def delete_employee(employee_id: str, payload: dict = Depends(verify_jwt_token)):
    """Delete employee (Admin only)"""
    result = await db.employees.delete_one({"id": employee_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}
# =================== CONTACT ROUTES ======================
@app.get("/api/contact", response_model=ContactPageSchema)
async def get_contact_page():
    contact_doc = await db.contact_page.find_one({})

    if not contact_doc:
        await db.contact_page.insert_one(default_contact_data)
        contact_doc = await db.contact_page.find_one({})

    contact_doc.pop("_id", None)
    return contact_doc
@app.put("/api/contact")
async def update_contact_page(payload: ContactPageSchema):
    existing = await db.contact_page.find_one({})

    if existing:
        await db.contact_page.update_one(
            {"_id": existing["_id"]},
            {"$set": payload.dict()}
        )
    else:
        await db.contact_page.insert_one(payload.dict())

    return {"message": "Contact page updated successfully"}

# ==================== BASIC ROUTES ====================

@api_router.get("/")
async def root():
    return {"message": "Digital Integrator CMS API", "version": "1.0.0"}

@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}

# Include router in app
app.include_router(api_router)

# CORS Middleware
# CORS Middleware
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

extra_origins = os.environ.get("CORS_ORIGINS", "")
if extra_origins:
    allowed_origins.extend(
        [origin.strip() for origin in extra_origins.split(",") if origin.strip()]
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def seed_about_categories():
    default_categories = [
        {
            "id": str(uuid.uuid4()),
            "name": "Director",
            "slug": "director",
            "description": "Director section",
            "sort_order": 1,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Company Overview",
            "slug": "company-overview",
            "description": "Company overview section",
            "sort_order": 2,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Advisory",
            "slug": "advisory",
            "description": "Advisory section",
            "sort_order": 3,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
    ]

    for category in default_categories:
        existing = await db.about_categories.find_one({"slug": category["slug"]})
        if not existing:
            await db.about_categories.insert_one(category)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
