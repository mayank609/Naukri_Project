import React, { useState } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import {
  LightBulbIcon,
  PhotoIcon,
  VideoCameraIcon,
  DocumentTextIcon,
  SparklesIcon,
  ArrowDownTrayIcon
} from '@heroicons/react/24/outline';

const ContentIdeation = () => {
  const { token } = useAuth();
  const [loading, setLoading] = useState(false);
  const [generatedContent, setGeneratedContent] = useState(null);
  const [contentType, setContentType] = useState('caption');
  
  const { register, handleSubmit, formState: { errors }, reset } = useForm();

  const contentTypes = [
    { id: 'image', name: 'Image Ideas', icon: PhotoIcon, description: 'Generate visual content concepts' },
    { id: 'caption', name: 'Caption Ideas', icon: DocumentTextIcon, description: 'Create engaging captions' },
    { id: 'video', name: 'Video Ideas', icon: VideoCameraIcon, description: 'Develop video content strategies' }
  ];

  const onSubmit = async (data) => {
    setLoading(true);
    try {
      const response = await axios.post('/api/content/generate', {
        content_type: contentType,
        brand_description: data.brandDescription,
        target_audience: data.targetAudience,
        platform: data.platform,
        tone: data.tone,
        hashtags: data.hashtags ? data.hashtags.split(',').map(tag => tag.trim()) : [],
        specific_requirements: data.requirements
      }, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      setGeneratedContent(response.data);
      toast.success('Content generated successfully!');
    } catch (error) {
      console.error('Error generating content:', error);
      toast.error('Failed to generate content. Please try again.');
      
      // Use mock data for demo
      setGeneratedContent(getMockGeneratedContent(contentType, data));
    } finally {
      setLoading(false);
    }
  };

  const getMockGeneratedContent = (type, data) => ({
    content_type: type,
    content: `Mock ${type} content for ${data.brandDescription}. This is a sample generated content that demonstrates the AI capabilities.`,
    strategy: `Focus on ${data.tone} tone that resonates with ${data.targetAudience}`,
    brand_alignment: `Ensure consistent brand voice and visual identity across all content`,
    engagement_tips: [
      "Use high-quality visuals",
      "Include clear call-to-actions",
      "Engage with your audience",
      "Post consistently",
      "Use relevant hashtags"
    ],
    hashtag_suggestions: ["#brand", "#content", "#socialmedia", "#engagement", "#strategy"]
  });

  const downloadContent = () => {
    if (!generatedContent) return;
    
    const content = `
Content Type: ${generatedContent.content_type}
Strategy: ${generatedContent.strategy}
Brand Alignment: ${generatedContent.brand_alignment}

Content:
${generatedContent.content}

Engagement Tips:
${generatedContent.engagement_tips.map(tip => `- ${tip}`).join('\n')}

Hashtag Suggestions:
${generatedContent.hashtag_suggestions.map(tag => `- ${tag}`).join('\n')}
    `;
    
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${contentType}_content_${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Content Ideation</h1>
        <p className="text-gray-600">AI-powered content generation for your social media strategy</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Content Generation Form */}
        <div className="card">
          <div className="flex items-center mb-6">
            <SparklesIcon className="h-6 w-6 text-primary-600 mr-2" />
            <h2 className="text-lg font-semibold text-gray-900">Generate Content</h2>
          </div>

          {/* Content Type Selection */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Content Type
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {contentTypes.map((type) => (
                <button
                  key={type.id}
                  onClick={() => setContentType(type.id)}
                  className={`p-4 rounded-lg border-2 transition-colors ${
                    contentType === type.id
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <type.icon className="h-6 w-6 text-primary-600 mb-2" />
                  <div className="text-sm font-medium text-gray-900">{type.name}</div>
                  <div className="text-xs text-gray-500">{type.description}</div>
                </button>
              ))}
            </div>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Brand Description
              </label>
              <textarea
                {...register('brandDescription', { required: 'Brand description is required' })}
                className="input-field"
                rows={3}
                placeholder="Describe your brand, values, and target audience..."
              />
              {errors.brandDescription && (
                <p className="text-red-500 text-sm mt-1">{errors.brandDescription.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Target Audience
              </label>
              <input
                {...register('targetAudience', { required: 'Target audience is required' })}
                type="text"
                className="input-field"
                placeholder="e.g., Young professionals aged 25-35"
              />
              {errors.targetAudience && (
                <p className="text-red-500 text-sm mt-1">{errors.targetAudience.message}</p>
              )}
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Platform
                </label>
                <select
                  {...register('platform')}
                  className="input-field"
                >
                  <option value="instagram">Instagram</option>
                  <option value="facebook">Facebook</option>
                  <option value="twitter">Twitter</option>
                  <option value="linkedin">LinkedIn</option>
                  <option value="tiktok">TikTok</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Tone
                </label>
                <select
                  {...register('tone')}
                  className="input-field"
                >
                  <option value="professional">Professional</option>
                  <option value="casual">Casual</option>
                  <option value="friendly">Friendly</option>
                  <option value="humorous">Humorous</option>
                  <option value="inspirational">Inspirational</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Hashtags (comma-separated)
              </label>
              <input
                {...register('hashtags')}
                type="text"
                className="input-field"
                placeholder="e.g., #brand, #content, #socialmedia"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Specific Requirements (optional)
              </label>
              <textarea
                {...register('requirements')}
                className="input-field"
                rows={2}
                placeholder="Any specific requirements or themes you want to include..."
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full flex items-center justify-center"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Generating...
                </>
              ) : (
                <>
                  <SparklesIcon className="h-5 w-5 mr-2" />
                  Generate Content
                </>
              )}
            </button>
          </form>
        </div>

        {/* Generated Content Display */}
        <div className="card">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center">
              <LightBulbIcon className="h-6 w-6 text-primary-600 mr-2" />
              <h2 className="text-lg font-semibold text-gray-900">Generated Content</h2>
            </div>
            {generatedContent && (
              <button
                onClick={downloadContent}
                className="btn-secondary flex items-center"
              >
                <ArrowDownTrayIcon className="h-4 w-4 mr-1" />
                Download
              </button>
            )}
          </div>

          {generatedContent ? (
            <div className="space-y-6">
              {/* Content */}
              <div>
                <h3 className="text-sm font-medium text-gray-700 mb-2">Content</h3>
                <div className="bg-gray-50 rounded-lg p-4">
                  <p className="text-gray-900 whitespace-pre-wrap">{generatedContent.content}</p>
                </div>
              </div>

              {/* Strategy */}
              <div>
                <h3 className="text-sm font-medium text-gray-700 mb-2">Strategy</h3>
                <div className="bg-blue-50 rounded-lg p-4">
                  <p className="text-blue-900">{generatedContent.strategy}</p>
                </div>
              </div>

              {/* Brand Alignment */}
              <div>
                <h3 className="text-sm font-medium text-gray-700 mb-2">Brand Alignment</h3>
                <div className="bg-green-50 rounded-lg p-4">
                  <p className="text-green-900">{generatedContent.brand_alignment}</p>
                </div>
              </div>

              {/* Engagement Tips */}
              <div>
                <h3 className="text-sm font-medium text-gray-700 mb-2">Engagement Tips</h3>
                <ul className="space-y-2">
                  {generatedContent.engagement_tips.map((tip, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-primary-600 mr-2">•</span>
                      <span className="text-gray-900">{tip}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Hashtag Suggestions */}
              <div>
                <h3 className="text-sm font-medium text-gray-700 mb-2">Hashtag Suggestions</h3>
                <div className="flex flex-wrap gap-2">
                  {generatedContent.hashtag_suggestions.map((tag, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center py-12">
              <LightBulbIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500">Generate content to see results here</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ContentIdeation; 