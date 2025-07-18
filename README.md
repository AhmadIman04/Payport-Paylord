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

# App snippets

<img width="417" height="834" alt="image" src="https://github.com/user-attachments/assets/a959b5b4-8723-48ba-914a-c9cef722cab3" />  <img width="412" height="832" alt="image" src="https://github.com/user-attachments/assets/b141d9b0-b294-4bff-bec2-6d942a0c33a0" />  <img width="397" height="825" alt="image" src="https://github.com/user-attachments/assets/5ed3ce4f-b8bc-40b1-87c1-f26b8757987c" />

<img width="436" height="837" alt="image" src="https://github.com/user-attachments/assets/0ef4b9d6-5b65-4d59-b1c2-6eab4475bf58" /> <img width="446" height="849" alt="image" src="https://github.com/user-attachments/assets/08eab4b6-5ca4-4402-9de8-798d1c4d38b0" />  <img width="1036" height="820" alt="image" src="https://github.com/user-attachments/assets/a004461f-5425-45aa-a821-c59d9e54623d" />






