import { useState, useEffect } from 'react';
import { analyticsAPI } from '../services/api';
import { Lightbulb, TrendingUp, Award, AlertCircle, CheckCircle2, XCircle } from 'lucide-react';

export default function Recommendations() {
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const fetchRecommendations = async () => {
    try {
      setLoading(true);
      const response = await analyticsAPI.getRecommendations();
      setRecommendations(response.data);
    } catch (error) {
      console.error('Failed to fetch recommendations:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading recommendations...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Business Recommendations</h1>
        <p className="text-gray-600">Data-driven insights to improve promotion rates and reduce costs</p>
      </div>

      {/* Overview */}
      <div className="bg-gradient-to-r from-primary-50 to-secondary-50 rounded-lg p-6 mb-6 border border-primary-200">
        <div className="flex items-start gap-4">
          <div className="bg-primary-100 p-3 rounded-full">
            <Lightbulb className="w-8 h-8 text-primary-600" />
          </div>
          <div className="flex-1">
            <h2 className="text-xl font-bold text-gray-900 mb-2">Key Finding</h2>
            <p className="text-gray-700 text-lg leading-relaxed">
              Based on analysis of {recommendations?.summary?.total_employees?.toLocaleString()} employees, 
              we've identified two primary drivers of promotion success. Implementing these recommendations 
              could help achieve the target promotion rate of <strong>25%</strong> and reduce hiring costs by <strong>50%</strong>.
            </p>
          </div>
        </div>
      </div>

      {/* Recommendations Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Training Score Recommendation */}
        {recommendations?.training_recommendation && (
          <div className="bg-white rounded-lg shadow-lg overflow-hidden">
            <div className="bg-gradient-to-r from-blue-500 to-blue-600 p-6 text-white">
              <div className="flex items-center gap-3 mb-2">
                <TrendingUp className="w-8 h-8" />
                <h3 className="text-2xl font-bold">Recommendation #1</h3>
              </div>
              <p className="text-blue-100 text-lg">Improve Training Scores</p>
            </div>

            <div className="p-6">
              <div className="mb-6">
                <p className="text-gray-700 leading-relaxed">
                  {recommendations.training_recommendation.description}
                </p>
              </div>

              {/* Key Metrics */}
              <div className="bg-blue-50 rounded-lg p-4 mb-6">
                <h4 className="font-semibold text-blue-900 mb-3">Key Insights</h4>
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-blue-800">Promoted Avg Score</span>
                    <span className="font-bold text-blue-900">
                      {recommendations.training_recommendation.promoted_avg?.toFixed(1)}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-blue-800">Not Promoted Avg</span>
                    <span className="font-bold text-blue-900">
                      {recommendations.training_recommendation.not_promoted_avg?.toFixed(1)}
                    </span>
                  </div>
                  <div className="flex justify-between items-center border-t border-blue-200 pt-2">
                    <span className="text-blue-800 font-semibold">Difference</span>
                    <span className="font-bold text-blue-900 text-lg">
                      {recommendations.training_recommendation.difference?.toFixed(1)} points
                    </span>
                  </div>
                </div>
              </div>

              {/* Pros and Cons */}
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div>
                  <h5 className="font-semibold text-green-900 mb-2 flex items-center gap-2">
                    <CheckCircle2 className="w-5 h-5" />
                    Pros
                  </h5>
                  <ul className="space-y-1">
                    {recommendations.training_recommendation.pros?.map((pro, i) => (
                      <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
                        <span className="text-green-600 mt-1">•</span>
                        <span>{pro}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h5 className="font-semibold text-red-900 mb-2 flex items-center gap-2">
                    <XCircle className="w-5 h-5" />
                    Cons
                  </h5>
                  <ul className="space-y-1">
                    {recommendations.training_recommendation.cons?.map((con, i) => (
                      <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
                        <span className="text-red-600 mt-1">•</span>
                        <span>{con}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Action Items */}
              <div className="border-t pt-4">
                <h5 className="font-semibold text-gray-900 mb-3">Recommended Actions</h5>
                <ul className="space-y-2">
                  {recommendations.training_recommendation.actions?.map((action, i) => (
                    <li key={i} className="flex items-start gap-3">
                      <span className="bg-blue-100 text-blue-800 font-semibold px-2 py-1 rounded text-xs">
                        {i + 1}
                      </span>
                      <span className="text-sm text-gray-700 flex-1">{action}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* Rating Recommendation */}
        {recommendations?.rating_recommendation && (
          <div className="bg-white rounded-lg shadow-lg overflow-hidden">
            <div className="bg-gradient-to-r from-purple-500 to-purple-600 p-6 text-white">
              <div className="flex items-center gap-3 mb-2">
                <Award className="w-8 h-8" />
                <h3 className="text-2xl font-bold">Recommendation #2</h3>
              </div>
              <p className="text-purple-100 text-lg">Improve Performance Ratings</p>
            </div>

            <div className="p-6">
              <div className="mb-6">
                <p className="text-gray-700 leading-relaxed">
                  {recommendations.rating_recommendation.description}
                </p>
              </div>

              {/* Key Metrics */}
              <div className="bg-purple-50 rounded-lg p-4 mb-6">
                <h4 className="font-semibold text-purple-900 mb-3">Key Insights</h4>
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-purple-800">Promoted Median</span>
                    <span className="font-bold text-purple-900">
                      {recommendations.rating_recommendation.promoted_median?.toFixed(1)}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-purple-800">Not Promoted Median</span>
                    <span className="font-bold text-purple-900">
                      {recommendations.rating_recommendation.not_promoted_median?.toFixed(1)}
                    </span>
                  </div>
                  <div className="flex justify-between items-center border-t border-purple-200 pt-2">
                    <span className="text-purple-800 font-semibold">Difference</span>
                    <span className="font-bold text-purple-900 text-lg">
                      {recommendations.rating_recommendation.difference?.toFixed(1)} points
                    </span>
                  </div>
                </div>
              </div>

              {/* Pros and Cons */}
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div>
                  <h5 className="font-semibold text-green-900 mb-2 flex items-center gap-2">
                    <CheckCircle2 className="w-5 h-5" />
                    Pros
                  </h5>
                  <ul className="space-y-1">
                    {recommendations.rating_recommendation.pros?.map((pro, i) => (
                      <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
                        <span className="text-green-600 mt-1">•</span>
                        <span>{pro}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h5 className="font-semibold text-red-900 mb-2 flex items-center gap-2">
                    <XCircle className="w-5 h-5" />
                    Cons
                  </h5>
                  <ul className="space-y-1">
                    {recommendations.rating_recommendation.cons?.map((con, i) => (
                      <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
                        <span className="text-red-600 mt-1">•</span>
                        <span>{con}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Action Items */}
              <div className="border-t pt-4">
                <h5 className="font-semibold text-gray-900 mb-3">Recommended Actions</h5>
                <ul className="space-y-2">
                  {recommendations.rating_recommendation.actions?.map((action, i) => (
                    <li key={i} className="flex items-start gap-3">
                      <span className="bg-purple-100 text-purple-800 font-semibold px-2 py-1 rounded text-xs">
                        {i + 1}
                      </span>
                      <span className="text-sm text-gray-700 flex-1">{action}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Best Strategy */}
      {recommendations?.best_strategy && (
        <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg p-6 border border-green-200">
          <div className="flex items-start gap-4">
            <div className="bg-green-100 p-3 rounded-full">
              <AlertCircle className="w-8 h-8 text-green-600" />
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-bold text-green-900 mb-2">Recommended Strategy</h3>
              <p className="text-gray-700 text-lg leading-relaxed mb-4">
                {recommendations.best_strategy.description}
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-white rounded-lg p-4">
                  <p className="text-sm text-gray-600 mb-1">Expected Promotion Rate</p>
                  <p className="text-2xl font-bold text-green-600">
                    {recommendations.best_strategy.expected_promotion_rate?.toFixed(1)}%
                  </p>
                </div>
                <div className="bg-white rounded-lg p-4">
                  <p className="text-sm text-gray-600 mb-1">Additional Promotions</p>
                  <p className="text-2xl font-bold text-green-600">
                    +{recommendations.best_strategy.additional_promotions}
                  </p>
                </div>
                <div className="bg-white rounded-lg p-4">
                  <p className="text-sm text-gray-600 mb-1">Cost Reduction</p>
                  <p className="text-2xl font-bold text-green-600">
                    -{recommendations.best_strategy.cost_reduction?.toFixed(1)}%
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Implementation Timeline */}
      <div className="bg-white rounded-lg shadow p-6 mt-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Implementation Timeline</h3>
        <div className="space-y-4">
          <div className="flex items-start gap-4">
            <div className="bg-blue-100 text-blue-800 font-bold px-3 py-1 rounded">Q1</div>
            <div className="flex-1">
              <p className="font-semibold text-gray-900">Assessment & Planning</p>
              <p className="text-sm text-gray-600">Analyze current training programs and performance review systems</p>
            </div>
          </div>
          <div className="flex items-start gap-4">
            <div className="bg-purple-100 text-purple-800 font-bold px-3 py-1 rounded">Q2</div>
            <div className="flex-1">
              <p className="font-semibold text-gray-900">Pilot Program</p>
              <p className="text-sm text-gray-600">Launch enhanced training and rating improvements in select departments</p>
            </div>
          </div>
          <div className="flex items-start gap-4">
            <div className="bg-green-100 text-green-800 font-bold px-3 py-1 rounded">Q3</div>
            <div className="flex-1">
              <p className="font-semibold text-gray-900">Full Rollout</p>
              <p className="text-sm text-gray-600">Deploy improvements company-wide based on pilot results</p>
            </div>
          </div>
          <div className="flex items-start gap-4">
            <div className="bg-orange-100 text-orange-800 font-bold px-3 py-1 rounded">Q4</div>
            <div className="flex-1">
              <p className="font-semibold text-gray-900">Monitor & Optimize</p>
              <p className="text-sm text-gray-600">Track KPIs and adjust strategies for continuous improvement</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
