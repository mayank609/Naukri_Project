import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Analytics from './pages/Analytics';
import ContentIdeation from './pages/ContentIdeation';
import CompetitorAnalysis from './pages/CompetitorAnalysis';
import Login from './pages/Login';
import Register from './pages/Register';
import { AuthProvider } from './contexts/AuthContext';

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="analytics" element={<Analytics />} />
          <Route path="content-ideation" element={<ContentIdeation />} />
          <Route path="competitor-analysis" element={<CompetitorAnalysis />} />
        </Route>
      </Routes>
    </AuthProvider>
  );
}

export default App; 