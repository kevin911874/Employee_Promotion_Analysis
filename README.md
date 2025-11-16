# Employee Promotion Analysis System

A full-stack web application for predicting employee promotions using machine learning, with comprehensive analytics and business insights.

## 📋 Project Overview

This system helps HR departments:
- **Predict** which employees are likely to be promoted
- **Analyze** key factors affecting promotions (training scores, previous ratings, etc.)
- **Simulate** business outcomes with different improvement strategies
- **Recommend** actionable improvements to increase promotion rates
- **Reduce** external hiring costs by up to 50%

### Key Features

✅ **Employee Management** - CRUD operations for employee data  
✅ **ML Predictions** - Random Forest model with 99% precision  
✅ **Analytics Dashboard** - Real-time metrics and visualizations  
✅ **Sensitivity Analysis** - See how changes affect promotion rates  
✅ **Business Simulations** - Test different improvement scenarios  
✅ **Recommendations** - Evidence-based suggestions for improvement  
✅ **RESTful API** - Complete backend API with MongoDB  
✅ **Responsive UI** - Modern React frontend with Tailwind CSS  

## 🏗️ Architecture

```
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── routes/         # API endpoints
│   │   ├── models/         # Pydantic models
│   │   ├── services/       # Business logic & ML
│   │   ├── config.py       # Configuration
│   │   ├── database.py     # MongoDB connection
│   │   └── main.py         # FastAPI app
│   └── requirements.txt
│
├── frontend/               # React Frontend
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   ├── App.jsx        # Main app component
│   │   └── main.jsx       # Entry point
│   └── package.json
│
├── train.csv              # Training dataset (54,808 employees)
├── test.csv               # Test dataset
└── Employee Promotion Prediction.ipynb  # ML model development
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- MongoDB 4.4+
- pip and npm/yarn

### Backend Setup

1. **Navigate to backend directory**
```powershell
cd backend
```

2. **Create virtual environment**
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

3. **Install dependencies**
```powershell
pip install -r requirements.txt
```

4. **Configure environment**
```powershell
cp .env.example .env
# Edit .env with your MongoDB URL and settings
```

5. **Start MongoDB** (if not running)
```powershell
# Windows: Start MongoDB service
net start MongoDB
```

6. **Run the application**
```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`  
API Documentation: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**
```powershell
cd frontend
```

2. **Install dependencies**
```powershell
npm install
```

3. **Start development server**
```powershell
npm run dev
```

Frontend will be available at: `http://localhost:3000`

### Database Setup

1. **Load initial data** (Optional)
```python
# Run this script to load train.csv data into MongoDB
python scripts/load_data.py
```

## 📊 Dataset Features

The system analyzes 12 employee features:

| Feature | Description | Type |
|---------|-------------|------|
| employee_id | Unique identifier | Integer |
| department | Employee department | Categorical |
| region | Work region | Categorical |
| education | Education level | Categorical |
| gender | Gender (m/f) | Categorical |
| recruitment_channel | How recruited | Categorical |
| no_of_trainings | Trainings completed | Numerical |
| age | Employee age | Numerical |
| previous_year_rating | Last year's rating (1-5) | Numerical |
| length_of_service | Years of service | Numerical |
| awards_won | Awards (0/1) | Binary |
| avg_training_score | Training score (0-100) | Numerical |
| **is_promoted** | Promotion status (Target) | Binary |

## 🎯 Key Insights from Analysis

### Top Factors for Promotion

1. **Average Training Score** (Most Important)
   - Promoted employees: Mean score = 71
   - Non-promoted employees: Mean score = 62

2. **Previous Year Rating**
   - Promoted employees: Median = 4
   - Non-promoted employees: Median = 3

3. **Awards Won**
4. **No of Trainings**
5. **Region & Recruitment Channel**

### Business Impact Simulations

| Improvement | Promotion Rate ↑ | Cost Reduction |
|-------------|------------------|----------------|
| 10% Training Score | +3.9% | -4.45% |
| 20% Training Score | +8.12% | -9.74% |
| 30% Training Score | +10.43% | -12.87% |
| 10% Rating + 20% Training | +12.78% | -16.24% |
| 10% Rating + 30% Training | +16.11% | -21.38% |

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Employees
- `GET /api/employees` - List all employees
- `GET /api/employees/{id}` - Get employee by ID
- `POST /api/employees` - Create employee
- `PUT /api/employees/{id}` - Update employee
- `DELETE /api/employees/{id}` - Delete employee
- `POST /api/employees/bulk-upload` - Bulk upload
- `GET /api/employees/stats/summary` - Get statistics

### Predictions
- `POST /api/predictions/predict` - Predict single employee
- `POST /api/predictions/predict-batch` - Batch predictions
- `GET /api/predictions/history/{id}` - Prediction history
- `GET /api/predictions/recent` - Recent predictions

### Analytics
- `GET /api/analytics/dashboard` - Dashboard stats
- `GET /api/analytics/training-score-analysis` - Training analysis
- `GET /api/analytics/previous-rating-analysis` - Rating analysis
- `POST /api/analytics/sensitivity-analysis` - Sensitivity analysis
- `POST /api/analytics/business-simulation` - Business simulation
- `GET /api/analytics/recommendations` - Get recommendations

## 💡 Recommendations Implemented

### Training Improvements
1. **Build Corporate LMS** - Learning Management System
2. **Mobile-Friendly Access** - Anytime, anywhere learning
3. **Leadership Training** - Soft skills development
4. **Relevant Content** - Survey-based course selection

### Performance Rating Improvements
1. **Transparent Feedback** - Clear, constructive reviews
2. **Objective Criteria** - Data-driven assessments
3. **Active Listening** - Manager training
4. **Right Questions** - Structured review process

## 📈 Model Performance

- **Algorithm**: Random Forest Classifier
- **Precision**: 99% (on test set)
- **Training**: SMOTE for handling imbalanced data
- **Features**: 58 (after one-hot encoding)
- **Validation**: Cross-validation with hyperparameter tuning

## 🎨 Frontend Pages

1. **Dashboard** - Overview metrics and charts
2. **Employees** - Manage employee records
3. **Predictions** - Make and view predictions
4. **Analytics** - Deep dive into data insights
5. **Recommendations** - Actionable improvements

## 🔐 Security

- JWT-based authentication
- Password hashing with bcrypt
- CORS protection
- Input validation with Pydantic
- MongoDB injection prevention

## 🛠️ Technologies Used

### Backend
- FastAPI (Python web framework)
- MongoDB (Database)
- Scikit-learn (Machine Learning)
- Pandas & NumPy (Data processing)
- SMOTE (Imbalanced data handling)
- Python-Jose (JWT)
- Passlib (Password hashing)

### Frontend
- React 18
- React Router (Navigation)
- TanStack Query (Data fetching)
- Chart.js & Recharts (Visualizations)
- Tailwind CSS (Styling)
- Axios (HTTP client)
- Lucide React (Icons)

## 📝 Environment Variables

### Backend (.env)
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=employee_promotion_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=http://localhost:3000
```

## 🧪 Testing

```powershell
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📦 Deployment

### Docker Deployment

```powershell
# Build and run with Docker Compose
docker-compose up -d
```

### Manual Deployment

1. Set production environment variables
2. Build frontend: `npm run build`
3. Serve static files with nginx
4. Run backend with gunicorn/uvicorn
5. Use MongoDB Atlas for database

## 📚 Additional Resources

- [Project Presentation Deck](./Employee%20Promotion%20Deck%20(2).pdf)
- [Jupyter Notebook](./Employee%20Promotion%20Prediction.ipynb)
- [API Documentation](http://localhost:8000/docs)

## 👥 Credits

**Created by**: Kevin Mayani
**Contact**: kevinmayani89@gmail.com

## 📄 License

This project is for educational and portfolio purposes.

## 🙏 Acknowledgments

- Bandung Institute of Technology, School of Business and Management
- Rakamin Data Science Bootcamp
- References cited in the presentation deck

---

**Goals Achieved:**
✅ Increase promotion rate up to 25%  
✅ Reduce hiring costs up to 50%  
✅ Provide data-driven insights  
✅ Deliver actionable recommendations  

For questions or support, please open an issue on GitHub.

