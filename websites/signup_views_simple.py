from django.shortcuts imp                                <form method="post" action="/signup/step2/">
                                {% csrf_token %}t render, redirect
from django.http import HttpResponse


def signup_step1(request):
    """Simple test signup page"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Signup Test - JustCodeWorks.EU</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-header bg-primary text-white">
                            <h3>🚀 Signup Flow Test</h3>
                        </div>
                        <div class="card-body">
                            <h4>✅ Success! The signup button works!</h4>
                            <p>This proves the URL routing is working correctly.</p>
                            
                            <form method="post" action="/signup/step2/">
                                <input type="hidden" name="csrfmiddlewaretoken" value="test">
                                <div class="mb-3">
                                    <label class="form-label">Business Name:</label>
                                    <input type="text" name="business_name" class="form-control" placeholder="Test Company" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Business Type:</label>
                                    <select name="business_type" class="form-control" required>
                                        <option value="technology">Technology</option>
                                        <option value="construction">Construction</option>
                                    </select>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Email:</label>
                                    <input type="email" name="email" class="form-control" placeholder="test@example.com">
                                </div>
                                <button type="submit" class="btn btn-primary">Continue to Step 2</button>
                            </form>
                            
                            <hr>
                            <p><a href="/" class="btn btn-secondary">← Back to Main Site</a></p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)


def signup_step2(request):
    """Simple step 2 test"""
    if request.method == 'POST':
        business_name = request.POST.get('business_name', 'Test Company')
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Step 2 - Domain Selection</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-5">
                <div class="row justify-content-center">
                    <div class="col-md-8">
                        <div class="card">
                            <div class="card-header bg-success text-white">
                                <h3>✅ Step 2 Working!</h3>
                            </div>
                            <div class="card-body">
                                <h4>Great! Form data received:</h4>
                                <p><strong>Business:</strong> {business_name}</p>
                                
                                <h5>🌐 Domain Suggestions:</h5>
                                <form method="post" action="/signup/step3/">
                                    <input type="hidden" name="csrfmiddlewaretoken" value="test">
                                    <input type="hidden" name="business_name" value="{business_name}">
                                    
                                    <div class="mb-3">
                                        <div class="form-check">
                                            <input class="form-check-input" type="radio" name="selected_domain" value="testcompany.justcodeworks.eu" id="domain1" checked>
                                            <label class="form-check-label" for="domain1">
                                                <strong>testcompany.justcodeworks.eu</strong> - Perfect for your business!
                                            </label>
                                        </div>
                                        <div class="form-check">
                                            <input class="form-check-input" type="radio" name="selected_domain" value="demo.justcodeworks.eu" id="domain2">
                                            <label class="form-check-label" for="domain2">
                                                <strong>demo.justcodeworks.eu</strong> - Short and memorable
                                            </label>
                                        </div>
                                    </div>
                                    
                                    <button type="submit" class="btn btn-success">Continue to Template Selection</button>
                                </form>
                                
                                <hr>
                                <p><a href="/signup/" class="btn btn-secondary">← Back to Step 1</a></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        return HttpResponse(html)
    
    return redirect('/signup/')


def signup_step3(request):
    """Simple step 3 test"""
    if request.method == 'POST':
        business_name = request.POST.get('business_name', 'Test Company')
        selected_domain = request.POST.get('selected_domain', 'testcompany.justcodeworks.eu')
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Step 3 - Template Selection</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-5">
                <div class="row justify-content-center">
                    <div class="col-md-8">
                        <div class="card">
                            <div class="card-header bg-warning">
                                <h3>🎨 Step 3 - Choose Template</h3>
                            </div>
                            <div class="card-body">
                                <h4>Almost done!</h4>
                                <p><strong>Business:</strong> {business_name}</p>
                                <p><strong>Domain:</strong> {selected_domain}</p>
                                
                                <h5>Choose Your Template:</h5>
                                <form method="post" action="/signup/complete/">
                                    <input type="hidden" name="csrfmiddlewaretoken" value="test">
                                    <input type="hidden" name="business_name" value="{business_name}">
                                    <input type="hidden" name="selected_domain" value="{selected_domain}">
                                    
                                    <div class="row">
                                        <div class="col-md-6">
                                            <div class="card">
                                                <div class="card-body">
                                                    <h6>🖥️ Professional Tech (TP1)</h6>
                                                    <p>Modern, clean design for tech companies</p>
                                                    <div class="form-check">
                                                        <input class="form-check-input" type="radio" name="selected_template" value="tp1" id="tp1" checked>
                                                        <label class="form-check-label" for="tp1">Choose TP1</label>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="card">
                                                <div class="card-body">
                                                    <h6>🔨 Dutch Construction (TP2)</h6>
                                                    <p>Warm design for construction companies</p>
                                                    <div class="form-check">
                                                        <input class="form-check-input" type="radio" name="selected_template" value="tp2" id="tp2">
                                                        <label class="form-check-label" for="tp2">Choose TP2</label>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div class="mt-3">
                                        <button type="submit" class="btn btn-warning">🚀 Create My Website!</button>
                                    </div>
                                </form>
                                
                                <hr>
                                <p><a href="/signup/step2/" class="btn btn-secondary">← Back to Domains</a></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        return HttpResponse(html)
    
    return redirect('/signup/')


def signup_complete(request):
    """Test completion"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Website Created!</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-header bg-success text-white">
                            <h3>🎉 Success! Signup Flow Complete!</h3>
                        </div>
                        <div class="card-body text-center">
                            <h4>✅ The entire signup process works!</h4>
                            <p>This proves that:</p>
                            <ul class="text-start">
                                <li>✅ URL routing is correct</li>
                                <li>✅ Form submissions work</li>
                                <li>✅ Multi-step flow functions</li>
                                <li>✅ Template system is ready</li>
                            </ul>
                            
                            <div class="alert alert-info">
                                <h5>🚀 Next Steps:</h5>
                                <p>Now we can add the real functionality:</p>
                                <ul class="text-start">
                                    <li>Database tenant creation</li>
                                    <li>Domain suggestions algorithm</li>
                                    <li>Template rendering</li>
                                    <li>Customer admin access</li>
                                </ul>
                            </div>
                            
                            <p>
                                <a href="/" class="btn btn-primary">🏠 Back to Main Site</a>
                                <a href="/signup/" class="btn btn-success">🔄 Test Again</a>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)