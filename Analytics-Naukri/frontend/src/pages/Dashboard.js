import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import {
  ChartBarIcon,
  HeartIcon,
  ChatBubbleLeftIcon,
  ShareIcon,
  TrendingUpIcon,
  TrendingDownIcon
} from '@heroicons/react/24/outline';
import { Line, Bar, Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const Dashboard = () => {
  const { token } = useAuth();
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await axios.get('/api/analytics/dashboard', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      setDashboardData(response.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      // Use mock data for demo
      setDashboardData(getMockDashboardData());
    } finally {
      setLoading(false);
    }
  };

  const getMockDashboardData = () => ({
    summary: {
      total_posts: 45,
      avg_engagement_rate: 3.2,
      total_likes: 12500,
      total_comments: 850,
      total_shares: 320,
      total_engagement: 13670
    },
    trends: {
      daily_trends: [
        { date: '2024-01-01', likes: 120, comments: 8, shares: 3, engagement_rate: 2.8 },
        { date: '2024-01-02', likes: 150, comments: 12, shares: 5, engagement_rate: 3.1 },
        { date: '2024-01-03', likes: 180, comments: 15, shares: 7, engagement_rate: 3.5 },
        { date: '2024-01-04', likes: 200, comments: 18, shares: 9, engagement_rate: 3.8 },
        { date: '2024-01-05', likes: 220, comments: 20, shares: 10, engagement_rate: 4.0 },
      ],
      media_performance: [
        { media_type: 'image', engagement_rate: 3.2, likes: 150, comments: 12 },
        { media_type: 'video', engagement_rate: 4.1, likes: 200, comments: 18 },
        { media_type: 'carousel', engagement_rate: 2.8, likes: 120, comments: 8 },
      ]
    },
    insights: [
      {
        type: 'success',
        title: 'High Performing Content',
        message: 'Found 3 posts with above-average engagement',
        recommendation: 'Analyze these posts to understand what resonates with your audience'
      },
      {
        type: 'warning',
        title: 'Low Performing Content',
        message: 'Found 2 posts with below-average engagement',
        recommendation: 'Review these posts and consider adjusting your content strategy'
      }
    ]
  });

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  const engagementChartData = {
    labels: dashboardData?.trends?.daily_trends?.map(item => item.date) || [],
    datasets: [
      {
        label: 'Engagement Rate (%)',
        data: dashboardData?.trends?.daily_trends?.map(item => item.engagement_rate) || [],
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4,
      },
    ],
  };

  const mediaPerformanceData = {
    labels: dashboardData?.trends?.media_performance?.map(item => item.media_type) || [],
    datasets: [
      {
        label: 'Engagement Rate (%)',
        data: dashboardData?.trends?.media_performance?.map(item => item.engagement_rate) || [],
        backgroundColor: [
          'rgba(59, 130, 246, 0.8)',
          'rgba(16, 185, 129, 0.8)',
          'rgba(245, 158, 11, 0.8)',
        ],
      },
    ],
  };

  const StatCard = ({ title, value, icon: Icon, trend, trendValue }) => (
    <div className="stat-card">
      <div className="flex items-center justify-between">
        <div>
          <p className="metric-label">{title}</p>
          <p className="metric-value">{value}</p>
          {trend && (
            <div className={`flex items-center text-sm ${trend === 'up' ? 'trend-up' : 'trend-down'}`}>
              {trend === 'up' ? (
                <TrendingUpIcon className="h-4 w-4 mr-1" />
              ) : (
                <TrendingDownIcon className="h-4 w-4 mr-1" />
              )}
              {trendValue}
            </div>
          )}
        </div>
        <div className="h-12 w-12 rounded-lg bg-primary-100 flex items-center justify-center">
          <Icon className="h-6 w-6 text-primary-600" />
        </div>
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Overview of your social media performance</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Posts"
          value={dashboardData?.summary?.total_posts || 0}
          icon={ChartBarIcon}
        />
        <StatCard
          title="Avg Engagement Rate"
          value={`${dashboardData?.summary?.avg_engagement_rate || 0}%`}
          icon={HeartIcon}
          trend="up"
          trendValue="+12%"
        />
        <StatCard
          title="Total Likes"
          value={dashboardData?.summary?.total_likes?.toLocaleString() || 0}
          icon={HeartIcon}
        />
        <StatCard
          title="Total Comments"
          value={dashboardData?.summary?.total_comments?.toLocaleString() || 0}
          icon={ChatBubbleLeftIcon}
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Engagement Trend */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Engagement Trend</h3>
          <div className="h-64">
            <Line
              data={engagementChartData}
              options={{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                  legend: {
                    display: false,
                  },
                },
                scales: {
                  y: {
                    beginAtZero: true,
                    ticks: {
                      callback: function(value) {
                        return value + '%';
                      }
                    }
                  }
                }
              }}
            />
          </div>
        </div>

        {/* Media Performance */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Media Performance</h3>
          <div className="h-64">
            <Bar
              data={mediaPerformanceData}
              options={{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                  legend: {
                    display: false,
                  },
                },
                scales: {
                  y: {
                    beginAtZero: true,
                    ticks: {
                      callback: function(value) {
                        return value + '%';
                      }
                    }
                  }
                }
              }}
            />
          </div>
        </div>
      </div>

      {/* Insights */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Insights</h3>
        <div className="space-y-4">
          {dashboardData?.insights?.map((insight, index) => (
            <div
              key={index}
              className={`p-4 rounded-lg border-l-4 ${
                insight.type === 'success'
                  ? 'bg-green-50 border-green-400'
                  : insight.type === 'warning'
                  ? 'bg-yellow-50 border-yellow-400'
                  : 'bg-blue-50 border-blue-400'
              }`}
            >
              <h4 className="font-medium text-gray-900">{insight.title}</h4>
              <p className="text-sm text-gray-600 mt-1">{insight.message}</p>
              <p className="text-sm text-gray-500 mt-2">{insight.recommendation}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 