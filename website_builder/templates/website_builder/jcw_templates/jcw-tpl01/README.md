# JCW-TPL01: AI-Powered Business Template

## Overview
JustCodeWorks Template 01 is an advanced AI-powered website template that integrates with the MagicAI plugin to provide dynamic content generation and intelligent business website creation.

## Features

### 🤖 AI Content Generation
- **MagicAI Integration**: Connects to tools.justcodeworks.net for AI-powered content
- **Context-Aware Prompts**: Generates content based on business type and industry
- **Real-time Editing**: AI edit buttons throughout all sections

### 📱 Dynamic Card System
- **Scalable Sections**: Support for 3-9 cards per section
- **Dynamic Add/Remove**: Easy card management with visual controls
- **Multiple Card Types**: Services, Blog Posts, Team Members, FAQs

### 🎨 Professional Design
- **10-Row Structure**: Comprehensive business website layout
  1. Hero Section with AI-generated headlines
  2. About Section with company story
  3. Stats/Achievements showcase
  4. Services grid (3-9 cards)
  5. Blog/News section (3-9 posts)
  6. Team members (3-9 profiles)
  7. Navigation integration
  8. Pricing/Plans section
  9. FAQ system (3-9 questions)
  10. Contact/Footer section

### 🔧 Technical Features
- **Bootstrap 5.1.3**: Modern responsive framework
- **Font Awesome 6.0**: Professional icon system
- **Smooth Scrolling**: Enhanced navigation experience
- **Form Handling**: Contact form with validation
- **Cross-browser Compatible**: Works on all modern browsers

## Template Structure

```
jcw-tpl01/
├── template.html          # Main template file with 10 sections
├── config.json           # Template configuration and metadata
├── dynamic-content.js    # AI integration and dynamic card system
└── README.md            # This documentation
```

## Business Type Support

### Construction Industry
- Home renovation services
- Plumbing and electrical work
- General repairs and maintenance
- New construction projects

### Technology Sector
- Web development services
- Mobile app development
- Cloud solutions
- Cybersecurity services

### General Business
- Professional services
- Consulting
- Any business type with AI-generated content

## Dynamic Sections

### Services Section (Row 4)
- **Card Limit**: 3-9 service cards
- **AI Features**: Auto-generate service descriptions
- **Icons**: Font Awesome integration
- **Actions**: Add, remove, edit with AI

### Blog Section (Row 5)
- **Card Limit**: 3-9 blog posts
- **AI Features**: Generate titles and excerpts
- **Media**: Placeholder images with titles
- **Date System**: Automatic date handling

### Team Section (Row 6)
- **Card Limit**: 3-9 team members
- **AI Features**: Generate names, positions, bios
- **Photos**: Placeholder avatar system
- **Optional**: Hide navigation if no team members

### FAQ Section (Row 9)
- **Card Limit**: 3-9 questions
- **AI Features**: Generate Q&A pairs
- **Format**: Expandable question format
- **Industry-Specific**: Business type relevant questions

## MagicAI Integration

### API Endpoint
```javascript
this.magicAIEndpoint = '/tools/magicai/';
```

### Content Generation Process
1. **User clicks AI edit button**
2. **System builds context-aware prompt**
3. **Sends request to MagicAI plugin**
4. **Receives and applies generated content**
5. **Updates section with new content**

### Prompt Examples
```javascript
// Hero section prompt
`Create compelling hero section content for ${businessName}, 
a ${businessType} company. Include headline, subtitle, and call-to-action.`

// Services prompt
`Generate professional service descriptions for ${businessName}, 
a ${businessType} company. Create 6 services with titles, descriptions, and icons.`
```

## Usage Instructions

### 1. Template Selection
- Choose JCW-TPL01 during website creation
- System loads with business data from JCW-TPL00
- AI generates initial content based on business type

### 2. Content Customization
- Click "Change Content" buttons for AI generation
- Use "Add" buttons to increase cards per section
- Use "Remove" buttons to decrease cards (min 3)
- All changes are real-time and responsive

### 3. Section Management
- Each section has independent card management
- Navigation automatically updates for team section
- Card controls show/hide based on limits
- Re-indexing handles card removal

## Technical Implementation

### Class Structure
```javascript
class JCWTemplate01 {
    constructor() {
        this.magicAIEndpoint = '/tools/magicai/';
        this.maxCards = 9;
        this.minCards = 3;
        // ... initialization
    }
}
```

### Key Methods
- `generateDynamicSections()`: Initialize all dynamic content
- `addCard(section)`: Add new card to section
- `removeCard(section, index)`: Remove specific card
- `generateAIContent(section)`: Call MagicAI for content
- `updateCardControls(section, count)`: Manage UI controls

### Event Handling
- Contact form submission
- Smooth scrolling navigation
- Dynamic card management
- AI content generation

## Business Integration

### Data Flow
1. **JCW-TPL00** collects business information
2. **JCW-TPL01** receives business data
3. **MagicAI** enhances content with AI
4. **Template** displays professional result

### Supported Business Types
- `construction`: Construction and renovation services
- `technology`: Tech companies and IT services
- `general`: Any other business type

### Content Adaptation
- Service descriptions match business type
- Blog topics relevant to industry
- Team structures appropriate to sector
- FAQ questions industry-specific

## Performance Optimization

### Lazy Loading
- Images load only when needed
- AI content generates on-demand
- Dynamic cards create as required

### Responsive Design
- Mobile-first approach
- Breakpoints: sm, md, lg, xl
- Flexible grid system
- Touch-friendly controls

### Caching Strategy
- Business data stored in localStorage
- AI responses cached temporarily
- Template state persistence

## Browser Support
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Dependencies
- Bootstrap 5.1.3
- Font Awesome 6.0
- MagicAI Plugin
- tools.justcodeworks.net

## Configuration

### Template Config (config.json)
```json
{
    "name": "JCW-TPL01",
    "type": "ai-powered",
    "maxCards": 9,
    "minCards": 3,
    "aiIntegration": true,
    "magicAIEndpoint": "/tools/magicai/"
}
```

### Business Type Templates
Each business type has predefined service templates that AI can enhance and customize.

## Future Enhancements
- Advanced AI prompts for better content
- More business type templates
- Enhanced card designs
- Additional section types
- Multi-language support

## Support
For technical support or customization requests, contact the JustCodeWorks.EU development team.

---

**Template Version**: 1.0.0  
**Last Updated**: October 10, 2025  
**Author**: JustCodeWorks.EU Team