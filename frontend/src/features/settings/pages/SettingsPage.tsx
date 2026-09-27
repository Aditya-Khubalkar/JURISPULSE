import React from 'react';
import { Settings, User, Building2, Bell, Lock, Palette, Globe } from 'lucide-react';
import { Card, Breadcrumb, Button, Avatar } from '@/design-system';
import { useAuthStore } from '@/store/authStore';
import { useUIStore } from '@/store/uiStore';

export function SettingsPage() {
  const { user } = useAuthStore();
  const { theme, setTheme } = useUIStore();

  return (
    <div className="max-w-2xl space-y-5">
      <div>
        <Breadcrumb items={[{ label: 'Settings' }]} />
        <h1 className="text-2xl font-bold text-ink mt-1">Settings</h1>
      </div>

      {/* Profile */}
      <Card>
        <div className="flex items-center gap-2 mb-4">
          <User className="w-4 h-4 text-ink-secondary" />
          <h2 className="font-semibold text-ink">Profile</h2>
        </div>
        <div className="flex items-center gap-4 mb-4">
          <Avatar name={user?.name ?? 'User'} size="xl" />
          <div>
            <p className="font-semibold text-ink">{user?.name}</p>
            <p className="text-sm text-ink-secondary">{user?.email}</p>
            <p className="text-sm text-ink-secondary capitalize">{user?.role} · {user?.organization}</p>
          </div>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-ink mb-1">Full Name</label>
            <input defaultValue={user?.name} className="w-full h-9 px-3 text-sm border border-border rounded-[6px] focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent" />
          </div>
          <div>
            <label className="block text-sm font-medium text-ink mb-1">Email</label>
            <input defaultValue={user?.email} type="email" className="w-full h-9 px-3 text-sm border border-border rounded-[6px] focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent" />
          </div>
          <div>
            <label className="block text-sm font-medium text-ink mb-1">Phone</label>
            <input defaultValue={user?.phone} type="tel" className="w-full h-9 px-3 text-sm border border-border rounded-[6px] focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent" />
          </div>
          <div>
            <label className="block text-sm font-medium text-ink mb-1">Bar Council ID</label>
            <input defaultValue={user?.barCouncilId} className="w-full h-9 px-3 text-sm border border-border rounded-[6px] focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent" />
          </div>
        </div>
        <div className="mt-4 flex justify-end">
          <Button size="sm">Save Profile</Button>
        </div>
      </Card>

      {/* Appearance */}
      <Card>
        <div className="flex items-center gap-2 mb-4">
          <Palette className="w-4 h-4 text-ink-secondary" />
          <h2 className="font-semibold text-ink">Appearance</h2>
        </div>
        <div className="flex gap-3">
          {(['light', 'dark'] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTheme(t)}
              className={`flex-1 p-4 rounded-[8px] border-2 text-sm font-medium transition-all ${
                theme === t ? 'border-primary-400 bg-primary-50 text-primary-700' : 'border-border text-ink-secondary hover:border-border-strong'
              }`}
            >
              {t === 'light' ? '☀️' : '🌙'} {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>
      </Card>

      {/* Notifications */}
      <Card>
        <div className="flex items-center gap-2 mb-4">
          <Bell className="w-4 h-4 text-ink-secondary" />
          <h2 className="font-semibold text-ink">Notifications</h2>
        </div>
        <div className="space-y-3">
          {[
            { label: 'Hearing reminders', desc: 'Get notified before upcoming hearings' },
            { label: 'Deadline alerts', desc: 'Alerts when deadlines approach' },
            { label: 'Document processed', desc: 'When AI finishes processing documents' },
            { label: 'Draft ready', desc: 'When a new draft is generated' },
            { label: 'Verification warnings', desc: 'When AI confidence is low' },
          ].map((n) => (
            <div key={n.label} className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-ink">{n.label}</p>
                <p className="text-xs text-ink-secondary">{n.desc}</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" defaultChecked className="sr-only peer" />
                <div className="w-10 h-5 bg-border rounded-full peer peer-checked:bg-primary-400 peer-checked:after:translate-x-5 after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-surface-raised after:rounded-full after:h-4 after:w-4 after:transition-all" />
              </label>
            </div>
          ))}
        </div>
      </Card>

      {/* Security */}
      <Card>
        <div className="flex items-center gap-2 mb-4">
          <Lock className="w-4 h-4 text-ink-secondary" />
          <h2 className="font-semibold text-ink">Security</h2>
        </div>
        <div className="space-y-3">
          <div>
            <label className="block text-sm font-medium text-ink mb-1">Current Password</label>
            <input type="password" className="w-full h-9 px-3 text-sm border border-border rounded-[6px] focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent" />
          </div>
          <div>
            <label className="block text-sm font-medium text-ink mb-1">New Password</label>
            <input type="password" className="w-full h-9 px-3 text-sm border border-border rounded-[6px] focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent" />
          </div>
          <Button variant="secondary" size="sm">Update Password</Button>
        </div>
      </Card>
    </div>
  );
}
