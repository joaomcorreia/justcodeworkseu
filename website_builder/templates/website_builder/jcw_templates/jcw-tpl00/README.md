# JCW-TPL00 - JustCodeWorks Default Template

## Overview

**JCW-TPL00** is the foundational website template for the JustCodeWorks.EU platform. This template provides a complete, responsive website solution with dynamic content that adapts to different business types.

## 🚀 Features

### Core Sections
- **Hero Slider** - Eye-catching landing section with business messaging
- **Services Grid** - 6-card service display with CSS Grid layout 
- **About Us** - Company information with statistics and mission
- **Contact Form** - Professional contact form with business information

### Dynamic Content System
- **5 Supported Business Types**: Automotive, Construction, Healthcare, Restaurant, Portfolio/Creative
- **Automatic Content Adaptation** - All sections update based on business type
- **Industry-Specific Messaging** - Tailored content for each business category
- **Professional Design** - Modern, clean aesthetic suitable for all industries

### Technical Features
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- **Bootstrap 5.1.3** - Modern CSS framework for consistent styling
- **Font Awesome 6.0** - Professional icons throughout
- **CSS Grid** - Reliable service card layout
- **Smooth Animations** - Intersection Observer API for scroll animations
- **Clean Code** - Well-structured, maintainable HTML/CSS/JS

## 📁 File Structure

```
jcw-tpl00/
├── template.html          # Main HTML template file
├── config.json           # Template configuration and metadata
├── dynamic-content.js     # JavaScript for dynamic content updates
└── README.md             # This documentation file
```

## 🔧 Usage

### Basic Implementation
```html
<!-- Include the template -->
{% include 'website_builder/jcw_templates/jcw-tpl00/template.html' %}
```

### With Business Context
```python
context = {
    'business_name': 'AutoFix Garage',
    'business_type': 'automotive',
    'business_description': 'Professional automotive repair services...',
    'business_address': '123 Auto Street, Car City, ST 12345',
    'business_phone': '(555) 123-AUTO',
    'business_email': 'info@autofixgarage.com',
    'business_hours': 'Mon-Fri: 8AM-6PM, Sat: 9AM-3PM'
}
```

### Dynamic Content Initialization
```javascript
// Initialize template for specific business type
initializeTemplate('automotive', businessData);

// Update content dynamically
updateServicesContent('construction');
updateAboutContent('healthcare');
updateContactContent('restaurant');
```

## 🎨 Customization

### Supported Business Types
1. **Automotive** - Auto repair, maintenance, car services
2. **Construction** - Building, renovation, contracting
3. **Healthcare** - Medical, dental, wellness services  
4. **Restaurant** - Dining, catering, food services
5. **Portfolio** - Creative, design, marketing agencies

### Color Customization
The template uses CSS custom properties that can be easily modified:
```css
:root {
    --primary-color: #007bff;
    --secondary-color: #28a745;
    --accent-color: #ffc107;
    --text-color: #333333;
    --background-color: #ffffff;
}
```

### Layout Modifications
- **Services Grid**: Easily switch between 2-column and 3-column layouts
- **Section Spacing**: Modify padding in the configuration
- **Typography**: Update font families and sizes in the CSS

## 📱 Responsive Breakpoints

- **Desktop**: 1200px and up - Full layout with all features
- **Tablet**: 768px - 1199px - Adjusted spacing and typography  
- **Mobile**: 767px and below - Single column layout, stacked sections

## 🔗 Dependencies

### CSS Frameworks
- Bootstrap 5.1.3 (CDN)
- Font Awesome 6.0.0 (CDN)

### JavaScript Features
- Vanilla JavaScript (no external dependencies)
- Modern browser APIs (Intersection Observer, CSS Grid)
- Progressive enhancement approach

## 🚀 Performance

- **Lightweight**: Minimal external dependencies
- **Fast Loading**: Optimized CSS and JavaScript
- **SEO Friendly**: Semantic HTML structure
- **Accessible**: WCAG compliant elements and interactions

## 🔄 Version History

### Version 1.0.0 (October 10, 2025)
- Initial release with complete dynamic content system
- Support for 5 major business types
- Responsive design for all screen sizes
- Professional styling with Bootstrap 5 and Font Awesome
- Hero slider with business-specific messaging
- 6-card services grid with CSS Grid layout
- About us section with statistics and mission
- Contact form with business information display

## 🛠 Development Notes

### Integration with JustCodeWorks Platform
This template is designed to work seamlessly with:
- Django template rendering system
- JustCodeWorks Clippy assistant
- Multi-tenant subdomain architecture
- Automated business type detection

### Future Enhancements
- Google Maps integration for contact section
- Advanced color theme system
- Additional business type support
- Blog section integration
- E-commerce capabilities
- Multi-language support

## 📝 License

This template is part of the JustCodeWorks.EU platform and is proprietary software developed for the European SME Digital Transformation initiative.

## 🤝 Support

For technical support or customization requests:
- Email: support@justcodeworks.eu
- Platform: JustCodeWorks.EU Admin Dashboard
- Documentation: Internal development wiki

---

**Created by JustCodeWorks.EU Team**  
*Empowering European SMEs through digital transformation*