# Testing - Fitbody-App

This document outlines the testing carried out for the Fitbody-App application to ensure correct functionality, responsive layout, database integrity, and code reliability. Both **automated** and **manual** testing approaches were used throughout development.

---

## Testing Approach

### Automated Testing

**Framework**: Django Test Framework (unittest)

**Test Files**:
- `accounts/tests.py`
- `products/tests.py`
- `payments/tests.py`
- `community/tests.py`

**What is tested automatically**:

- ✅ CustomUser model creation and string representation
- ✅ Profile model with OneToOne relationship
- ✅ Product, ExercisePlan, NutritionPlan models
- ✅ Order and Subscription models
- ✅ ProgressPost and Comment models
- ✅ Double-purchase prevention
- ✅ View access control (login requirements)
- ✅ Registration and profile creation
- ✅ Product filtering by type, price, and search

### Manual Testing

**What is tested manually**:

- ✅ User experience and visual layout
- ✅ Real-world user scenarios
- ✅ Stripe payment flow
- ✅ Subscription management
- ✅ Community interactions
- ✅ Newsletter subscription
- ✅ Cross-browser and cross-device compatibility
- ✅ Accessibility with screen readers
- ✅ Keyboard navigation
- ✅ Form validation and error messages

---

## What is Testing?

Testing is the process of evaluating a software application to ensure it behaves as expected, meets requirements, and is free from defects. In web development, testing helps verify that code works correctly across different browsers, devices, and user scenarios. Testing improves code quality, reduces bugs, and enhances user experience.

### Types of Testing

#### Unit Testing

**Definition:** Unit testing involves testing individual components or functions of the code in isolation to ensure each part works correctly on its own.

**In this project:**

- Each model is tested independently (CustomUser, Profile, Product, Order, Subscription, ProgressPost)
- Tests verify that models have correct fields, constraints, and string representations
- Django's TestCase framework is used to run unit tests automatically
- Double-purchase prevention with validation logic

#### Automated Testing

Automated testing uses scripts and testing frameworks to run tests automatically without human intervention. Tests can be run repeatedly, ensuring consistent results and saving time during development.

**In this project:**

- Django Test Framework is used for automated testing
- Tests run with a single command: `python manage.py test`
- 60 unit tests covering models, views, and forms

#### Manual Testing

Manual testing involves a human interacting with the application to verify functionality, usability, and visual appearance. It tests real-world scenarios that automated tests might miss.

**In this project:**

- Visual layout on different screen sizes
- User experience and ease of navigation
- Browser compatibility (Chrome, Firefox, Edge, Safari)
- Device testing (mobile, tablet, desktop)
- Stripe payment flow verification
- Subscription management verification
- Community interaction testing

---

## Code Validation
### HTML Validation

I have used the recommended [HTML W3C validator](https://validator.w3.org) to validate all of my HTML files.

| Page | URL | Status |
|------|-----|--------|
| Homepage | `https://fitbody-app-9cff49d317d1.herokuapp.com/` | ✅ Pass |
| Products | `https://fitbody-app-9cff49d317d1.herokuapp.com/products/` | ✅ Pass |
| About | `https://fitbody-app-9cff49d317d1.herokuapp.com/about/` | ✅ Pass |
| Features | `https://fitbody-app-9cff49d317d1.herokuapp.com/features/` | ✅ Pass |
| Pricing | `https://fitbody-app-9cff49d317d1.herokuapp.com/pricing/` | ✅ Pass |
| Contact | `https://fitbody-app-9cff49d317d1.herokuapp.com/contact/` | ✅ Pass |
| Community | `https://fitbody-app-9cff49d317d1.herokuapp.com/community/` | ✅ Pass |
| Profile | `https://fitbody-app-9cff49d317d1.herokuapp.com/accounts/profile/username/` | ✅ Pass |


### HTML Code Validation Screenshots

| Homepage | ![](/static/docs/html-validation-screenshots/home.png) |
|----------|--------------------------------------------------------|
| Products | ![](/static/docs/html-validation-screenshots/products.png) |
| About | ![](/static/docs/html-validation-screenshots/about.png) |
| Features | ![](/static/docs/html-validation-screenshots/features.png) |
| Pricing | ![](/static/docs/html-validation-screenshots/pricing.png) |
| Contact | ![](/static/docs/html-validation-screenshots/contact.png) |
| Community | ![](/static/docs/html-validation-screenshots/community.png) |
| Profile | ![](/static/docs/html-validation-screenshots/profile.png) |

### CSS Validation

I have used the recommended [CSS Jigsaw Validator](https://jigsaw.w3.org/css-validator) to validate my CSS files.

| File | Link | Status |
|------|------|--------|
| `static/css/base.css` | [Validate CSS](https://jigsaw.w3.org/css-validator/validator?uri=https://fitbody-app-9cff49d317d1.herokuapp.com/static/css/base.css) | ✅ Pass |


### Python Validation (CI Python Linter)

| File | Result | Screenshot |
|------|--------|------------|
| `fitness_platform/settings.py` | ✅ Pass | ![settings.py](/static/docs/python-validation-screenshots/settings.png) |
| `accounts/views.py` | ✅ Pass | ![views.py](/static/docs/python-validation-screenshots/accountsviews.png) |
| `accounts/models.py` | ✅ Pass | ![models.py](/static/docs/python-validation-screenshots/accountsmodel.png) |


**Note:** Line length warnings are style suggestions only and do not affect functionality.


---

## Lighthouse Testing (Chrome DevTools)

Lighthouse audits were run on the deployed Heroku site.

| Category | Score | Screenshot |
|----------|-------|------------|
| Performance | Good | ![performance](/static/docs/lighthouse/performance.png) |
| Accessibility | 98% | ![accessibility](/static/docs/lighthouse/accessibility.png) |
| Best Practices | Good | ![bestpractices](/static/docs/lighthouse/bestpractices.png) |
| SEO | 100% | ![seo](/static/docs/lighthouse/seo.png) |

*(Scores may vary slightly by device/network)*

---

## Unit Testing Results

Django's built-in test framework was used for unit testing.

### Test Files

| File | Tests | Description |
|------|-------|-------------|
| `accounts/tests.py` | 18 tests | CustomUser, Profile models, registration, login, profile views |
| `products/tests.py` | 14 tests | Product, ExercisePlan, NutritionPlan models, filtering |
| `payments/tests.py` | 10 tests | Order, Subscription, MembershipPlan models |
| `community/tests.py` | 18 tests | ProgressPost, Comment models, likes, comments |

### Test Output

```
Found 60 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
............Not Found: /accounts/profile/nonexistent/
.......................................Not Found: /products/nonexistent/
.........
----------------------------------------------------------------------
Ran 60 tests in 86.354s

OK
```

### What was Tested

- ✅ CustomUser creation with username, email, password
- ✅ Profile auto-creation via signals
- ✅ Profile default values (bio, fitness_goal, membership_status)
- ✅ Product creation with exercise and nutrition plans
- ✅ Product filtering by type, price, and search
- ✅ Order creation with pending/paid status
- ✅ Subscription creation and activation
- ✅ ProgressPost creation with title and caption
- ✅ Comment creation on posts
- ✅ Like functionality (AJAX)
- ✅ View access control (login requirements)
- ✅ User registration with valid/invalid passwords

---

## Responsiveness Testing

Tested using Chrome DevTools on the following breakpoints:

| Device | Screen Width | Result |
|--------|--------------|--------|
| iPhone SE | 375px | ✅ Fully responsive |
| iPhone 12/13/14 | 390px | ✅ Fully responsive |
| iPad Mini | 768px | ✅ Fully responsive |
| iPad Air | 820px | ✅ Fully responsive |
| Desktop | 1024px+ | ✅ Fully responsive |
| Desktop | 1440px+ | ✅ Fully responsive |
| Desktop | 1920px+ | ✅ Fully responsive |

### Responsive Features Verified:
- ✅ Navigation bar collapses to hamburger menu on mobile
- ✅ Product cards stack vertically on mobile (1 column)
- ✅ Product cards display in 3 columns on desktop
- ✅ Community posts adjust to full width on mobile
- ✅ Dashboard cards stack on mobile
- ✅ Footer stacks columns on mobile
- ✅ Button sizes remain touch-friendly
- ✅ No horizontal scroll on any device

---

## Browser Compatibility

| Browser | Screenshot | Result |
|---------|------------|--------|
| Chrome | ![Chrome](/static/docs/browser-testing/chrome.png) | ✅ Works as expected |
| Edge | ![Edge](/static/docs/browser-testing/edge.png) | ✅ Works as expected |
| Firefox | ![Firefox](/static/docs/browser-testing/firefox.png) | ✅ Works as expected |
| Safari | ![Safari](/static/docs/browser-testing/safari.png) | ✅ Works as expected |
| Opera | ![Opera](/static/docs/browser-testing/opera.png) | ✅ Works as expected |

---

## Test Cases (Sample)

| Feature | Step(s) | Expected | Actual | Pass |
|---------|---------|----------|--------|------|
| User Registration | Fill form with valid data | Redirect to home, user created | As expected | ✅ |
| User Login | Enter valid credentials | Redirect to home, navbar changes | As expected | ✅ |
| View Products | Click "Products" in navbar | All products displayed | As expected | ✅ |
| Filter Products | Select "Exercise Plan" | Only exercise products shown | As expected | ✅ |
| View Product Detail | Click "View Details" | Product page with details | As expected | ✅ |
| Purchase Product | Click "Purchase Now" | Redirect to Stripe Checkout | As expected | ✅ |
| Subscribe to Premium | Click "Subscribe Monthly" | Redirect to Stripe Checkout | As expected | ✅ |
| Create Progress Post | Fill form with image | Post appears in feed | As expected | ✅ |
| Like a Post | Click heart button | Count increases, heart turns red | As expected | ✅ |
| Add Comment | Type comment and submit | Comment appears below post | As expected | ✅ |
| View Dashboard | Click "Dashboard" | Shows purchases and posts | As expected | ✅ |
| Newsletter Subscribe | Enter email in footer | Success message appears | As expected | ✅ |
| Admin Access | Visit /admin with superuser | Admin dashboard displays | As expected | ✅ |
|Browse Products | Click "Products" in the navigation bar | All products displayed | As expected | ✅ |

---

## Accessibility Testing

Manual accessibility checks were performed:

| Test | Result |
|------|--------|
| Semantic HTML structure (header, nav, main, footer) | ✅ Pass |
| ARIA labels on icon-only links | ✅ Pass |
| Color contrast ratio (WCAG 2.1 AA) - 7.1:1 | ✅ Pass |
| Keyboard navigation (Tab, Shift+Tab, Enter) | ✅ Pass |
| Form labels associated with inputs | ✅ Pass |
| Heading hierarchy (h1, h2, h3) | ✅ Pass |
| Focus indicators on interactive elements | ✅ Pass |

---

## Heading Hierarchy Validation

All pages were checked for proper heading hierarchy:

| Page | Heading Structure | Status |
|------|-------------------|--------|
| Homepage | h1 → h2 → h3 | ✅ Pass |
| Products | h1 → h2 → h3 | ✅ Pass |
| About | h1 → h2 → h3 | ✅ Pass |
| Features | h1 → h2 → h3 | ✅ Pass |
| Pricing | h1 → h2 → h3 | ✅ Pass |
| Contact | h1 → h2 | ✅ Pass |
| Login | h1 | ✅ Pass |
| Register | h1 | ✅ Pass |
| Dashboard | h1 → h2 → h3 | ✅ Pass |
| Community | h1 → h2 → h3 | ✅ Pass |
| Profile | h1 → h2 | ✅ Pass |

---

## User Story Testing

### New Users

| User Story | Test | Result |
|------------|------|--------|
| I want to register an account | Visit /accounts/register/ | ✅ Form works with validation |
| I want to view products without logging in | Visit /products/ as guest | ✅ Products fully visible |
| I want to browse exercise and nutrition plans | Use filter on products page | ✅ Filter works correctly |
| I want to purchase a plan | Click "Purchase Now" | ✅ Redirects to Stripe |

### Returning Users

| User Story | Test | Result |
|------------|------|--------|
| I want to login quickly | Use login form | ✅ Redirects to dashboard |
| I want to view my profile | Click profile link | ✅ Profile displays correctly |
| I want to edit my profile | Click "Edit Profile" | ✅ Form works with image upload |
| I want to see my dashboard | Click "Dashboard" | ✅ Shows purchases and posts |

### Community Engagement

| User Story | Test | Result |
|------------|------|--------|
| I want to post progress updates | Visit /community/create/ | ✅ Form works with image upload |
| I want to like posts | Click heart button | ✅ AJAX updates instantly |
| I want to comment on posts | Type comment and submit | ✅ Comment appears |
| I want to review products | Fill review form on product detail | ✅ Review saves |

### Newsletter Subscription

| User Story | Test | Result |
|------------|------|--------|
| I want to subscribe to the newsletter | Enter email in footer form | ✅ Success message appears |
| I want to see if I'm already subscribed | Enter same email again | ✅ "Already subscribed" message |
| I want to see subscribers in admin | Check admin panel | ✅ Email appears in list |

### Admin/Owner

| User Story | Test | Result |
|------------|------|--------|
| I want to manage products | Admin → Products → Add/Edit/Delete | ✅ Full CRUD functionality |
| I want to manage users | Admin → Users → View | ✅ Users visible |
| I want to view orders | Admin → Orders → View | ✅ Orders visible |
| I want to manage subscriptions | Admin → Subscriptions → View | ✅ Subscriptions visible |
| I want to manage newsletter subscribers | Admin → Newsletter subscribers | ✅ Full management |

---

## Bugs and Fixes

### Bugs Fixed During Development

| Bug | Description | Fix |
|-----|-------------|-----|
| `CustomUser has no profile` | Superuser created before signals | Manually created profiles for existing users |
| `NoReverseMatch: payments` | Payments namespace missing | Updated URL configuration |
| `No MembershipPlan matches query` | Yearly plan missing in admin | Created MembershipPlan in admin |
| SSL connection error | Database SSL misconfigured | Disabled SSL for Code Institute database |
| Product filter redirecting to home | Form missing action URL | Added `action="{% url 'products:list' %}"` |
| Filter not submitting | JavaScript conflict | Added `onchange="this.form.submit()"` to select |
| Favicon 404 errors | Browser looking at root | Added favicon links to static path |
| Accessibility: navbar toggle | Missing aria-label | Added `aria-label="Toggle navigation menu"` |
| Accessibility: social links | No accessible name | Added `aria-label` to each social link |
| Accessibility: heading order | Heading levels skipped | Changed heading tags to proper hierarchy |
| `stripe_sustomer_id` typo | Field name misspelled | Changed to `stripe_customer_id` |
| Profile capitalization | `Profile` vs `profile` | Standardized to lowercase `profile` |
| URL pattern order | `profile/edit/` not matching | Moved `profile/edit/` before dynamic pattern |
| Footer platform links | `#` placeholder links | Updated to correct URLs |
| Newsletter admin missing | Model not registered | Registered NewsletterSubscriber in admin |
| Footer hover effects | No hover feedback | Added CSS hover effects on all footer links |
| Test database errors | Database lock issues | Reset test database, all tests passing |
| Heading hierarchy | Skipped heading levels | Fixed all pages to have proper h1→h2→h3 structure |

### Known Issues (Future Improvements)

| Issue | Description | Planned Fix |
|-------|-------------|-------------|
| No email confirmations | Users don't receive email after registration | Integrate Django email backend |
| Yearly subscription | Only monthly plan available | Add yearly plan when ready |
| No password reset | Users can't reset password | Add password reset functionality |
| Limited product images | Products show placeholder | Add more product images |
| No email notifications | Newsletter subscribers don't receive emails | Integrate Mailchimp or SendGrid |

---

## Conclusion

The Fitbody-App fitness community platform functions reliably and meets all core project requirements:

- ✅ User authentication (register, login, logout, profile)
- ✅ Product management with exercise and nutrition plans
- ✅ Stripe payment integration (one-time and subscription)
- ✅ Community features (posts, likes, comments)
- ✅ User dashboard with purchases and posts
- ✅ Premium membership with access control
- ✅ Newsletter subscription with database storage
- ✅ Fully responsive design on all devices
- ✅ Deployed and working on Heroku
- ✅ Admin panel with full data management
- ✅ Accessibility: 98% Lighthouse score
- ✅ SEO: 100% Lighthouse score
- ✅ Heading hierarchy fixed on all pages
- ✅ 60 unit tests passing

The application has been tested across multiple browsers and devices, with all core features working as expected. Known limitations are documented for future improvement.

This testing approach ensures confidence in both functionality and code quality while leaving room for future enhancements such as email confirmations, password reset, and yearly subscription plans.