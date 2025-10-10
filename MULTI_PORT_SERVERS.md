# 🚀 Multi-Port Django Server Setup Guide

## ✅ **YES! You can absolutely run multiple Django servers on different ports!**

This is perfect for your JustCodeWorks platform to handle different scenarios and environments.

---

## 🎯 **Current Active Servers**

### **Port 8000** - Main Development Server
- **Command**: `python manage.py runserver 127.0.0.1:8000`
- **Admin**: http://127.0.0.1:8000/admin/
- **Website Builder**: http://127.0.0.1:8000/website-builder/

### **Port 8001** - Alternative Server
- **Command**: `python manage.py runserver 127.0.0.1:8001`  
- **Admin**: http://127.0.0.1:8001/admin/
- **Website Builder**: http://127.0.0.1:8001/website-builder/

### **Port 8002** - Demo Server
- **Command**: `python manage.py runserver 127.0.0.1:8002`
- **Admin**: http://127.0.0.1:8002/admin/
- **Website Builder**: http://127.0.0.1:8002/website-builder/

### **Port 8003** - Testing Server  
- **Command**: `python manage.py runserver 127.0.0.1:8003`
- **Admin**: http://127.0.0.1:8003/admin/
- **Website Builder**: http://127.0.0.1:8003/website-builder/

---

## 🔧 **How to Start Multiple Servers**

### **Basic Command Structure**
```bash
# General format
python manage.py runserver [IP:PORT]

# Examples
python manage.py runserver 127.0.0.1:8000
python manage.py runserver 127.0.0.1:8001
python manage.py runserver 127.0.0.1:8002
python manage.py runserver 127.0.0.1:8003
python manage.py runserver 127.0.0.1:8004
python manage.py runserver 127.0.0.1:8005
```

### **Starting Servers in Background**
```bash
# Start multiple servers (each in separate terminal/PowerShell)
cd c:\projects\justcodeworkseu

# Terminal 1
python manage.py runserver 127.0.0.1:8000

# Terminal 2  
python manage.py runserver 127.0.0.1:8001

# Terminal 3
python manage.py runserver 127.0.0.1:8002

# And so on...
```

---

## 🎪 **Use Cases for Multiple Ports**

### **1. Different Client Demos**
- **Port 8000**: Main demo for government
- **Port 8001**: HMD Klusbedrijf demo 
- **Port 8002**: Taxi Pro Service demo
- **Port 8003**: AutoFix Garage demo

### **2. Development & Testing**
- **Port 8000**: Main development
- **Port 8001**: Testing new features
- **Port 8002**: Client preview environment
- **Port 8003**: Backup/fallback server

### **3. Different Configurations**
```bash
# Different settings files
python manage.py runserver 127.0.0.1:8000 --settings=justcodeworks.settings
python manage.py runserver 127.0.0.1:8001 --settings=justcodeworks.settings_demo  
python manage.py runserver 127.0.0.1:8002 --settings=justcodeworks.settings_client
```

### **4. Performance Testing**
- **Load balancing simulation**
- **Concurrent user testing**
- **Feature comparison**

---

## 📋 **Quick Start Scripts**

### **Windows PowerShell Script**
Create `start_servers.ps1`:
```powershell
# Start multiple Django servers
Start-Process powershell -ArgumentList "-Command", "cd c:\projects\justcodeworkseu; python manage.py runserver 127.0.0.1:8000"
Start-Process powershell -ArgumentList "-Command", "cd c:\projects\justcodeworkseu; python manage.py runserver 127.0.0.1:8001" 
Start-Process powershell -ArgumentList "-Command", "cd c:\projects\justcodeworkseu; python manage.py runserver 127.0.0.1:8002"
Start-Process powershell -ArgumentList "-Command", "cd c:\projects\justcodeworkseu; python manage.py runserver 127.0.0.1:8003"

Write-Host "✅ Started servers on ports 8000, 8001, 8002, 8003"
Write-Host "🌐 Access: http://127.0.0.1:8000/admin/"
```

### **Batch File**  
Create `start_servers.bat`:
```batch
@echo off
cd c:\projects\justcodeworkseu
start "Server 8000" python manage.py runserver 127.0.0.1:8000
start "Server 8001" python manage.py runserver 127.0.0.1:8001  
start "Server 8002" python manage.py runserver 127.0.0.1:8002
start "Server 8003" python manage.py runserver 127.0.0.1:8003

echo ✅ Started 4 Django servers
echo 🌐 Main: http://127.0.0.1:8000/admin/
pause
```

---

## 🎯 **Business Applications**

### **Government Demo Setup**
```bash
# Demo Environment
Port 8000: Main presentation
Port 8001: Backup server  
Port 8002: Interactive demo for officials
Port 8003: Technical deep-dive server
```

### **Client Management**
```bash
# Client-Specific Servers
Port 8000: HMD Klusbedrijf portal
Port 8001: Taxi Pro Service portal
Port 8002: AutoFix Garage portal  
Port 8003: New client onboarding
```

### **Development Workflow**
```bash
# Development Setup
Port 8000: Stable development
Port 8001: Feature testing
Port 8002: Client preview
Port 8003: Integration testing
```

---

## 🔧 **Management Commands**

### **Check Active Ports**
```bash
# See what's running on specific ports
netstat -ano | findstr :8000
netstat -ano | findstr :8001  
netstat -ano | findstr :8002
netstat -ano | findstr :8003
```

### **Stop All Servers**
```bash
# Kill all Python processes (stops all servers)
taskkill /f /im python.exe

# Or stop individually by finding PID and killing specific process
```

### **Server Health Check**
```bash
# Quick test if servers are responding
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8001/
curl http://127.0.0.1:8002/
curl http://127.0.0.1:8003/
```

---

## ⚡ **Pro Tips**

### **Port Range Considerations**
- **8000-8010**: Django development servers
- **3000-3010**: Node.js/React development servers  
- **5000-5010**: Flask/Python web servers
- **9000-9010**: Custom applications

### **Resource Management**
- Each server uses memory and CPU
- Monitor system resources with multiple servers
- Consider using different databases for different purposes

### **URL Organization**
```
http://127.0.0.1:8000/  → Main Development
http://127.0.0.1:8001/  → Client Demo
http://127.0.0.1:8002/  → Government Demo  
http://127.0.0.1:8003/  → Feature Testing
```

---

## 🎉 **Perfect for JustCodeWorks Business Model!**

### **SaaS Demonstration**
- **Multiple demo environments** for different client industries
- **A/B testing** different features and templates  
- **Scalability demonstration** showing multiple server capability

### **Client Service**  
- **Dedicated environments** for high-value clients
- **Staging environments** for client approval
- **Backup servers** for business continuity

### **European Market**
- **Localization testing** (Portuguese, Spanish, French servers)
- **Regional demonstrations** tailored to different countries
- **Government compliance** testing on separate environments

**You now have unlimited flexibility to run as many Django servers as you need for your European SME platform! 🇪🇺🚀**