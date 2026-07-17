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