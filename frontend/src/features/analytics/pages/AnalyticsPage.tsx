import React, { useState } from 'react';
import { BarChart3, TrendingUp, FileText, Bot, Scale, Clock } from 'lucide-react';
import { Card, StatCard, Breadcrumb } from '@/design-system';
import { mockAnalytics, mockCasesByStatus, mockCasesByType, mockMonthlyActivity } from '@/services/api/mockData';
import { formatNumber } from '@/lib/utils';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, AreaChart, Area, Legend,
} from 'recharts';

export function AnalyticsPage() {
  return (
    <div className="space-y-5">
      <div>
        <Breadcrumb items={[{ label: 'Insights' }, { label: 'Analytics' }]} />
        <h1 className="text-2xl font-bold text-ink mt-1">Analytics</h1>
        <p className="text-sm text-ink-secondary">Platform usage and case insights</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3">
        <StatCard label="Active Cases" value={mockAnalytics.activeCases} icon={<Scale className="w-4 h-4" />} colorClass="bg-primary-100 text-primary-700" />
        <StatCard label="Completed" value={mockAnalytics.completedCases} icon={<Scale className="w-4 h-4" />} colorClass="bg-blue-50 text-blue-600" />
        <StatCard label="Research" value={mockAnalytics.researchRequests} icon={<BarChart3 className="w-4 h-4" />} colorClass="bg-purple-50 text-purple-600" />
        <StatCard label="Drafts" value={mockAnalytics.draftsGenerated} icon={<FileText className="w-4 h-4" />} colorClass="bg-amber-50 text-amber-600" />
        <StatCard label="Docs Processed" value={mockAnalytics.documentsProcessed} icon={<FileText className="w-4 h-4" />} colorClass="bg-teal-50 text-teal-600" />
        <StatCard label="Avg. Process Time" value={`${(mockAnalytics.avgProcessingTimeMs / 1000).toFixed(1)}s`} icon={<Clock className="w-4 h-4" />} colorClass="bg-orange-50 text-orange-600" />
        <StatCard label="AI Alerts" value={mockAnalytics.verificationAlerts} icon={<Bot className="w-4 h-4" />} colorClass="bg-red-50 text-red-500" />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {/* Monthly Activity */}
        <Card>
          <h3 className="font-semibold text-ink mb-4">Monthly Activity</h3>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={mockMonthlyActivity} margin={{ top: 4, right: 0, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#dde7df" />
              <XAxis dataKey="label" tick={{ fontSize: 11, fill: '#65736b' }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontSize: 11, fill: '#65736b' }} axisLine={false} tickLine={false} />
              <Tooltip contentStyle={{ background: 'white', border: '1px solid #dde7df', borderRadius: 8, fontSize: 12 }} />
              <Legend wrapperStyle={{ fontSize: 11 }} />
              <Bar dataKey="docs" name="Documents" fill="#7ed957" radius={[3, 3, 0, 0]} />
              <Bar dataKey="research" name="Research" fill="#1f6b45" radius={[3, 3, 0, 0]} />
              <Bar dataKey="drafts" name="Drafts" fill="#f4c95d" radius={[3, 3, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        {/* Cases by Type */}
        <Card>
          <h3 className="font-semibold text-ink mb-4">Cases by Type</h3>
          <div className="flex items-center gap-4">
            <ResponsiveContainer width={140} height={140}>
              <PieChart>
                <Pie data={mockCasesByType} dataKey="value" cx="50%" cy="50%" outerRadius={65} strokeWidth={0}>
                  {mockCasesByType.map((entry, i) => (
                    <Cell key={i} fill={entry.color} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
            <div className="flex-1 grid grid-cols-2 gap-1.5">
              {mockCasesByType.map((s) => (
                <div key={s.label} className="flex items-center gap-1.5 text-xs">
                  <div className="w-2 h-2 rounded-full shrink-0" style={{ background: s.color }} />
                  <span className="text-ink-secondary">{s.label}</span>
                  <span className="font-semibold text-ink ml-auto">{s.value}</span>
                </div>
              ))}
            </div>
          </div>
        </Card>

        {/* Cases by Status */}
        <Card>
          <h3 className="font-semibold text-ink mb-4">Cases by Status</h3>
          <ResponsiveContainer width="100%" height={180}>
            <BarChart data={mockCasesByStatus} layout="vertical" margin={{ top: 0, right: 20, left: 40, bottom: 0 }}>
              <XAxis type="number" tick={{ fontSize: 11, fill: '#65736b' }} axisLine={false} tickLine={false} />
              <YAxis dataKey="label" type="category" tick={{ fontSize: 11, fill: '#65736b' }} axisLine={false} tickLine={false} />
              <Tooltip contentStyle={{ background: 'white', border: '1px solid #dde7df', borderRadius: 8, fontSize: 12 }} />
              <Bar dataKey="value" name="Cases" radius={[0, 3, 3, 0]}>
                {mockCasesByStatus.map((entry, i) => (
                  <Cell key={i} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </Card>

        {/* Research usage trend */}
        <Card>
          <h3 className="font-semibold text-ink mb-4">Research & Drafts Trend</h3>
          <ResponsiveContainer width="100%" height={180}>
            <AreaChart data={mockMonthlyActivity} margin={{ top: 4, right: 0, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id="aResearch" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#7ed957" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#7ed957" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="aDrafts" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#f4c95d" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#f4c95d" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#dde7df" />
              <XAxis dataKey="label" tick={{ fontSize: 11, fill: '#65736b' }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontSize: 11, fill: '#65736b' }} axisLine={false} tickLine={false} />
              <Tooltip contentStyle={{ background: 'white', border: '1px solid #dde7df', borderRadius: 8, fontSize: 12 }} />
              <Legend wrapperStyle={{ fontSize: 11 }} />
              <Area type="monotone" dataKey="research" stroke="#7ed957" strokeWidth={2} fill="url(#aResearch)" name="Research" />
              <Area type="monotone" dataKey="drafts" stroke="#f4c95d" strokeWidth={2} fill="url(#aDrafts)" name="Drafts" />
            </AreaChart>
          </ResponsiveContainer>
        </Card>
      </div>
    </div>
  );
}
