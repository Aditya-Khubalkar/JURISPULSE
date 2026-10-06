/**\n * Authentication pages including Login, Register, and Forgot Password.\n */\nimport React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Scale, Eye, EyeOff, ArrowRight } from 'lucide-react';
import { useAuthStore } from '@/store/authStore';
import { authApi } from '@/services/api/mockApi';
import { ROUTES } from '@/constants';
import { Button } from '@/design-system';
import { Alert } from '@/design-system';

export function LoginPage() {
  const [email, setEmail] = useState('demo@jurispulse.in');
  const [password, setPassword] = useState('demo1234');
  const [remember, setRemember] = useState(false);
  const [showPw, setShowPw] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const { login } = useAuthStore();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) {
      setError('Please enter your email and password.');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const res = await authApi.login(email, password);
      login(res.data.user, res.data.token);
      navigate(ROUTES.DASHBOARD);
    } catch {
      setError('Invalid credentials. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-surface flex">
      {/* Left panel */}
      <div className="hidden lg:flex lg:w-1/2 bg-[#174A35] relative overflow-hidden flex-col justify-between p-12">
        {/* Background decoration */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-16 left-16 w-64 h-64 rounded-full bg-primary-400 blur-3xl" />
          <div className="absolute bottom-16 right-16 w-64 h-64 rounded-full bg-[#f4c95d] blur-3xl" />
        </div>

        {/* Logo */}
        <div className="relative flex items-center gap-3">
          <div className="w-10 h-10 rounded-[10px] bg-primary-400 flex items-center justify-center">
            <Scale className="w-5 h-5 text-primary-900" strokeWidth={2.5} />
          </div>
          <div>
            <span className="text-xl font-bold text-white">JurisPulse</span>
            <div className="text-xs text-white/60">by Axiom</div>
          </div>
        </div>

        {/* Quote */}
        <div className="relative">
          <blockquote className="text-2xl font-light text-white/90 font-serif leading-relaxed mb-6">
            "Where there is law, there is justice — and where there is justice, there must be clarity."
          </blockquote>
          <div className="space-y-3">
            {[
              'Multi-agent AI workflow orchestration',
              'Real-time hallucination detection',
              '14,544 indexed Indian legal precedents',
            ].map((feature) => (
              <div key={feature} className="flex items-center gap-2 text-sm text-white/80">
                <div className="w-1.5 h-1.5 rounded-full bg-primary-400" />
                {feature}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Right panel */}
      <div className="flex-1 flex items-center justify-center p-6">
        <div className="w-full max-w-sm">
          {/* Mobile logo */}
          <div className="lg:hidden flex items-center gap-2 mb-8">
            <div className="w-8 h-8 rounded-[8px] bg-primary-400 flex items-center justify-center">
              <Scale className="w-4 h-4 text-primary-900" strokeWidth={2.5} />
            </div>
            <span className="text-lg font-bold text-ink">JurisPulse</span>
          </div>

          <h1 className="text-2xl font-bold text-ink mb-1">Sign in</h1>
          <p className="text-sm text-ink-secondary mb-6">
            Don't have an account?{' '}
            <Link to={ROUTES.REGISTER} className="text-primary-700 font-medium hover:underline">
              Create account
            </Link>
          </p>

          {/* Demo hint */}
          <div className="mb-4 p-3 bg-primary-100 border border-primary-200 rounded-[8px]">
            <p className="text-xs text-primary-700 font-medium">Demo credentials pre-filled</p>
            <p className="text-xs text-ink-secondary">Email: demo@jurispulse.in · Password: demo1234</p>
          </div>

          {error && (
            <Alert variant="danger" className="mb-4" onDismiss={() => setError('')}>
              {error}
            </Alert>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-ink mb-1">
                Email address
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                autoComplete="email"
                required
                className="w-full h-10 px-3 text-sm border border-border rounded-[6px] bg-surface-raised focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent"
                placeholder="you@example.com"
              />
            </div>

            <div>
              <div className="flex items-center justify-between mb-1">
                <label htmlFor="password" className="text-sm font-medium text-ink">
                  Password
                </label>
                <Link
                  to={ROUTES.FORGOT_PASSWORD}
                  className="text-xs text-primary-700 hover:underline"
                >
                  Forgot password?
                </Link>
              </div>
              <div className="relative">
                <input
                  id="password"
                  type={showPw ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  autoComplete="current-password"
                  required
                  className="w-full h-10 px-3 pr-10 text-sm border border-border rounded-[6px] bg-surface-raised focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent"
                  placeholder="••••••••"
                />
                <button
                  type="button"
                  onClick={() => setShowPw(!showPw)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-ink-secondary hover:text-ink"
                  aria-label={showPw ? 'Hide password' : 'Show password'}
                >
                  {showPw ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <input
                id="remember"
                type="checkbox"
                checked={remember}
                onChange={(e) => setRemember(e.target.checked)}
                className="w-4 h-4 rounded border-border accent-primary-400"
              />
              <label htmlFor="remember" className="text-sm text-ink-secondary">
                Remember me
              </label>
            </div>

            <Button
              type="submit"
              fullWidth
              size="lg"
              loading={loading}
              rightIcon={!loading ? <ArrowRight className="w-4 h-4" /> : undefined}
            >
              Sign in
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
}

// ── Register Page ─────────────────────────────────────────────────────────────

export function RegisterPage() {
  const navigate = useNavigate();
  const { login } = useAuthStore();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirm: '',
    role: 'lawyer',
    organization: '',
  });
  const [error, setError] = useState('');

  const handleChange = (field: string) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData((prev) => ({ ...prev, [field]: e.target.value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.password !== formData.confirm) {
      setError('Passwords do not match.');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const res = await authApi.register(formData);
      login(res.data.user, res.data.token);
      navigate(ROUTES.DASHBOARD);
    } catch {
      setError('Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-surface flex items-center justify-center p-6">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="flex items-center gap-2 mb-8">
          <div className="w-8 h-8 rounded-[8px] bg-primary-400 flex items-center justify-center">
            <Scale className="w-4 h-4 text-primary-900" strokeWidth={2.5} />
          </div>
          <span className="text-lg font-bold text-ink">JurisPulse</span>
        </div>

        <div className="bg-surface-raised rounded-[12px] border border-border shadow-sm p-6">
          <h1 className="text-xl font-bold text-ink mb-1">Create account</h1>
          <p className="text-sm text-ink-secondary mb-5">
            Already have an account?{' '}
            <Link to={ROUTES.LOGIN} className="text-primary-700 font-medium hover:underline">
              Sign in
            </Link>
          </p>

          {error && (
            <Alert variant="danger" className="mb-4" onDismiss={() => setError('')}>
              {error}
            </Alert>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div className="col-span-2">
                <label htmlFor="name" className="block text-sm font-medium text-ink mb-1">Full name <span className="text-red-500">*</span></label>
                <input id="name" type="text" value={formData.name} onChange={handleChange('name')} required
                  className="w-full h-9 px-3 text-sm border border-border rounded-[6px] bg-surface-raised focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent"
                  placeholder="Arjun Sharma" />
              </div>
              <div className="col-span-2">
                <label htmlFor="reg-email" className="block text-sm font-medium text-ink mb-1">Email address <span className="text-red-500">*</span></label>
                <input id="reg-email" type="email" value={formData.email} onChange={handleChange('email')} required
                  className="w-full h-9 px-3 text-sm border border-border rounded-[6px] bg-surface-raised focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent"
                  placeholder="you@example.com" />
              </div>
              <div>
                <label htmlFor="reg-password" className="block text-sm font-medium text-ink mb-1">Password <span className="text-red-500">*</span></label>
                <input id="reg-password" type="password" value={formData.password} onChange={handleChange('password')} required
                  className="w-full h-9 px-3 text-sm border border-border rounded-[6px] bg-surface-raised focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent"
                  placeholder="••••••••" />
              </div>
              <div>
                <label htmlFor="reg-confirm" className="block text-sm font-medium text-ink mb-1">Confirm password <span className="text-red-500">*</span></label>
                <input id="reg-confirm" type="password" value={formData.confirm} onChange={handleChange('confirm')} required
                  className="w-full h-9 px-3 text-sm border border-border rounded-[6px] bg-surface-raised focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent"
                  placeholder="••••••••" />
              </div>
              <div className="col-span-2">
                <label htmlFor="reg-role" className="block text-sm font-medium text-ink mb-1">Role</label>
                <select id="reg-role" value={formData.role} onChange={handleChange('role')}
                  className="w-full h-9 px-3 text-sm border border-border rounded-[6px] bg-surface-raised focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent">
                  <option value="lawyer">Lawyer</option>
                  <option value="junior">Junior Lawyer</option>
                  <option value="client">Client</option>
                </select>
                <p className="text-xs text-ink-secondary mt-1">Admin roles require manual assignment.</p>
              </div>
              <div className="col-span-2">
                <label htmlFor="reg-org" className="block text-sm font-medium text-ink mb-1">Organization</label>
                <input id="reg-org" type="text" value={formData.organization} onChange={handleChange('organization')}
                  className="w-full h-9 px-3 text-sm border border-border rounded-[6px] bg-surface-raised focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent"
                  placeholder="Law firm or organization name" />
              </div>
            </div>

            <Button type="submit" fullWidth size="lg" loading={loading} className="mt-2">
              Create account
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
}

// ── Forgot Password Page ──────────────────────────────────────────────────────

export function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [sent, setSent] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    await authApi.forgotPassword(email);
    setLoading(false);
    setSent(true);
  };

  return (
    <div className="min-h-screen bg-surface flex items-center justify-center p-6">
      <div className="w-full max-w-sm">
        <div className="flex items-center gap-2 mb-8">
          <div className="w-8 h-8 rounded-[8px] bg-primary-400 flex items-center justify-center">
            <Scale className="w-4 h-4 text-primary-900" strokeWidth={2.5} />
          </div>
          <span className="text-lg font-bold text-ink">JurisPulse</span>
        </div>

        <h1 className="text-xl font-bold text-ink mb-1">Reset password</h1>
        <p className="text-sm text-ink-secondary mb-6">
          Enter your email and we'll send reset instructions.
        </p>

        {sent ? (
          <Alert variant="success">
            <p className="font-medium">Email sent!</p>
            <p>Check your inbox for password reset instructions.</p>
          </Alert>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="forgot-email" className="block text-sm font-medium text-ink mb-1">
                Email address
              </label>
              <input
                id="forgot-email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full h-10 px-3 text-sm border border-border rounded-[6px] bg-surface-raised focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent"
                placeholder="you@example.com"
              />
            </div>
            <Button type="submit" fullWidth size="lg" loading={loading}>
              Send reset link
            </Button>
            <div className="text-center">
              <Link to={ROUTES.LOGIN} className="text-sm text-ink-secondary hover:text-ink">
                Back to sign in
              </Link>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
\n// Add registration page if present\n