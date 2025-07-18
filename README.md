# 🧾 PayPort — QR-Powered Merchant Registration Gateway

**PayPort** is a modern platform that simplifies merchant onboarding through centralized registration and QR code-based autofill. It is designed for MSMEs (micro, small, and medium enterprises) who are registering on food delivery platforms or other digital services.

Merchants fill in their information once and can reuse it across platforms with a single QR scan — drastically reducing repetitive manual form-filling and document uploading.  

📌 **Now with AI-powered support via Gemini Chatbot**  
PayPort also includes an intelligent chatbot assistant powered by **Gemini and RAG (Retrieval-Augmented Generation)**, which provides contextual help to guide users step-by-step through the registration process.

---

## 🚀 Key Features

- 📋 Multi-step merchant registration with autosave
- 📎 Secure upload of documents (SSM cert, IC, etc.)
- 🔄 Resume saved sessions with local storage
- 📦 Data stored securely in Supabase (PostgreSQL + File Storage)
- 📲 QR code generation to encapsulate merchant identity
- 📷 Camera-based QR scanning to auto-fill forms
- 🧠 Gemini-powered **AI chatbot** with RAG to assist users during onboarding

---

## 🧠 What Makes PayPort Different?

| Problem | Traditional Onboarding | PayPort |
|--------|--------------------------|---------|
| ⏱ Time | Multiple forms per platform | Fill once, scan to auto-fill |
| 📂 Files | Upload documents every time | One-time upload |
| ❓ Help | No guidance or agent support | AI chatbot built-in |
| 🛠️ Flexibility | Forms differ by platform | Unified merchant data structure |

---

## 🧭 How It Works

### 🧑‍💼 Step 1: Merchant Registration
- User visits PayPort and fills in **all business information**.
- Uploads all required documents (e.g. SSM cert, personal ID, business logo).
- Data is stored securely in the **PayPort database**.

### 🔳 Step 2: QR Code Generation
- After registration, the user clicks on **“Display QR”**.
- A dynamically generated **QR code** is shown.
- This code is tied to the merchant’s PayPort ID.

### 📝 Step 3: Quick Form Auto-Fill
- On a third-party registration form, click **“Sign in with QR”**.
- Scan the QR code using the camera.
- The system retrieves the merchant’s data and **auto-fills** the form in real time.

### 💬 Step 4: Need Help? Use the Chatbot
- At any point, users can open the **AI chatbot** powered by **Gemini**.
- Ask questions like:
  - “What documents do I need?”
  - “How do I fix a missing field?”
  - “Where can I view my QR code?”
- The chatbot uses **retrieval-augmented generation (RAG)** to provide **accurate, context-aware answers** using internal documentation and guides.

---


