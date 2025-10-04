## 🚀 Quick Manual Setup for Subdomains

Since you need admin access to modify the hosts file, here's the quickest way:

### **Step 1: Edit Windows Hosts File**

1. **Press `Win + R`**, type `notepad`, **right-click** and select **"Run as administrator"**
2. In Notepad, click **File > Open** and navigate to: `C:\Windows\System32\drivers\etc\hosts`
3. **Change file type** from "Text Documents" to **"All Files"** to see the hosts file
4. **Add these lines at the bottom** of the file:

```
# JustCodeWorks.EU Customer Subdomains
127.0.0.1    vakwerkpro.justcodeworks.eu
127.0.0.1    bouwbedrijf-amsterdam.justcodeworks.eu
127.0.0.1    techsolutions.justcodeworks.eu
127.0.0.1    webstudio-delft.justcodeworks.eu
127.0.0.1    schilder-partners.justcodeworks.eu
```

5. **Save and close** Notepad

### **Step 2: Flush DNS Cache**

Open Command Prompt and run:
```cmd
ipconfig /flushdns
```

### **Step 3: Test the Subdomains**

Make sure your Django server is running, then visit:

#### **Customer Websites:**
- **VakWerk Pro (Construction)**: http://vakwerkpro.justcodeworks.eu:8001/
- **TechSolutions (Tech)**: http://techsolutions.justcodeworks.eu:8001/
- **Bouwbedrijf (Construction)**: http://bouwbedrijf-amsterdam.justcodeworks.eu:8001/

#### **Customer Admin Panels:**
- **VakWerk Admin**: http://vakwerkpro.justcodeworks.eu:8001/admin/
- **TechSolutions Admin**: http://techsolutions.justcodeworks.eu:8001/admin/

#### **Your Main Site (unchanged):**
- **JustCodeWorks**: http://127.0.0.1:8001/

---

### **Expected Results:**

✅ **vakwerkpro.justcodeworks.eu** → Dutch construction template (TP2)  
✅ **techsolutions.justcodeworks.eu** → Professional tech template (TP1)  
✅ **Each gets their own branding** and company information  
✅ **Admin panels** work for customer content management  

### **If it doesn't work:**
1. Check hosts file syntax (no extra spaces)
2. Restart your browser 
3. Try `ipconfig /flushdns` again
4. Make sure Django server is running on port 8001

**Ready to test real subdomains! 🎯**