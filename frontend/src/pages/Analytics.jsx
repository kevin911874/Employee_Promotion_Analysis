import { useState, useEffect } from 'react';
import { analyticsAPI } from '../services/api';
import { BarChart3, TrendingUp, Activity, Sliders } from 'lucide-react';

export default function Analytics() {
  const [trainingAnalysis, setTrainingAnalysis] = useState(null);
  const [ratingAnalysis, setRatingAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [simulationResult, setSimulationResult] = useState(null);
  const [simulationLoading, setSimulationLoading] = useState(false);

  const [simulationForm, setSimulationForm] = useState({
    scenario: 'training_10',
    training_improvement: 10,
    rating_improvement: 0,
  });

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const [training, rating] = await Promise.all([
        analyticsAPI.getTrainingScoreAnalysis(),
        analyticsAPI.getPreviousRatingAnalysis(),
      ]);
      setTrainingAnalysis(training.data);
      setRatingAnalysis(rating.data);
    } catch (error) {
      console.error('Failed to fetch analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSimulation = async (e) => {
    e.preventDefault();
    setSimulationLoading(true);
    
    try {
      const response = await analyticsAPI.businessSimulation(simulationForm);
      setSimulationResult(response.data);
    } catch (error) {
      console.error('Simulation failed:', error);
      alert('Simulation failed');
    } finally {
      setSimulationLoading(false);
    }
  };

  const scenarios = [
    { value: 'training_10', label: '10% Training Score Increase' },
    { value: 'training_20', label: '20% Training Score Increase' },
    { value: 'training_30', label: '30% Training Score Increase' },
    { value: 'rating_10', label: '10% Previous Rating Increase' },
    { value: 'combined_20_10', label: 'Combined: 20% Training + 10% Rating' },
    { value: 'combined_30_10', label: 'Combined: 30% Training + 10% Rating' },
  ];

  if (loading) {
    return (
      <div className="p-6">
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading analytics...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Analytics & Insights</h1>
        <p className="text-gray-600">Explore data patterns and run business simulations</p>
      </div>

      {/* Training Score Analysis */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="flex items-center gap-2 mb-4">
          <BarChart3 className="w-6 h-6 text-primary-600" />
          <h2 className="text-xl font-bold">Training Score Analysis</h2>
        </div>
        
        {trainingAnalysis && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-lg">
              <p className="text-sm text-green-700 font-medium mb-2">Promoted Employees</p>
              <p className="text-3xl font-bold text-green-900">
                {trainingAnalysis.promoted?.mean?.toFixed(1)}
              </p>
              <p className="text-xs text-green-600 mt-1">Average Training Score</p>
            </div>

            <div className="bg-gradient-to-br from-red-50 to-red-100 p-6 rounded-lg">
              <p className="text-sm text-red-700 font-medium mb-2">Not Promoted</p>
              <p className="text-3xl font-bold text-red-900">
                {trainingAnalysis.not_promoted?.mean?.toFixed(1)}
              </p>
              <p className="text-xs text-red-600 mt-1">Average Training Score</p>
            </div>

            <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-lg">
              <p className="text-sm text-blue-700 font-medium mb-2">Difference</p>
              <p className="text-3xl font-bold text-blue-900">
                {(trainingAnalysis.promoted?.mean - trainingAnalysis.not_promoted?.mean).toFixed(1)}
              </p>
              <p className="text-xs text-blue-600 mt-1">Points Higher</p>
            </div>
          </div>
        )}

        <div className="mt-6 p-4 bg-blue-50 rounded-lg">
          <p className="text-sm text-blue-800">
            <strong>Key Insight:</strong> Employees who were promoted have significantly higher training scores 
            (average {trainingAnalysis?.promoted?.mean?.toFixed(1)}) compared to those who weren't promoted 
            (average {trainingAnalysis?.not_promoted?.mean?.toFixed(1)}). This indicates training performance 
            is a strong predictor of promotion.
          </p>
        </div>
      </div>

      {/* Previous Rating Analysis */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="flex items-center gap-2 mb-4">
          <TrendingUp className="w-6 h-6 text-secondary-600" />
          <h2 className="text-xl font-bold">Previous Year Rating Analysis</h2>
        </div>
        
        {ratingAnalysis && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-6 rounded-lg">
              <p className="text-sm text-purple-700 font-medium mb-2">Promoted Employees</p>
              <p className="text-3xl font-bold text-purple-900">
                {ratingAnalysis.promoted?.median?.toFixed(1)}
              </p>
              <p className="text-xs text-purple-600 mt-1">Median Rating</p>
            </div>

            <div className="bg-gradient-to-br from-orange-50 to-orange-100 p-6 rounded-lg">
              <p className="text-sm text-orange-700 font-medium mb-2">Not Promoted</p>
              <p className="text-3xl font-bold text-orange-900">
                {ratingAnalysis.not_promoted?.median?.toFixed(1)}
              </p>
              <p className="text-xs text-orange-600 mt-1">Median Rating</p>
            </div>

            <div className="bg-gradient-to-br from-indigo-50 to-indigo-100 p-6 rounded-lg">
              <p className="text-sm text-indigo-700 font-medium mb-2">Difference</p>
              <p className="text-3xl font-bold text-indigo-900">
                {(ratingAnalysis.promoted?.median - ratingAnalysis.not_promoted?.median).toFixed(1)}
              </p>
              <p className="text-xs text-indigo-600 mt-1">Points Higher</p>
            </div>
          </div>
        )}

        <div className="mt-6 p-4 bg-purple-50 rounded-lg">
          <p className="text-sm text-purple-800">
            <strong>Key Insight:</strong> Previous year performance rating is another critical factor. 
            Promoted employees typically have a median rating of {ratingAnalysis?.promoted?.median} 
            compared to {ratingAnalysis?.not_promoted?.median} for non-promoted employees.
          </p>
        </div>
      </div>

      {/* Business Simulation */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center gap-2 mb-4">
          <Activity className="w-6 h-6 text-green-600" />
          <h2 className="text-xl font-bold">Business Simulation</h2>
        </div>

        <p className="text-gray-600 mb-6">
          Run what-if scenarios to predict the impact of training and rating improvements on promotion rates and hiring costs.
        </p>

        <form onSubmit={handleSimulation} className="mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">Select Scenario</label>
              <select
                value={simulationForm.scenario}
                onChange={(e) => setSimulationForm({ ...simulationForm, scenario: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              >
                {scenarios.map((s) => (
                  <option key={s.value} value={s.value}>{s.label}</option>
                ))}
              </select>
            </div>

            <div className="flex items-end">
              <button
                type="submit"
                disabled={simulationLoading}
                className="w-full bg-primary-600 text-white py-2 px-4 rounded-lg hover:bg-primary-700 disabled:opacity-50 font-medium"
              >
                {simulationLoading ? 'Running...' : 'Run Simulation'}
              </button>
            </div>
          </div>
        </form>

        {/* Simulation Results */}
        {simulationResult && (
          <div className="border-t pt-6">
            <h3 className="text-lg font-semibold mb-4">Simulation Results</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              {/* Before */}
              <div className="bg-gray-50 p-6 rounded-lg">
                <h4 className="text-md font-semibold text-gray-700 mb-4">Current State</h4>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Promotion Rate</span>
                    <span className="font-semibold">{simulationResult.before?.promotion_rate?.toFixed(2)}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Promoted Count</span>
                    <span className="font-semibold">{simulationResult.before?.promoted_count}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Hiring Cost</span>
                    <span className="font-semibold">${(simulationResult.before?.total_hiring_cost / 1000000).toFixed(2)}M</span>
                  </div>
                </div>
              </div>

              {/* After */}
              <div className="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-lg">
                <h4 className="text-md font-semibold text-green-900 mb-4">After Improvement</h4>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-green-700">Promotion Rate</span>
                    <span className="font-bold text-green-900">{simulationResult.after?.promotion_rate?.toFixed(2)}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-green-700">Promoted Count</span>
                    <span className="font-bold text-green-900">{simulationResult.after?.promoted_count}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-green-700">Hiring Cost</span>
                    <span className="font-bold text-green-900">${(simulationResult.after?.total_hiring_cost / 1000000).toFixed(2)}M</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Impact Summary */}
            <div className="bg-blue-50 p-6 rounded-lg">
              <h4 className="text-md font-semibold text-blue-900 mb-4">Impact Summary</h4>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <p className="text-sm text-blue-700">Promotion Rate Change</p>
                  <p className="text-2xl font-bold text-blue-900">
                    +{simulationResult.impact?.promotion_rate_increase?.toFixed(2)}%
                  </p>
                </div>
                <div>
                  <p className="text-sm text-blue-700">Additional Promotions</p>
                  <p className="text-2xl font-bold text-blue-900">
                    +{simulationResult.impact?.additional_promotions}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-blue-700">Cost Reduction</p>
                  <p className="text-2xl font-bold text-blue-900">
                    -{simulationResult.impact?.cost_reduction_percentage?.toFixed(2)}%
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
