# 🚀 Quick Start Guide

## Employee Promotion Analysis - Full Stack Application

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **MongoDB** - [Download](https://www.mongodb.com/try/download/community) or use [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

---

## 🏃 Quick Start (5 minutes)

### 1. Start MongoDB

**Option A: Local MongoDB**
```powershell
# Start MongoDB service
net start MongoDB
```

**Option B: MongoDB Atlas (Cloud)**
- Create a free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- Create a cluster and get your connection string
- Update `.env` with your connection string

---

### 2. Start Backend

```powershell
# Navigate to backend directory
cd backend

# Activate virtual environment (already created)
.\venv\Scripts\Activate

# Load data into MongoDB (first time only)
python load_data.py

# Start FastAPI server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc

---

### 3. Start Frontend (New Terminal)

```powershell
# Navigate to frontend directory
cd frontend

# Start Vite dev server (npm install already done)
npm run dev
```

Frontend will be available at:
- **App**: http://localhost:5173

---

## 📋 What You Can Do Now

### 1. Register/Login
- Visit http://localhost:5173
- Click "Sign up" and create an account
- Login with your credentials

### 2. Explore Features

**Dashboard** (`/`)
- View overall statistics
- See promotion rates by department
- Key insights from data analysis

**Employees** (`/employees`)
- View all employee records
- Search and filter employees
- Add/Edit/Delete employees
- Bulk upload CSV files

**Predictions** (`/predictions`)
- Predict single employee promotion likelihood
- Input employee data and get ML prediction
- View confidence scores

**Analytics** (`/analytics`)
- Training score analysis (promoted vs not promoted)
- Previous rating analysis
- Run business simulations (6 scenarios)
- See impact of improvements on promotion rate and costs

**Recommendations** (`/recommendations`)
- View data-driven recommendations
- See pros/cons of each strategy
- Implementation timeline
- Expected ROI

---

## 🔧 Configuration

### Backend (.env file)

The `.env` file in the `backend/` directory contains:

```env
# MongoDB
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=employee_promotion

# JWT Authentication
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Business Metrics
AVERAGE_HIRING_COST=800
PROMOTION_RATE_TARGET=25
COST_REDUCTION_TARGET=50
```

**Important:** Change `SECRET_KEY` in production!

---

## 📊 Data

### Sample Data
- **train.csv**: 54,808 employee records with 13 features
- Located in project root directory
- Automatically loaded by `load_data.py`

### Features (13 total)
1. `employee_id` - Unique identifier
2. `department` - 9 departments
3. `region` - Geographic region
4. `education` - Education level
5. `gender` - m/f
6. `recruitment_channel` - How hired
7. `no_of_trainings` - Number of trainings attended
8. `age` - Employee age
9. `previous_year_rating` - Performance rating (1-5)
10. `length_of_service` - Years at company
11. `awards_won` - Number of awards (0/1)
12. `avg_training_score` - Average training score (0-100)
13. `is_promoted` - Target variable (0/1)

---

## 🧪 Testing the API

### Using Swagger UI (Recommended)

1. Go to http://localhost:8000/docs
2. Click on any endpoint
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"

### Using cURL

**Register a user:**
```powershell
curl -X POST http://localhost:8000/api/auth/register `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"test@example.com\",\"password\":\"password123\",\"full_name\":\"Test User\"}'
```

**Login:**
```powershell
curl -X POST http://localhost:8000/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"test@example.com\",\"password\":\"password123\"}'
```

**Get dashboard stats:**
```powershell
curl http://localhost:8000/api/analytics/dashboard `
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 🐛 Troubleshooting

### Backend Issues

**Issue:** `ModuleNotFoundError`
```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Issue:** MongoDB connection error
```powershell
# Check if MongoDB is running
mongosh

# Or check Windows service
Get-Service MongoDB
```

**Issue:** Port 8000 already in use
```powershell
# Use different port
python -m uvicorn app.main:app --reload --port 8001
```

### Frontend Issues

**Issue:** Port 5173 already in use
```powershell
# Kill the process or use different port
# Edit vite.config.js and change port
```

**Issue:** API calls failing (CORS)
- Check backend is running
- Verify `.env` CORS_ORIGINS includes frontend URL
- Check browser console for errors

**Issue:** Blank page
```powershell
# Clear cache and rebuild
npm run build
npm run dev
```

---

## 📦 Project Structure

```
Employee Promotion Analysis/
│
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── routes/            # API endpoints
│   │   ├── models/            # Pydantic models
│   │   ├── services/          # Business logic
│   │   ├── config.py          # Configuration
│   │   ├── database.py        # MongoDB connection
│   │   └── main.py            # FastAPI app
│   ├── venv/                  # Virtual environment
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables
│   └── load_data.py           # Data loading script
│
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── pages/             # Page components
│   │   ├── components/        # Reusable components
│   │   ├── services/          # API client
│   │   ├── App.jsx            # Main app component
│   │   └── main.jsx           # Entry point
│   ├── public/                # Static assets
│   ├── package.json           # NPM dependencies
│   └── vite.config.js         # Vite configuration
│
├── train.csv                   # Training data
├── test.csv                    # Test data
├── README.md                   # Full documentation
├── QUICKSTART.md              # This file
└── PROJECT_SUMMARY.md         # Project overview
```

---

## 🎯 Next Steps

1. **Explore the Data**
   - Navigate to Employees page
   - Search and filter records
   - View employee details

2. **Make Predictions**
   - Go to Predictions page
   - Enter employee information
   - Get promotion likelihood

3. **Run Simulations**
   - Open Analytics page
   - Select a scenario
   - See potential impact

4. **Review Recommendations**
   - Check Recommendations page
   - Understand improvement strategies
   - Plan implementation

---

## 💡 Tips

- **Data Persistence**: MongoDB keeps data even after restart
- **Hot Reload**: Both backend and frontend auto-reload on changes
- **API Docs**: Always available at `/docs` - great for testing
- **Error Handling**: Check browser console and backend terminal for errors
- **Performance**: First load may be slow while ML model initializes

---

## 🔐 Security Notes

⚠️ **For Development Only**

This setup is for development. For production:

1. Use strong `SECRET_KEY` (generate with `openssl rand -hex 32`)
2. Enable HTTPS
3. Use production-grade MongoDB (Atlas)
4. Set proper CORS origins
5. Add rate limiting
6. Implement proper logging
7. Use environment-specific configs
8. Add input validation
9. Enable authentication on all routes
10. Regular security audits

---

## 📞 Support

If you encounter issues:

1. Check this guide
2. Review README.md
3. Check backend terminal for errors
4. Check browser console for frontend errors
5. Verify all services are running
6. Ensure MongoDB has data (run `load_data.py`)

---

## 🎉 Success!

You should now have a fully functional Employee Promotion Analysis system running locally!

- Backend API: ✅
- Frontend UI: ✅
- MongoDB: ✅
- Sample Data: ✅

Happy analyzing! 🚀
