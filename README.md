# 🤖 AI Productivity Personal Assistant

Sebuah aplikasi asisten produktivitas pribadi berbasis AI yang dibangun menggunakan **Streamlit** dan **Google Gemini API** (`google-genai` SDK). Aplikasi ini dirancang untuk membantu Anda mengelola tugas harian, memantau *goals*, mencatat ide dengan cepat, dan mendapatkan wawasan produktivitas berbasis AI.

---

## ✨ Fitur Utama

1. **📋 AI Task Management:** Tambah, selesaikan, dan hapus tugas hanya dengan mengetik pesan natural (menggunakan *NLP Intent Parsing*).
2. **🎯 Daily Goals Tracker:** Tentukan hingga 3 target harian dan pantau progres pencapaian Anda.
3. **📝 Quick Notes Organizer:** Catat ide secara cepat. Biarkan AI mengelompokkan dan merangkum catatan Anda secara otomatis.
4. **📊 Weekly Review:** Dapatkan ringkasan performa mingguan yang digenerate oleh AI berdasarkan rasio penyelesaian tugas dan *goals* Anda.
5. **💡 Productivity Tips:** AI yang suportif siap memberikan motivasi dan saran konkret (seperti *Pomodoro* atau *time-blocking*) sesuai dengan tingkat penyelesaian tugas Anda hari ini.
6. **🗣️ Gaya Bahasa Dinamis:** Sesuaikan gaya komunikasi AI (*Formal*, *Santai*, atau *Profesional*) langsung dari *sidebar*.

---

## 📂 Struktur Proyek

```text
productivity-assistant/
├── app.py                 # File utama aplikasi Streamlit
├── config.py              # Konfigurasi & Inisialisasi API Gemini
├── .env                   # Tempat menyimpan API Key yang aman (di-ignore Git)
├── requirements.txt       # Daftar pustaka / dependensi proyek
├── utils/
│   ├── ai_handler.py      # Logika utama komunikasi dengan AI Gemini
│   ├── task_manager.py    # CRUD untuk tugas
│   ├── goals_tracker.py   # Logika pemantauan goals harian
│   ├── notes_manager.py   # Pencatatan dan kategorisasi AI
│   └── weekly_review.py   # Sintesis review mingguan
└── components/
    ├── sidebar.py         # UI untuk pengaturan dan navigasi
    └── chat_interface.py  # Antarmuka utama chatbot
```

---

## 🚀 Cara Menjalankan Proyek

### 1. Prasyarat (Prerequisites)
Pastikan Anda telah menginstal **Python 3.10+** di sistem Anda.

### 2. Instalasi
Clone repository ini, masuk ke folder proyek, dan instal dependensi yang dibutuhkan:
```bash
git clone https://github.com/USERNAME_ANDA/NAMA_REPO_ANDA.git
cd productivity-assistant
pip install -r requirements.txt
```

### 3. Konfigurasi API Key
Aplikasi ini membutuhkan API Key dari [Google Gemini (Google AI Studio)](https://aistudio.google.com/app/apikey).
Buat sebuah file bernama `.env` di folder utama aplikasi dan masukkan API Key Anda:
```env
GEMINI_API_KEY=KUNCI_API_ANDA_DI_SINI
```

> **Catatan Penggunaan Model:**
> Jika Anda mengalami *Error 503 (Model is currently experiencing high demand)*, ini berarti server Google sedang penuh. Anda bisa mengganti nama model yang digunakan (`MODEL_NAME`) di dalam file `config.py`.
> Untuk daftar lengkap model terbaru yang tersedia, Anda bisa mengecek dokumentasi resmi di [ai.google.dev/gemini-api/docs/models/gemini](https://ai.google.dev/gemini-api/docs/models/gemini).

### 4. Jalankan Aplikasi
Gunakan Streamlit untuk menjalankan server secara lokal:
```bash
streamlit run app.py
```
Aplikasi akan otomatis terbuka di browser Anda (biasanya di `http://localhost:8501`).

---

## 🛠️ Teknologi yang Digunakan
* **Bahasa:** Python 3
* **Framework Web UI:** Streamlit
* **AI & LLM:** Google Gemini API (`google-genai` SDK) dengan model `gemini-2.5-flash` / `gemini-3.1-flash-lite`.

---
*Dibuat untuk memenuhi proyek akhir — LLM-Based Tools and Gemini API Integration.*
