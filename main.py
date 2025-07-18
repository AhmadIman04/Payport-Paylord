from fastapi import FastAPI, Form, UploadFile, File, HTTPException, Query
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
from pydantic import BaseModel
import google.generativeai as genai

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
# Set your Gemini API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key = GOOGLE_API_KEY)

# Load the Gemini 2.0 Flash model
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

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
    

@app.get("/get_owner")
def read_owner_name(merchant_id: str):
    owner_name = get_owner_name(merchant_id)
    if owner_name is None:
        raise HTTPException(status_code=404, detail="Merchant not found")
    return {"merchant_id": merchant_id, "owner_name": owner_name}


# Assuming `supabase` is already initialized
def get_owner_name(merchant_id: str) -> Optional[str]:
    response = supabase.table("merchant_data").select("owner_name").eq("id", merchant_id).single().execute()
    if response.data is None:
        return None
    return response.data.get("owner_name")

@app.get("/get_personal_info")
def get_personal_info(merchant_id: str = Query(..., description="The merchant ID to look up")):
    fields = "owner_name, owner_id, dob, nationality, owner_email, owner_phone"
    response = supabase.table("merchant_data").select(fields).eq("id", merchant_id).single().execute()
    
    if response.data is None:
        raise HTTPException(status_code=404, detail="Merchant not found")
    
    return {
        "merchant_id": merchant_id,
        "personal_info": response.data
    }

@app.get("/get_business_info")
def get_business_info(merchant_id: str = Query(..., description="The merchant ID to look up")):
    fields = (
        "business_name, outlet_name, outlet_address, outlet_type, outlet_category, "
        "ssm_number, merchant_id, open_time, close_time, delivery_radius, service_type"
    )
    response = supabase.table("merchant_data").select(fields).eq("id", merchant_id).single().execute()
    
    if response.data is None:
        raise HTTPException(status_code=404, detail="Merchant not found")
    
    return {
        "merchant_id": merchant_id,
        "business_info": response.data
    }

@app.get("/get_company_contact")
def get_company_contact(merchant_id: str = Query(..., description="The merchant ID to look up")):
    fields = "company_email, company_phone, support_contact"
    response = supabase.table("merchant_data").select(fields).eq("id", merchant_id).single().execute()
    
    if response.data is None:
        raise HTTPException(status_code=404, detail="Merchant not found")
    
    return {
        "merchant_id": merchant_id,
        "company_contact": response.data
    }

@app.get("/get_bank_info")
def get_bank_info(merchant_id: str = Query(..., description="The merchant ID to look up")):
    # Step 1: Fetch bank-related data
    fields = "bank_name, bank_account, account_holder, account_type"
    response = supabase.table("merchant_data").select(fields).eq("id", merchant_id).single().execute()
    
    if response.data is None:
        raise HTTPException(status_code=404, detail="Merchant not found")

    bank_info = response.data

    # Step 2: Generate public URL for the bank statement file
    file_path = f"{merchant_id}_proof_of_account.pdf"
    try:
        file_url_response = supabase.storage.from_("pdfs").get_public_url(file_path)
        bank_info["proof_of_account_url"] = file_url_response
    except Exception:
        bank_info["proof_of_account_url"] = None  # Fallback in case the file does not exist

    return {
        "merchant_id": merchant_id,
        "bank_info": bank_info
    }

@app.get("/get_documents")
def get_documents(merchant_id: str = Query(..., description="The merchant ID to look up documents for")):
    file_names = {
        "business_license": f"{merchant_id}_business_license.pdf",
        "halal_cert": f"{merchant_id}_halal_cert.pdf",
        "ic_passport": f"{merchant_id}_ic_passport.pdf",
        "menu_photos": f"{merchant_id}_menu_photos.pdf",
        "outlet_photos": f"{merchant_id}_outlet_photos.pdf",
        "signed_agreement": f"{merchant_id}_signed_agreement.pdf",
        "ssm_cert": f"{merchant_id}_ssm_cert.pdf",
        "bank_statement": f"{merchant_id}_bank_statement.pdf"
    }

    document_urls = {}
    for doc_type, file_name in file_names.items():
        try:
            public_url = supabase.storage.from_("pdfs").get_public_url(file_name)
            document_urls[doc_type] = public_url
        except Exception:
            document_urls[doc_type] = None  # File missing or permission issue

    return {
        "merchant_id": merchant_id,
        "documents": document_urls
    }

@app.get("/get_json_menu")
def get_json_menu(merchant_id: str = Query(..., description="The merchant ID to fetch menu JSON for")):
    file_path = f"{merchant_id}_json_menu.json"

    try:
        # Download file content from Supabase storage
        response = supabase.storage.from_("pdfs").download(file_path)
        file_bytes = response
        json_data = json.loads(file_bytes.decode("utf-8"))
    except Exception:
        raise HTTPException(status_code=404, detail="JSON menu file not found or invalid")

    return {
        "merchant_id": merchant_id,
        "menu": json_data
    }

class PromptRequest(BaseModel):
    prompt: str

@app.post("/chat")
async def generate_text(request: PromptRequest):
    try:
        with open("chatbot_info.txt", "r", encoding="utf-8") as file:
            contents = file.read()
        actual_prompt = f"""
        Persona : You are a chatbot that is build for an app that is built to guide merchants in malaysia to onboard and digitalize their business
        easier, there fore you will give some kind of information and based on that info you will need to answer the user query
        Information : {contents}
        User Query :{request.prompt}

        now based on the user query  and information provided give a simple to understand answer
        """
        response = model.generate_content(actual_prompt)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

@app.get("/phone-home", response_class=HTMLResponse)
async def serve_phone_home(request: Request):
    return templates.TemplateResponse("phone_home.html", {"request": request})

@app.get("/phone-bi", response_class=HTMLResponse)
async def serve_phone_bi(request: Request):
    return templates.TemplateResponse("phone_bi.html", {"request": request})

@app.get("/phone-pi", response_class=HTMLResponse)
async def serve_phone_pi(request: Request):
    return templates.TemplateResponse("phone_pi.html", {"request": request})

@app.get("/phone-ci", response_class=HTMLResponse)
async def serve_phone_ci(request: Request):
    return templates.TemplateResponse("phone_ci.html", {"request": request})

@app.get("/phone-bank", response_class=HTMLResponse)
async def serve_phone_bank(request: Request):
    return templates.TemplateResponse("phone_bank.html", {"request": request})

@app.get("/phone-documents", response_class=HTMLResponse)
async def serve_phone_documents(request: Request):
    return templates.TemplateResponse("phone_documents.html", {"request": request})

@app.get("/phone-food-menu", response_class=HTMLResponse)
async def serve_phone_food_menu(request: Request):
    return templates.TemplateResponse("phone_food_menu.html", {"request": request})

@app.get("/chat-bot", response_class=HTMLResponse)
async def phone_chatbot(request: Request):
    return templates.TemplateResponse("phone_chat_bot.html", {"request": request})