# 🥗 Healthy Meal Planner

A Django-based meal preparation platform with calorie tracking, BMI calculation, and personalized recipe management. This can be a freesource for a comprehensive database to healthy recipies with customisation per user needs. Keeping track of your meals will be a easy job and once a recipe is store on profile, can be reused indefinitly on the account. User can change portion size to control calorie intake, change recipe ingredients and quantities to make better healthy choices. Profile will keep the trak of weight and BMI. Recipies are free to browse while to gain all benifits of the website user will have to sign up.

🔗 **Live Link:** [Healthy Meal Planner](https://healthy-meal-planner-cc66090aa001.herokuapp.com/) 
📂 **Repository:** [darakhshanda/healthy_meal_planner](https://github.com/darakhshanda/healthy_meal_planner)

---
A responsive site layout enables easy navigation on all devices.

## Desktop
<p><img width="1787" alt="desktop" src="https://github.com/"></p>

## Tablet
<p><img width="600" alt="tablet" src="https://github.com/"></p>

## Mobile
<p><img width="400" alt="iphone" src="https://github.com/"></p>


## UX Design

### Typography

[**Font Awesome**](https://fontawesome.com) icons were used for the site icons. For example, the social media icons in the footer of the pages.

[**Lato**](https://fonts.google.com/specimen/Lato) was used for the primary headers and titles.




### Colour Palette ###
![screenshot](docs/images/swatch.png)

A simple colour palette was chosen to compliment the vibrant images of the band, with a plain white page background, blue icons and a dark gray footer and individual blog page  header background. A simple red was chosen for the link hover to blog pages.



### Home Page Wireframe Design
<img width="1043" alt="Home" src="https://github.com/mbriscoe/broken-lines-blog/assets/86828720/fc1c7075-0936-462b-a62c-97e1c3dc9bf1" style="width:70%;">

## 📑 Table of Contents

- [Summary](#-summary)
- [Site Goals](#-site-goals)
- [User Management](#1-user-management)
- [User Profile Management](#2-user-profile-management)
- [Recipe Management](#3-recipe-management)
- [Meal Planning](#4-meal-planning)
- [Nutrition Tracking](#5-nutrition-tracking)
- [Search & Discovery](#6-search--discovery)
- [Data Models](#7-data-models)
- [Authentication & Security](#8-authentication--security)
- [User Stories](#-user-stories)
- [Technical Architecture](#-technical-architecture)
- [Database Models](#️-database-models)
- [Design](#-design)
- [Features](#-features)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Technologies Used](#️-technologies-used)
- [Credits](#-credits)
- [Acknowledgments](#-acknowledgments)

---

## 📖 Summary

**Healthy Meal Planner** is an interactive web application designed to help users manage their nutrition through:

- **Personalized calorie tracking** based on BMI and activity levels
- **Recipe creation and management** with detailed nutritional breakdowns
- **Meal planning** with daily calorie summaries
- **Health metrics monitoring** including BMI calculations

This project solves:

- Difficulty tracking daily caloric intake
- Lack of personalized meal planning tools
- Need for accessible nutrition information
- Complex macro tracking (protein, carbs, fat)

### Target Users

- Health-conscious individuals
- Fitness enthusiasts tracking macros
- Families planning balanced meals
- People managing dietary restrictions
- Anyone seeking nutritional awareness

### Unique Aspects

- Automated BMI and calorie goal calculations
- Ingredient-based nutrition tracking
- Customizable recipe creation
- Django-powered security and scalability

---

## 📌 Site Goals

### Core Functionality

- Provide calorie and macro tracking for health-conscious users
- Enable recipe creation, browsing, and management
- Calculate personalized daily calorie goals based on BMI and activity level
- Allow meal planning and tracking against nutritional targets
- Support ingredient management with precise nutritional data

### User Experience

- Clean, intuitive interface for recipe management
- Responsive design for mobile, tablet, and desktop
- Quick access to daily calorie summaries
- Visual nutrition breakdowns with progress indicators
- Secure user authentication and profile management

### Scalability

- Support for recipe sharing and community features
- Expandable to include meal prep scheduling
- Potential API integration for third-party apps
- Multi-user household management

---
# Project Functionalities
## Overview
This document outlines all the functionalities and features available in the Healthy Meal Planner application, a Django-based web platform designed to help users manage their nutrition through calorie tracking, meal planning, and personalized recipe management.


## 1. User Management

### Registration
- **Custom User Registration Form** (`CustomRegistrationForm`)
- Features:
  - Username validation (minimum 3 characters, unique)
  - Email validation (unique, case-insensitive)
  - Strong password validation
  - Password confirmation requirement
  - Bootstrap-styled form inputs
  - Error handling and user feedback

### Login & Authentication
- Django Allauth integration for authentication
- Login-required decorators on protected views
- Session management
- User authentication persistence

### Profile Access
- Each user has a unique profile
- View and edit personal information
- Account management through Django Allauth

---

## 2. User Profile Management

### Profile Setup
**Endpoint:** `profile/`
**View:** `profile_setup(request)`

#### User Health Information Stored:
- **Personal Details:**
  - First Name
  - Last Name
  - Age
  - Gender (Male, Female, Other)
  - Profile Image (Cloudinary storage)

- **Physical Measurements:**
  - Height (in centimeters)
  - Weight (in kilograms)

#### Automatic Calculations:
1. **BMI (Body Mass Index)**
   - Formula: weight_kg / (height_m²)
   - Automatically calculated and stored
   - Updated whenever health data changes

2. **Daily Calorie Goal**
   - Formula: Mifflin-St Jeor Equation
   - Adjusts based on:
     - Gender
     - Age
     - Weight
     - Height
     - Activity Factor (Default: 1.2 - Sedentary)
   - Calculated as: BMR × Activity Factor
   - Auto-calculated on profile save

#### Features:
- One-to-one relationship with Django User model
- Image upload via Cloudinary
- Timestamp tracking (created_at, updated_at)
- Automatic calculations before saving
- Success messages confirming profile updates

---

## 3. Recipe Management

### Recipe Model
**Database Table:** `recipe`

#### Recipe Information:
- **Basic Details:**
  - Title (max 255 characters)
  - Description
  - Instructions
  - Recipe Image (Cloudinary storage)

- **Cooking Information:**
  - Servings (default: 1)
  - Prep Time (in minutes)
  - Cook Time (in minutes)
  - Total Time (calculated: prep_time + cook_time)

- **Ingredients:**
  - Stored as JSON format
  - Supports detailed ingredient lists with quantities

- **Nutritional Information (per serving):**
  - Total Calories
  - Protein (grams)
  - Carbohydrates (grams)
  - Fat (grams)
  - Fiber (grams)

- **Categorization:**
  - Breakfast
  - Lunch
  - Dinner
  - Snack

- **Ownership & Timestamps:**
  - Created by (User ForeignKey)
  - Created at (auto-generated)
  - Updated at (auto-tracked)

### Recipe CRUD Operations

#### Create Recipe
**Endpoint:** `recipes/create/`
**View:** `RecipeCreateView` (Class-based)
- Authentication required
- Upload recipe image
- Enter ingredient list
- Set nutritional values
- Categorize recipe
- Auto-timestamps creation

#### Read/View Recipes
**Multiple Views:**
1. **Recipe List View** (`recipes/`)
   - `RecipeListView` - Browse all recipes
   - Paginated display (12 recipes per page)
   - Search functionality

2. **Recipe Detail View** (`recipes/<int:recipe_id>/`)
   - Full recipe information
   - Nutritional breakdown
   - Ingredient list
   - Instructions
   - Creator information

3. **User's Recipes** (`recipes/user/<username>/`)
   - View all recipes created by specific user
   - Filtered by username

#### Update Recipe
**Endpoint:** `recipes/<int:pk>/edit/`
**View:** `RecipeUpdateView`
- Edit recipe details
- Update nutritional information
- Modify ingredients
- Change category
- Update timestamps automatically

#### Delete Recipe
**Endpoint:** `recipes/<int:pk>/delete/`
**View:** `RecipeDeleteView`
- Permanent deletion
- Login required

### Recipe Display on Homepage
**Endpoint:** `/` (index)
**Features:**
- All recipes displayed with search
- Search by title and description
- Pagination support
- Recipe serialization to JSON
- Responsive grid layout

---

## 4. Meal Planning

### Meal Plan Model
**Database Table:** `meal_plan`

#### Structure:
- **User Association:**
  - Foreign Key to User
  - One meal plan per user per day (unique_together constraint)

- **Daily Meal Slots:**
  - Breakfast Recipe (nullable, Foreign Key to Recipe)
  - Lunch Recipe (nullable, Foreign Key to Recipe)
  - Dinner Recipe (nullable, Foreign Key to Recipe)
  - Snack Recipe (nullable, Foreign Key to Recipe)

- **Timestamps:**
  - Created at
  - Updated at

#### Meal Plan Features:

1. **Get Total Calories**
   - Sums calories from all selected recipes
   - Handles null recipes gracefully

2. **Get All Recipes**
   - Returns dictionary of all meal slots
   - Structure: `{'breakfast': recipe, 'lunch': recipe, ...}`

3. **Is Complete Check**
   - Validates if all meal slots are filled

4. **Meal Plan Summary**
   - Returns structured summary:
     ```
     {
       'breakfast': {'title': 'Recipe Title', 'calories': 350},
       'lunch': {'title': 'Recipe Title', 'calories': 450},
       'dinner': {'title': 'Recipe Title', 'calories': 600},
       'snack': {'title': 'Recipe Title', 'calories': 150},
       'total_calories': 1550
     }
     ```

### Meal Plan CRUD Operations

#### Create Meal Plan
**Endpoint:** `meal-plan/create/`
**View:** `create_meal_plan(request)`
- Create meal plan for specific date
- Optional: Pre-fill recipes
- Auto-creates plan if doesn't exist

#### View Meal Plans
**Multiple Endpoints:**

1. **Current Day Meal Plan** (`dashboard/`)
   - Shows today's meal plan
   - Displays selected recipes
   - Shows total calories consumed
   - Calculates remaining calories
   - `meal_plan_current` view

2. **All User Meal Plans** (`meal-plans/`)
   - List of all meal plans
   - Sorted by date (newest first)
   - `meal_plan_list_view`

3. **Specific Date Meal Plan** (`meal-plan/<date>/`)
   - View meal plan for specific date
   - `meal_plan_view` view

#### Update Meal Plan
**Endpoint:** `meal-plan/<int:plan_id>/update/`
**View:** `meal_plan_update(request, plan_id)`
- Modify recipe selections
- Change any meal slot
- Auto-updates timestamps

#### Delete Meal Plan
**Endpoint:** `meal-plan/<int:plan_id>/delete/`
**View:** `delete_meal_plan(request, plan_id)`
- Remove entire meal plan
- Permanent deletion

### Meal Plan Form
**Form:** `MealPlanForm`
- Select recipes for each meal
- Dropdown selection from available recipes
- Form validation

---

## 5. Nutrition Tracking

### Dashboard View
**Endpoint:** `dashboard/`
**View:** `dashboard(request)`

#### Displays:
1. **User Profile Summary**
   - BMI Status
   - Daily Calorie Goal

2. **Today's Meal Plan**
   - Current date's meal plan
   - All meal slots and selections

3. **Nutrition Summary**
   - Total calories consumed today
   - Remaining calories for the day
   - Calculation: `remaining = daily_goal - total_consumed`

4. **Progress Information**
   - Count of user's created recipes
   - Meal plan status

### Nutrition Calculations:

#### BMI Calculation
```
BMI = weight_kg / (height_m²)
```
- Performed on UserProfile.save()
- Rounded to 2 decimal places

#### Daily Calorie Goal (Mifflin-St Jeor Equation)
```
For Males:
  BMR = 10×weight + 6.25×height - 5×age + 5
  Daily Goal = BMR × Activity Factor

For Females:
  BMR = 10×weight + 6.25×height - 5×age - 161
  Daily Goal = BMR × Activity Factor

Activity Factor = 1.2 (Sedentary, default)
```

#### Meal-based Nutrition:
- Each recipe stores macro breakdown:
  - Protein (g)
  - Carbohydrates (g)
  - Fat (g)
  - Fiber (g)
- Total daily macros sum from selected recipes

---

## 6. Search & Discovery

### Homepage Search
**Endpoint:** `/`
**Features:**
- Real-time search capability
- Search fields:
  - Recipe title (case-insensitive)
  - Recipe description (case-insensitive)
- Pagination (12 recipes per page)
- Displays all matching recipes

### Browse by Category
- Recipes organized by:
  - Breakfast
  - Lunch
  - Dinner
  - Snack

### Browse User Recipes
**Endpoint:** `recipes/user/<username>/`
- View all recipes created by specific user
- Filter by username
- User-specific recipe discovery

---

## 7. Data Models

### UserProfile
```
- user (OneToOneField to User)
- first_name, last_name (CharField)
- user_image (CloudinaryField)
- age (IntegerField)
- gender (CharField: male, female, other)
- height_cm (FloatField)
- weight_kg (FloatField)
- daily_calorie_goal (FloatField)
- bmi (FloatField)
- created_at (DateTimeField)
- updated_at (DateTimeField)

Methods:
- calculate_bmi()
- calculate_daily_calorie_needs()
- save() - auto-calculates on save
```

### Recipe
```
- title (CharField, max 255)
- description (TextField)
- instructions (TextField)
- image_url (CloudinaryField)
- servings (IntegerField)
- prep_time_minutes (IntegerField)
- cook_time_minutes (IntegerField)
- ingredients (JSONField)
- total_calories (FloatField)
- protein (FloatField)
- carbs (FloatField)
- fat (FloatField)
- fiber (FloatField)
- category (CharField: breakfast, lunch, dinner, snack)
- created_by (ForeignKey to User)
- created_at (DateTimeField)
- updated_at (DateTimeField)

Methods:
- total_time() - returns prep + cook time
```

### MealPlan
```
- user (ForeignKey to User)
- day (DateField)
- breakfast_recipe (ForeignKey to Recipe, nullable)
- lunch_recipe (ForeignKey to Recipe, nullable)
- dinner_recipe (ForeignKey to Recipe, nullable)
- snack_recipe (ForeignKey to Recipe, nullable)
- created_at (DateTimeField)
- updated_at (DateTimeField)

Constraints:
- unique_together: ['user', 'day']

Methods:
- get_total_calories() - sums all recipe calories
- get_all_recipes() - returns dict of all meals
- is_complete() - checks if all slots filled
- meal_plan_summary() - returns structured summary
```

---

## 8. Authentication & Security

### Security Features
1. **Login Required Decorators**
   - `@login_required()` on protected views
   - Automatic redirect to login page

2. **User Isolation**
   - Each user only sees/edits their own data
   - Filter by `request.user` in queries

3. **Ownership Validation**
   - Recipes linked to `created_by` user
   - Meal plans linked to specific user
   - Delete operations restricted to owners

4. **Password Hashing**
   - Django's built-in password hashing
   - Custom password validation rules

5. **Email Validation**
   - Unique email enforcement
   - Case-insensitive email checks
   - Valid email format validation

6. **CSRF Protection**
   - Django CSRF token on forms
   - Automatic token validation

### Session Management
- Django session framework
- Login persistence
- Secure logout

---

## 📱 Available URLs/Routes

### Public Routes
- `/` - Homepage with recipe search
- `/help/` - Help page

### Authentication Routes (via Django Allauth)
- `/accounts/signup/` - Registration
- `/accounts/login/` - Login
- `/accounts/logout/` - Logout
- `/accounts/` - Account management

### User Routes (Login Required)
- `/profile/` - Profile setup/edit
- `/dashboard/` - User dashboard
- `/recipes/` - Recipe list
- `/recipes/create/` - Create recipe
- `/recipes/<id>/` - View recipe
- `/recipes/<id>/edit/` - Edit recipe
- `/recipes/<id>/delete/` - Delete recipe
- `/recipes/user/<username>/` - User recipes
- `/meal-plans/` - All meal plans
- `/meal-plan/create/` - Create meal plan
- `/meal-plan/<date>/` - View meal plan by date
- `/meal-plan/<id>/` - View meal plan
- `/meal-plan/<id>/update/` - Update meal plan
- `/meal-plan/<id>/delete/` - Delete meal plan

---

## 🔧 Technologies & Dependencies

### Backend
- **Django 4.2.27** - Web framework
- **Django Allauth 65.13.1** - Authentication
- **Django Crispy Forms 2.5** - Form rendering
- **Django Bootstrap v5 1.0.11** - Bootstrap integration

### Database
- **PostgreSQL** (via psycopg2) - Production database
- **SQLite** - Development database

### Cloud Storage
- **Cloudinary 1.36.0** - Image storage and CDN
- **dj3-cloudinary-storage 0.0.6** - Django Cloudinary integration

### Frontend
- **Bootstrap 5** - Responsive UI
- **Django Summernote 0.8.20.0** - Rich text editor

### Deployment
- **Gunicorn 23.0.0** - WSGI application server
- **WhiteNoise 6.11.0** - Static files serving
- **dj-database-url 0.5.0** - Database URL parsing

### Other
- **python-decouple 3.8** - Environment variables
- **Requests 2.32.5** - HTTP client
- **OAuth 2.0** - Social authentication

---

## 📊 Key Features Summary

| Feature | Status | Details |
|---------|--------|---------|
| User Registration | ✅ Implemented | Custom form with validation |
| Profile Management | ✅ Implemented | Health metrics, BMI, calorie calculation |
| Recipe CRUD | ✅ Implemented | Full create, read, update, delete |
| Meal Planning | ✅ Implemented | Daily meal slots, calorie tracking |
| Nutrition Tracking | ✅ Implemented | Macro tracking, daily summaries |
| Search & Filter | ✅ Implemented | By title, description, category |
| User Authentication | ✅ Implemented | Django Allauth integration |
| Image Upload | ✅ Implemented | Cloudinary integration |
| Responsive Design | ✅ Implemented | Bootstrap 5 |

---

## 🚀 Future Enhancement Opportunities

Based on the current functionality, these features could be added:

1. **Nutritional Analysis**
   - Detailed macro breakdowns for full days
   - Nutritional comparison to goals
   - Charts and visualizations

2. **Meal Prep Scheduling**
   - Weekly meal prep planning
   - Shopping lists from meal plans
   - Bulk cooking recommendations

3. **Social Features**
   - Recipe sharing between users
   - Community recipes
   - User ratings and reviews

4. **API Integration**
   - Third-party nutrition databases
   - Fitness app integration
   - Mobile app support

5. **Advanced Planning**
   - Weekly meal plans
   - Meal templates
   - Dietary restriction filters
   - Allergen management

6. **Notifications & Reminders**
   - Meal reminders
   - Hydration reminders
   - Weekly summary emails

7. **Analytics**
   - Consumption trends
   - Health progress tracking
   - Goal achievement statistics

---

## 👤 User Stories

### Persona 1: "Sarah – Health-Conscious Parent (Age 35)"

**Description:** A working mother managing nutrition for her family of four.

**Needs:**

- Track family meals and calories
- Quick recipe searches by category
- Weekly meal planning
- Nutritional balance monitoring

**Behavior:**

- Plans meals on weekends
- Searches for healthy recipes during lunch breaks
- Needs mobile access while grocery shopping

**User Stories:**

- ✅ As a parent, I want to plan weekly meals so my family eats balanced nutrition
- ✅ As a busy user, I want to filter recipes by category so I can find dinner ideas quickly
- ✅ As a meal planner, I want to see weekly calorie summaries so I can adjust portions
- ✅ As a user, I want to save favorite recipes so I can reuse successful meals

---

### Persona 2: "Mike – Fitness Enthusiast (Age 28)"

**Description:** A gym-goer focused on muscle building and precise macro tracking.

**Needs:**

- Precise protein, carb, and fat tracking
- Custom meal plans matching training days
- BMI and calorie calculations
- Recipe nutritional breakdowns

**Behavior:**

- Logs meals immediately after eating
- Tracks macros to the gram
- Adjusts calorie goals based on workout intensity

**User Stories:**

- ✅ As a fitness user, I want to track macros so I meet my training goals
- ✅ As a user, I want BMI calculations so I monitor my health progress
- ✅ As an athlete, I want to adjust calorie goals based on activity level
- ✅ As a meal tracker, I want to see daily remaining calories so I stay on target

---

### Persona 3: "Emma – Weight Management User (Age 42)"

**Description:** Someone working with a nutritionist to achieve sustainable weight loss.

**Needs:**

- Calorie deficit tracking
- Simple recipe creation
- Daily progress visualization
- Healthy ingredient substitutions

**Behavior:**

- Checks calorie budget multiple times daily
- Prefers simple, low-calorie recipes
- Needs encouragement and progress tracking

**User Stories:**

- ✅ As a weight-loss user, I want to see remaining daily calories so I don't exceed my limit
- ✅ As a user, I want to create custom recipes so I control ingredients
- ✅ As a health tracker, I want to update my weight so my calorie goals adjust automatically
- ✅ As a user, I want visual progress indicators so I stay motivated

---

### Additional User Needs

- 🔹 As a vegetarian, I want to filter recipes by dietary preference
- 🔹 As a diabetic, I want to see carb content prominently displayed
- 🔹 As a mobile user, I want responsive design so I can log meals on-the-go
- 🔹 As a privacy-conscious user, I want secure login so my health data stays private
- 🔹 As a beginner cook, I want step-by-step instructions so recipes are easy to follow

---

## 🧱 Technical Architecture

### **Tech Stack**

- **Backend:** Python 3.x, Django 5.0
- **Frontend:** HTML5, CSS3, JavaScript  
- **Database:**  
  - PostgreSQL (production)  
  - SQLite (development/testing)  
- **Authentication:** Django built-in auth system (with custom user profile extension)
- **Image Handling:** Pillow

---

### **Django Apps Structure**

#### **1. `users`**

**Handles:**

- User registration, login, logout  
- Profile creation & editing  
- Storing user health metrics  
- Calculating BMI & calorie goals  

#### **2. `recipes`**

**Handles:**

- Recipe CRUD operations  
- Ingredient management  
- Nutrition calculations  
- Recipe categories  
- Image uploads  

#### **3. `calories`**

**Handles:**

- Daily calorie tracking  
- Meal plan creation  
- Consumed vs remaining calorie summaries  
- Daily nutrition breakdowns

---

## 🗄️ Database Models

### 👤 **User Profile Model**

```python

healthy_meal_planner/
├── mealapp/              # User authentication & main app
│   ├── recipes/              # Recipe management
│   ├── mealplans/            # Meal planning
│   ├── migrations/
│   ├── models.py         # CaloriesIntake, MealPlan models
│   ├── views.py          # Meal plan views
│   └── urls.py
└── manage.py
```

Understanding Django's is_staff System

#### Regular User (default)

user. is_staff = False       # Cannot access admin panel
user.is_superuser = False   # No special permissions

#### Staff User (can access admin)

user.is_staff = True        # Can access admin panel
user.is_superuser = False   # Limited permissions (set via groups/permissions)

#### Superuser (full access)

user.is_staff = True        # Can access admin panel
user.is_superuser = True    # Full permissions (can do everything)

Extends Django's built-in `User` via One-to-One relationship.

#### **User Profile Fields**

| Field | Type | Description |
| --- | --- | --- |
| user | OneToOneField(User) | Extends Django User model |
| age | IntegerField | User's age |
| gender | CharField | M/F/Other |
| height | FloatField | Height in cm |
| weight | FloatField | Weight in kg |
| activity_level | CharField | Sedentary, Light, Moderate, Active, Very Active |
| daily_calorie_goal | IntegerField | Calculated using BMR + activity multiplier |
| bmi | FloatField (property) | Calculated: weight / (height/100)² |

#### **Methods**

- `calculate_bmi()` → Returns BMI value
- `calculate_daily_calorie_goal()` → Uses Mifflin-St Jeor or Harris-Benedict equation

---

### 🍲 **Recipe Model**

#### **Recipe Fields**

| Field | Type | Description |
| --- | --- | --- |
| title | CharField | Recipe name |
| description | TextField | Recipe overview |
| ingredients | ManyToManyField | Through IngredientQuantity |
| instructions | TextField | Step-by-step cooking directions |
| total_calories | IntegerField | Auto-calculated from ingredients |
| protein | FloatField | Total protein in grams |
| carbs | FloatField | Total carbohydrates in grams |
| fat | FloatField | Total fat in grams |
| serving_size | IntegerField | Number of servings |
| image | ImageField | Recipe photo |
| created_by | ForeignKey(User) | Recipe author |
| category | CharField | Breakfast/Lunch/Dinner/Snack |
| created_at | DateTimeField | Timestamp |
| updated_at | DateTimeField | Last modified |

---

### 🧮 **Ingredient Model**

#### **Ingredient Fields**

| Field | Type | Description |
| --- | --- | --- |
| name | CharField | Ingredient name |
| calories_per_100g | FloatField | Calories per 100g |
| protein_per_100g | FloatField | Protein per 100g |
| carbs_per_100g | FloatField | Carbs per 100g |
| fat_per_100g | FloatField | Fat per 100g |

---

### ⚖️ **IngredientQuantity (Intermediate Model)**

*Stores ingredient amounts per recipe with auto-calculated nutrition.*

#### **Data Fields**

| Field | Type | Description |
| --- | --- | --- |
| recipe | ForeignKey(Recipe) | Associated recipe |
| ingredient | ForeignKey(Ingredient) | Associated ingredient |
| quantity_in_grams | FloatField | Amount used |

#### **Auto-Calculated Properties**

- `calories` = (quantity / 100) × calories_per_100g  
- `protein` = (quantity / 100) × protein_per_100g  
- `carbs` = (quantity / 100) × carbs_per_100g  
- `fat` = (quantity / 100) × fat_per_100g  

---

### 📅 **Meal Plan Model**

#### **Meal Plan Fields**

| Field | Type | Description |
| --- | --- | --- |
| user | ForeignKey(User) | Plan owner |
| date | DateField | Meal date |
| recipes | ManyToManyField(Recipe) | Recipes for the day |
| total_daily_calories | IntegerField | Auto-calculated sum |
| remaining_calories | IntegerField | daily_goal − total_daily_calories |

---

## 🎨 Design

### Color Palette

Designed for health, freshness, and clarity.

| Color | Hex Code | Usage |
| --- | --- | --- |
| **Primary Green** | `#4CAF50` | Main brand, success states, healthy theme |
| **Accent Orange** | `#FF9800` | Call-to-action buttons, highlights |
| **Background Light** | `#F5F5F5` | Page backgrounds, cards |
| **Text Dark** | `#333333` | Main text, high readability |
| **Success** | `#2ECC71` | Completed goals, positive feedback |
| **Warning** | `#E74C3C` | Calorie warnings, errors |
| **White** | `#FFFFFF` | Cards, modals, clean surfaces |

### Typography

#### Primary Font: "Roboto"

- Used for headings and navigation
- Modern, clean, professional
- Excellent web readability

#### Secondary Font: "Open Sans"

- Body text and descriptions
- High legibility at small sizes
- Friendly, approachable

**Fallback:** Arial, sans-serif

### UI Elements

#### Buttons

- **Primary:** Green with white text, rounded corners
- **Secondary:** Outlined green, transparent background
- **Danger:** Red for delete actions
- **States:** default, hover (slight darken), active (pressed), disabled (greyed)

#### Cards

- White background with subtle shadow
- Rounded corners (8px border-radius)
- Recipe cards display image, title, calories, category

#### Forms

- Clean inputs with border focus states
- Django Crispy Forms for consistent styling
- Inline validation messages

#### Progress Bars

- Visual calorie tracking (consumed/remaining)
- Color-coded: green (under goal), orange (near limit), red (over limit)

---

<details>

<summary> 🧱 Wireframes</summary>

[![All devices](mealapp/static/images/wireframe_all_in_one.png)](mealapp/static/images/wireframe_all_in_one.png)

```ruby
 Homepage
```

[![Homepage](mealapp/static/images/wireframe_home.png)](mealapp/static/images/wireframe_home.png)

```ruby
 Dashboard for user profile
```

[![Dashboard](mealapp/static/images/wireframe_profile.png)](mealapp/static/images/wireframe_profile.png)

Help page

[![Help page](mealapp/static/images/wireframe_help.png)](mealapp/static/images/wireframe_help.png)

Sign up page

[![Sign up page](mealapp/static/images/wireframe_signup.png)](mealapp/static/images/wireframe_signup.png)

</details>

**Planned Views:**

- **Dashboard:** Daily calorie summary, recent recipes, quick meal log
- **Recipe List:** Grid/card layout with filters (category, calories)
- **Recipe Detail:** Image, ingredients table, nutrition facts, instructions
- **Meal Planner:** Calendar view with daily totals
- **Profile:** User stats, BMI calculator, goal settings

---

## 🚀 Features

### 1. **User Registration & Authentication**

Users can create accounts, login securely, and manage profiles.

**Implementation Details:**

- Django built-in authentication
- Custom UserProfile model extension
- Password validation and security

**Key Functionality:**

- Register new account
- Login/Logout
- Password reset via email
- Profile creation on first login

---

### 2. **BMI & Calorie Goal Calculator**

Automatically calculates personalized daily calorie targets.

**Implementation Details:**

- BMI formula: `weight (kg) / (height (m))²`
- Calorie goal using **Mifflin-St Jeor Equation:**
  - **BMR (Men):** 10 × weight + 6.25 × height − 5 × age + 5
  - **BMR (Women):** 10 × weight + 6.25 × height − 5 × age − 161
- Activity multipliers:
  - Sedentary: BMR × 1.2
  - Light: BMR × 1.375
  - Moderate: BMR × 1.55
  - Active: BMR × 1.725
  - Very Active: BMR × 1.9

**Key Functionality:**

- Auto-calculate on profile save
- Update when weight/activity changes
- Display in user dashboard

---

### 3. **Recipe Management (CRUD)**

Create, browse, edit, and delete custom recipes.

**Implementation Details:**

- Django forms with validation
- Image upload with Pillow
- ManyToMany ingredient relationships
- Auto-calculated nutrition totals

**Key Functionality:**

- Add recipes with multiple ingredients
- Upload recipe photos
- Edit/delete own recipes
- View all recipes (public or user-filtered)
- Filter by category (Breakfast/Lunch/Dinner/Snack)

---

### 4. **Ingredient Database**

Pre-populated ingredient list with nutritional values.

**Implementation Details:**

- Admin-managed ingredient library
- Nutritional data per 100g standard
- Extensible for user additions

**Key Functionality:**

- Search ingredients when creating recipes
- View nutrition per ingredient
- Add custom ingredients (future feature)

---

### 5. **Calorie & Macro Tracking**

Log daily meals and monitor nutrition intake.

**Implementation Details:**

- MealPlan model links users, dates, and recipes
- Auto-sum calories from added recipes
- Calculate remaining daily calories

**Key Functionality:**

- Add recipes to daily meal plan
- View total calories consumed
- See macro breakdown (protein/carbs/fat)
- Visual progress bars
- Edit/remove logged meals

---

### 6. **Meal Planning Calendar**

Plan meals in advance with visual calendar interface.

**Implementation Details:**

- Date-based meal organization
- Daily calorie summaries
- Week/month view options (future)

**Key Functionality:**

- Select date and add recipes
- View weekly meal plan
- Duplicate previous days' meals
- Export meal plan (future)

---

### 7. **Responsive Design**

Mobile-first, accessible across all devices.

**Implementation Details:**

- CSS Grid and Flexbox layouts
- Media queries for breakpoints
- Touch-friendly buttons on mobile

**Key Functionality:**

- Works on desktop, tablet, mobile
- Optimized forms for mobile input
- Readable text at all screen sizes

---

## 🧪 Testing

### Manual Testing Checklist

#### **Authentication & Profiles**

- [x] User can register successfully
- [x] User can login with correct credentials
- [x] User receives error with wrong password
- [x] Profile is auto-created on registration
- [x] BMI calculates correctly
- [x] Calorie goal updates when activity changes
- [x] User can logout

#### **Recipe Management**

- [x] User can create recipe with ingredients
- [x] Recipe image uploads successfully
- [x] Total calories auto-calculate
- [x] Macros (protein/carbs/fat) sum correctly
- [x] User can edit own recipes
- [x] User can delete own recipes
- [x] Recipes display by category

#### **Calorie Tracking**

- [x] User can add recipe to meal plan
- [x] Daily total calories calculate correctly
- [x] Remaining calories display accurately
- [x] User can remove meals from plan
- [x] Meal plan persists across sessions

#### **Responsiveness**

- [x] Layout works on mobile (375px)
- [x] Layout works on tablet (768px)
- [x] Layout works on desktop (1920px)
- [x] Forms are usable on touchscreens

---

### Automated Testing

#### **Django Unit Tests**

```python
# Example test structure
tests/
├── test_models.py    # BMI calculation, nutrition totals
├── test_views.py     # HTTP responses, authentication
├── test_forms.py     # Form validation
```

**Coverage Goals:**

- Models: 90%+
- Views: 80%+
- Forms: 85%+

#### **Code Quality**

- **PEP8 Compliance:** All Python files
- **HTML Validator (W3C):** All templates
- **CSS Validator (Jigsaw):** All stylesheets
- **Accessibility (WAVE):** All public pages

#### **Performance (Lighthouse)**

- Performance: Target 90+
- Accessibility: Target 95+
- Best Practices: Target 90+
- SEO: Target 95+

### Known Bugs & Issues

#### **Fixed Issues**

✅ **Issue #1:** Image upload failing on production  
**Solution:** Configured media file handling with WhiteNoise

✅ **Issue #2:** BMI calculation returning None  
**Solution:** Added height/weight validation before calculation

#### **Unfixed Issues**

⚠️ **Issue #3:** Ingredient search slow with large database  
**Status:** Planning to add database indexing  
**Workaround:** Limit ingredient list to 500 most common items

---

## 🚀 Deployment

### **Local Development Setup**

```bash
# 1. Clone the repository
git clone https://github.com/darakhshanda/healthy_meal_planner.git
cd healthy_meal_planner

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variables
# Create env.py file with:
# SECRET_KEY = 'your-secret-key'
# DEBUG = True

# 6. Run migrations
python manage.py makemigrations
python manage.py migrate

# 7. Create superuser
python manage.py createsuperuser

# 8. Load ingredient fixtures (optional)
python manage.py loaddata ingredients.json

# 9. Run development server
python manage.py runserver

# Visit: http://127.0.0.1:8000/
```

---

### **Production Deployment**

#### **Platform Options:**

- Heroku
- Railway
- PythonAnywhere
- DigitalOcean

#### **Production Checklist:**

- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use PostgreSQL database
- [ ] Set up static file serving (WhiteNoise/AWS S3)
- [ ] Configure media file storage
- [ ] Set secure `SECRET_KEY`
- [ ] Enable HTTPS
- [ ] Set up environment variables
- [ ] Configure email backend (for password reset)

#### **Environment Variables:**

```bash
SECRET_KEY=<random-50-char-string>
DEBUG=False
DATABASE_URL=<postgresql-connection-string>
ALLOWED_HOSTS=yourdomain.com
```

---

## 🛠️ Technologies Used

### **Languages**

- **Python 3.11** – Backend logic
- **HTML5** – Structure
- **CSS3** – Styling
- **JavaScript** – Interactive elements

### **Frameworks & Libraries**

#### **Backend**

- **Django 5.0** – Web framework
- **Django Crispy Forms** – Form rendering
- **Pillow** – Image processing
- **psycopg2** – PostgreSQL adapter

#### **Database**

- **PostgreSQL** – Production database
- **SQLite** – Development database

#### **Frontend**

- **Bootstrap 5** (optional) – UI components
- **Font Awesome** – Icons
- **Google Fonts** – Typography (Roboto, Open Sans)

### **Development Tools**

- **Git / GitHub** – Version control
- **VS Code** – IDE
- **Django Debug Toolbar** – Development debugging
- **Postman** – API testing (if REST API added)

### **Hosting & Deployment**

- **Heroku / Railway** – Platform as a Service
- **WhiteNoise** – Static file serving
- **Cloudinary / AWS S3** – Media file storage (optional)

---

## 🧠 Best Practices & Architecture Notes

### **Django Signals**

- Auto-create `UserProfile` when `User` is created
- Recalculate recipe nutrition when ingredients change
- Update meal plan totals when recipes are added/removed

### **Security**

- CSRF protection on all forms
- SQL injection prevention via Django ORM
- XSS protection in templates
- Secure password hashing (PBKDF2)

### **Database Optimization**

- Use `select_related()` for foreign keys
- Use `prefetch_related()` for many-to-many
- Add database indexes on frequently queried fields

### **Code Organization**

- Separate settings for development/production
- Use environment variables for secrets
- Keep views thin, logic in models/services
- Write reusable template tags

### **Future Enhancements**

- Django REST Framework API for mobile apps
- Recipe sharing and social features
- Barcode scanning for packaged foods
- Integration with fitness trackers (Fitbit, Apple Health)
- Multi-language support (i18n)

---

## 📚 Credits

### **Code References**

- [Django Documentation](https://docs.djangoproject.com/)
- [Real Python Tutorials](https://realpython.com/)
- [The Meal DB](https://www.themealdb.com/) for recipies and images
- MDN Web Docs for JavaScript

### **Resources**

- **Nutrition Data:** [USDA FoodData Central](https://fdc.nal.usda.gov/)
- **BMI Guidelines:** [WHO BMI Classifications](https://www.who.int/health-topics/obesity)
- **Calorie Calculations:** Mifflin-St Jeor Equation
- **Recipe Inspiration:** BBC Good Food, AllRecipes

### **Assets**

- **Icons:** Font Awesome
- **Fonts:** Google Fonts (Roboto, Open Sans)
- **Stock Images:** Unsplash, Pexels

---

## 🙏 Acknowledgments

- **Code Institute / Mentor:** For project guidance and support
- **Django Community:** For excellent documentation and support

---

## 📄 License

This project is for learnig purposes and woould appreciate suggestions and contributions.

---

## 📞 Contact

**Maintainer:** darakhshanda  
**Repository:** [github.com/darakhshanda/healthy_meal_planner](https://github.com/darakhshanda/healthy_meal_planner)  
**Issues:** [Report a bug](https://github.com/darakhshanda/healthy_meal_planner/issues)

---

**⭐ If you find this project helpful, please give it a star on GitHub!**
