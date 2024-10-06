# ServerSideWeb-Project: Activity Hub

## Overview
โครงงานนี้เป็นส่วนหนึ่งของรายวิชาการพัฒนาเว็บฝั่งเซิร์ฟเวอร์ (SERVER-SIDE WEB DEVELOPMENT) รหัสวิชา 06016418 ภาคเรียนที่ 1 ปีการศึกษา 2567

จัดทำขึ้นจากความต้องการของผู้คนที่มีเวลาว่างและต้องการหากิจกรรมที่น่าสนใจเข้าร่วม แต่ประสบปัญหาในการค้นหาข้อมูลเกี่ยวกับกิจกรรมต่างๆ ทั้งในเรื่องของสถานที่และเวลา จึงจำเป็นต้องมีระบบที่ช่วยในการรวบรวมและแสดงข้อมูลกิจกรรมให้ผู้ใช้สามารถเข้าถึงได้ง่ายและสะดวกมากขึ้น

ระบบนี้ไม่เพียงแต่ช่วยให้ผู้ใช้ค้นหากิจกรรมได้อย่างสะดวก แต่ยังรองรับการจัดการข้อมูลกิจกรรมด้วย โดยผู้ใช้ที่เป็นผู้จัด (Organizer) สามารถสร้างและจัดการกิจกรรมได้เอง 

## Pre Setup
- Python 3.x
- PostgreSQL (สำหรับการใช้งาน psycopg2)
- pip (สำหรับติดตั้ง dependencies)

## Setup Instructions

### 1. Create a virtual environment (Windows)
```bash
py -m venv myvenv
```

### 2. Activate virtual environment (Windows)
เมื่อสร้าง virtual environment เรียบร้อยแล้ว ให้ทำการ activate เพื่อเริ่มใช้งาน:
```bash
myvenv\Scripts\activate.bat
```

### 3. cd เข้าไปในโปรเจค
```bash
cd project_event_management 
```

### 4. Pip Install เข้าไปใน Environment ของ Project
หลังจาก activate virtual environment แล้ว ให้ติดตั้ง dependencies ที่จำเป็นด้วยคำสั่ง pip
```bash
pip install django
pip install psycopg2
pip install pillow
pip install python-decouple
```

### 5. Migrate Database
ก่อนรันโปรเจ็กต์ ให้ทำการ migrate ฐานข้อมูลด้วยคำสั่ง:
```bash
python manage.py migrate
```

## Environment Variables
โปรเจ็กต์นี้ใช้ไฟล์ `.env` ในการจัดการค่าตั้งค่าที่สำคัญ เช่น ข้อมูลการเชื่อมต่อฐานข้อมูลและการตั้งค่าอีเมล สำหรับการตั้งค่าโปรเจ็กต์ ให้สร้างไฟล์ `.env` ใน root directory ของโปรเจ็กต์ และใส่ค่าต่างๆ ตามตัวอย่างด้านล่าง:

```env
# Email Settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER="your-email@gmail.com"
EMAIL_HOST_PASSWORD="your-app-password"
```

### Run the Project
```bash
python manage.py runserver
```
