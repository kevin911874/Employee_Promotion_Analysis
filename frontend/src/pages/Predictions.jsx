import { useState } from 'react';
import { predictionsAPI } from '../services/api';
import { TrendingUp, Users, CheckCircle, XCircle } from 'lucide-react';

export default function Predictions() {
  const [activeTab, setActiveTab] = useState('single');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  
  const [formData, setFormData] = useState({
    department: '',
    region: '',
    education: '',
    gender: '',
    recruitment_channel: '',
    no_of_trainings: '',
    age: '',
    previous_year_rating: '',
    length_of_service: '',
    awards_won: '',
    avg_training_score: '',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      const response = await predictionsAPI.predictSingle(formData);
      setResult(response.data);
    } catch (error) {
      console.error('Prediction failed:', error);
      alert('Prediction failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Promotion Predictions</h1>
        <p className="text-gray-600">Predict employee promotion likelihood using ML model</p>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow mb-6">
        <div className="border-b border-gray-200">
          <div className="flex">
            <button
              onClick={() => setActiveTab('single')}
              className={`px-6 py-3 font-medium ${
                activeTab === 'single'
                  ? 'border-b-2 border-primary-600 text-primary-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              <TrendingUp className="w-5 h-5 inline mr-2" />
              Single Prediction
            </button>
            <button
              onClick={() => setActiveTab('batch')}
              className={`px-6 py-3 font-medium ${
                activeTab === 'batch'
                  ? 'border-b-2 border-primary-600 text-primary-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              <Users className="w-5 h-5 inline mr-2" />
              Batch Prediction
            </button>
          </div>
        </div>

        <div className="p-6">
          {activeTab === 'single' ? (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Form */}
              <div>
                <h3 className="text-lg font-semibold mb-4">Employee Information</h3>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">Department</label>
                    <input
                      type="text"
                      name="department"
                      value={formData.department}
                      onChange={handleChange}
                      className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500"
                      placeholder="e.g., Sales & Marketing"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">Region</label>
                    <input
                      type="text"
                      name="region"
                      value={formData.region}
                      onChange={handleChange}
                      className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500"
                      placeholder="e.g., region_2"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">Education</label>
                    <select
                      name="education"
                      value={formData.education}
                      onChange={handleChange}
                      className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500"
                      required
                    >
                      <option value="">Select Education</option>
                      <option value="Bachelor's">Bachelor's</option>
                      <option value="Master's & above">Master's & above</option>
                      <option value="Below Secondary">Below Secondary</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">Gender</label>
                    <select
                      name="gender"
                      value={formData.gender}
                      onChange={handleChange}
                      className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500"
                      required
                    >
                      <option value="">Select Gender</option>
                      <option value="m">Male</option>
                      <option value="f">Female</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">Recruitment Channel</label>
                    <input
                      type="text"
                      name="recruitment_channel"
                      value={formData.recruitment_channel}
                      onChange={handleChange}
                      className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500"
                      placeholder="e.g., sourcing"
                      required
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium mb-1">No. of Trainings</label>
                      <input
                        type="number"
                        name="no_of_trainings"
                        value={formData.no_of_trainings}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500"
                        required
                        min="0"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium mb-1">Age</label>
                      <input
                        type="number"
                        name="age"
                        value={formData.age}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500"
                        required
                        min="18"
                        max="70"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium mb-1">Previous Year Rating</label>
                      <input
                        type="number"
                        name="previous_year_rating"
                        value={formData.previous_year_rating}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500"
                        min="1"
                        max="5"
                        step="0.1"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium mb-1">Length of Service</label>
                      <input
                        type="number"
                        name="length_of_service"
                        value={formData.length_of_service}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500"
                        required
                        min="0"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium mb-1">Awards Won</label>
                      <input
                        type="number"
                        name="awards_won"
                        value={formData.awards_won}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500"
                        required
                        min="0"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium mb-1">Avg Training Score</label>
                      <input
                        type="number"
                        name="avg_training_score"
                        value={formData.avg_training_score}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500"
                        required
                        min="0"
                        max="100"
                      />
                    </div>
                  </div>

                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-primary-600 text-white py-2 px-4 rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
                  >
                    {loading ? 'Predicting...' : 'Predict Promotion'}
                  </button>
                </form>
              </div>

              {/* Result */}
              <div>
                <h3 className="text-lg font-semibold mb-4">Prediction Result</h3>
                {result ? (
                  <div className="bg-white border-2 border-gray-200 rounded-lg p-6">
                    <div className="text-center mb-6">
                      {result.prediction === 1 ? (
                        <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-2" />
                      ) : (
                        <XCircle className="w-16 h-16 text-red-500 mx-auto mb-2" />
                      )}
                      <h4 className="text-2xl font-bold text-gray-900 mb-2">
                        {result.prediction === 1 ? 'Likely to be Promoted' : 'Unlikely to be Promoted'}
                      </h4>
                      <p className="text-gray-600">
                        Confidence: {(result.confidence * 100).toFixed(1)}%
                      </p>
                    </div>

                    <div className="space-y-3">
                      <div className="flex justify-between border-b pb-2">
                        <span className="text-gray-600">Promotion Score</span>
                        <span className="font-semibold">{result.promotion_score?.toFixed(2)}</span>
                      </div>
                      <div className="flex justify-between border-b pb-2">
                        <span className="text-gray-600">Training Score</span>
                        <span className="font-semibold">{formData.avg_training_score}</span>
                      </div>
                      <div className="flex justify-between border-b pb-2">
                        <span className="text-gray-600">Previous Rating</span>
                        <span className="font-semibold">{formData.previous_year_rating || 'N/A'}</span>
                      </div>
                    </div>

                    {result.recommendation && (
                      <div className="mt-4 p-4 bg-blue-50 rounded-lg">
                        <p className="text-sm text-blue-800">
                          <strong>Recommendation:</strong> {result.recommendation}
                        </p>
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                    <TrendingUp className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                    <p className="text-gray-500">Fill in the form and click predict to see results</p>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="text-center py-12">
              <Users className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-700 mb-2">Batch Prediction</h3>
              <p className="text-gray-500 mb-4">Upload a CSV file with multiple employees for batch predictions</p>
              <button className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700">
                Upload CSV File
              </button>
              <p className="text-xs text-gray-400 mt-2">Coming soon...</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
