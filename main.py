from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse , JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from supabase import create_client
from typing import Dict, Optional
from dotenv import load_dotenv
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.get("/success", response_class=HTMLResponse)
async def read_success(request: Request):
    """Serves the success page after a successful form submission."""
    return templates.TemplateResponse("success.html", {"request": request})

@app.post("/submit/")
async def submit_form(
    business_name: str = Form(...),
    outlet_name: str = Form(...),
    outlet_address: str = Form(...),
    outlet_type: str = Form(...),
    outlet_category: str = Form(...),
    ssm_number: str = Form(...),
    merchant_id: str = Form(None),
    open_time: str = Form(...),
    close_time: str = Form(...),
    delivery_radius: str = Form(None),
    service_type: str = Form(...),
    owner_name: str = Form(...),
    owner_id: str = Form(...),
    dob: str = Form(...),
    nationality: str = Form(...),
    owner_email: str = Form(...),
    owner_phone: str = Form(...),
    position: str = Form(...),
    company_email: str = Form(...),
    company_phone: str = Form(...),
    support_contact: str = Form(None),
    bank_name: str = Form(...),
    bank_account: str = Form(...),
    account_holder: str = Form(...),
    account_type: str = Form(...),
    proof_of_account: UploadFile = File(None),
    ssm_cert: UploadFile = File(...),
    ic_passport: UploadFile = File(...),
    bank_statement: UploadFile = File(None),
    halal_cert: UploadFile = File(None),
    menu_photos: list[UploadFile] = File(...),
    outlet_photos: list[UploadFile] = File(None),
    business_license: UploadFile = File(None),
    signed_agreement: UploadFile = File(...),
):
    return {"status": "success", "message": "Merchant registered successfully!"}


load_dotenv()  # Load variables from .env file

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Optional: Raise error if they are not set
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Missing Supabase configuration.")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_merchant_data_with_files(merchant_id: str) -> Optional[Dict]:
    response = supabase.table("merchant_data").select("*").eq("id", merchant_id).single().execute()
    if response.data is None:
        return None
    merchant_data = response.data
    files = supabase.storage.from_("pdfs").list()
    related = {
        f["name"].replace(f"{merchant_id}_",""):
        supabase.storage.from_("pdfs").get_public_url(f["name"])
        for f in files if f["name"].startswith(merchant_id)
    }
    merchant_data["files"] = related
    print (merchant_data)
    return merchant_data

@app.get("/api/merchant/{merchant_id}", response_class=JSONResponse)
async def fetch_merchant(merchant_id: str):
    data = get_merchant_data_with_files(merchant_id)
    if not data:
        raise HTTPException(404, "Merchant not found")
    return data

@app.get("/debug")
async def debug():
    dict = {"hi":1}
    print("The code goes through here ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZz")
    return  dict


@app.get("/print")
async def debug_print(random_string: str):
    try:
        parsed_data = json.loads(random_string)
        print("✅ PANDA_FORM_DATA_KEY contents:", json.dumps(parsed_data, indent=2))
        return {"status": "ok", "keys": list(parsed_data.keys())}
    except Exception as e:
        print("❌ Error parsing random_string:", e)
        return {"status": "error", "message": str(e)}


#############################################################################

@app.get("/food-panda", response_class=HTMLResponse)
async def serve_step1_business_info(request: Request):
    return templates.TemplateResponse("1-business-info.html", {"request": request})

@app.get("/owner-info", response_class=HTMLResponse)
async def serve_step2_owner_info(request: Request):
    return templates.TemplateResponse("2-owner-info.html", {"request": request})

@app.get("/company-info", response_class=HTMLResponse)
async def serve_step3_company_info(request: Request):
    return templates.TemplateResponse("3-company-info.html", {"request": request})

@app.get("/bank-info", response_class=HTMLResponse)
async def serve_step4_bank_info(request: Request):
    return templates.TemplateResponse("4-bank-info.html", {"request": request})

@app.get("/documents", response_class=HTMLResponse)
async def serve_step5_documents(request: Request):
    return templates.TemplateResponse("5-documents.html", {"request": request})

@app.get("/menu", response_class=HTMLResponse)
async def serve_step6_menu(request: Request):
    return templates.TemplateResponse("6-menu.html", {"request": request})

@app.get("/review", response_class=HTMLResponse)
async def serve_step7_review(request: Request):
    return templates.TemplateResponse("7-review-submit.html", {"request": request})

@app.get("/success_foodpanda", response_class=HTMLResponse)
async def serve_step7_review(request: Request):
    return templates.TemplateResponse("8-success-foodpanda.html", {"request": request})
