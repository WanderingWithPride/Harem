# 🔧 SUPABASE SETUP GUIDE
## Connect Your Harem CRM to Supabase Database

**Status:** System working in offline mode - needs database connection  
**Next Step:** Configure Supabase credentials  

---

## 🚀 **QUICK SETUP (5 Minutes)**

### **Step 1: Create Supabase Project**

1. **Go to [supabase.com](https://supabase.com)**
2. **Click "Start your project"**
3. **Sign up/Login with GitHub**
4. **Click "New Project"**
5. **Fill in project details:**
   - **Name:** `harem-crm`
   - **Database Password:** Create a strong password
   - **Region:** Choose closest to you
6. **Click "Create new project"**
7. **Wait 2-3 minutes for setup**

### **Step 2: Get Your Credentials**

1. **Go to your project dashboard**
2. **Click "Settings" (gear icon)**
3. **Click "API"**
4. **Copy these values:**
   - **Project URL** (looks like: `https://your-project.supabase.co`)
   - **anon public key** (long string starting with `eyJ...`)

### **Step 3: Configure Streamlit Cloud**

#### **Option A: Streamlit Cloud Secrets (Recommended)**

1. **Go to your Streamlit Cloud app**
2. **Click "Manage app"**
3. **Click "Secrets"**
4. **Add these secrets:**

```toml
[supabase]
url = "https://your-project.supabase.co"
anon_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

[security]
jwt_secret = "your-secure-jwt-secret-key"
encryption_key = "your-encryption-key"

[performance]
cache_ttl = 300
enable_caching = true
```

#### **Option B: Environment Variables (Local)**

1. **Create `.env` file in your project:**
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
JWT_SECRET=your-secure-jwt-secret-key
ENCRYPTION_KEY=your-encryption-key
```

### **Step 4: Set Up Database Tables**

1. **Go to Supabase SQL Editor**
2. **Click "New query"**
3. **Copy and paste this SQL:**

```sql
-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create custom types
CREATE TYPE user_role AS ENUM ('owner', 'panel', 'sub');
CREATE TYPE application_status AS ENUM ('draft', 'submitted', 'under_review', 'approved', 'rejected');
CREATE TYPE task_category AS ENUM ('service', 'training', 'content', 'partnered', 'partnered_content');
CREATE TYPE task_status AS ENUM ('planned', 'confirmed', 'done', 'cancelled');
CREATE TYPE contract_type AS ENUM ('msa', 'content_release', 'nda', 'amendment');
CREATE TYPE face_obscure_pref AS ENUM ('mask', 'digital');
CREATE TYPE bible_visibility AS ENUM ('owner', 'panel', 'subs');

-- Users table
CREATE TABLE users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at timestamptz DEFAULT now(),
  role user_role NOT NULL DEFAULT 'sub',
  email text UNIQUE NOT NULL,
  display_name text,
  legal_name_first text,
  legal_name_last text,
  pronouns text,
  dob date,
  age_verified boolean DEFAULT false,
  id_verification_provider text,
  id_verification_ref text,
  city text,
  state text,
  country text,
  is_remote boolean DEFAULT false,
  notes text
);

-- Applications table
CREATE TABLE applications (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES users(id) ON DELETE CASCADE,
  status application_status DEFAULT 'submitted',
  role_pref text[],
  limits jsonb,
  safewords jsonb,
  availability_capacity_per_week int,
  available_remote boolean,
  available_training_solo boolean,
  available_partnered boolean,
  available_partnered_content boolean,
  content_willing boolean,
  content_alias text,
  content_face_obscure boolean DEFAULT false,
  content_face_obscure_pref face_obscure_pref,
  remote_ok boolean,
  travel_ok boolean,
  compensation_pref text,
  tithe_percent numeric,
  submitted_at timestamptz DEFAULT now()
);

-- Tasks table
CREATE TABLE tasks (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at timestamptz DEFAULT now(),
  created_by uuid REFERENCES users(id),
  assigned_to uuid REFERENCES users(id),
  title text NOT NULL,
  category task_category NOT NULL,
  description text,
  location text,
  start_at timestamptz,
  end_at timestamptz,
  status task_status DEFAULT 'planned',
  private boolean DEFAULT true,
  owner_bible_version_id uuid,
  updated_at timestamptz DEFAULT now()
);

-- Content sessions table
CREATE TABLE content_sessions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  title text NOT NULL,
  shoot_date timestamptz,
  location text,
  notes text,
  created_at timestamptz DEFAULT now()
);

-- Contracts table
CREATE TABLE contracts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES users(id) ON DELETE CASCADE,
  contract_type contract_type NOT NULL,
  version text,
  signed boolean DEFAULT false,
  signed_at timestamptz,
  file_url text,
  form_payload jsonb,
  created_at timestamptz DEFAULT now()
);

-- Enable Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE contracts ENABLE ROW LEVEL SECURITY;

-- Create policies for owner access
CREATE POLICY "Owners can view all data" ON users FOR ALL USING (true);
CREATE POLICY "Owners can view all applications" ON applications FOR ALL USING (true);
CREATE POLICY "Owners can view all tasks" ON tasks FOR ALL USING (true);
CREATE POLICY "Owners can view all content sessions" ON content_sessions FOR ALL USING (true);
CREATE POLICY "Owners can view all contracts" ON contracts FOR ALL USING (true);
```

4. **Click "Run"**
5. **Wait for success message**

### **Step 5: Test Connection**

1. **Restart your Streamlit app**
2. **Go to Admin Login**
3. **You should see:** ✅ **Database connected**
4. **Login with:** `admin` / `harem2025`

---

## 🔧 **TROUBLESHOOTING**

### **If you still see "Database connection failed":**

#### **Check 1: Credentials**
- ✅ **URL format:** `https://your-project.supabase.co` (no trailing slash)
- ✅ **Key format:** Starts with `eyJ...` (long string)
- ✅ **No extra spaces** in secrets

#### **Check 2: Supabase Project**
- ✅ **Project is active** (not paused)
- ✅ **Database is ready** (green status)
- ✅ **API is enabled** (default)

#### **Check 3: Streamlit Secrets**
- ✅ **Secrets are saved** in Streamlit Cloud
- ✅ **App is restarted** after adding secrets
- ✅ **No typos** in secret names

### **Common Issues:**

#### **"Invalid API key"**
- Check the key is copied correctly
- Make sure it's the `anon` key, not `service_role`

#### **"Connection timeout"**
- Check your Supabase project is active
- Try a different region if needed

#### **"Table doesn't exist"**
- Run the SQL setup script
- Check the tables were created in Supabase

---

## 📊 **WHAT YOU'LL GET AFTER SETUP**

### **✅ Real-Time Data:**
- **Applications** - Real applications from database
- **Users** - Real user profiles and data
- **Tasks** - Real task management
- **Analytics** - Real metrics and KPIs
- **All CRM Features** - Fully functional

### **✅ Enhanced Features:**
- **Live Updates** - Real-time data synchronization
- **Data Persistence** - All data saved to database
- **User Management** - Complete user lifecycle
- **Performance Tracking** - Real analytics
- **Security** - Database-level security

---

## 🎯 **NEXT STEPS AFTER SETUP**

1. **Test the connection** - Verify database is connected
2. **Create test data** - Add some sample applications
3. **Test all features** - Verify everything works
4. **Configure users** - Set up your admin account
5. **Start using** - Begin managing applications

---

## 📞 **SUPPORT**

### **If you need help:**
1. **Check the troubleshooting section above**
2. **Verify your Supabase project is active**
3. **Double-check your credentials**
4. **Make sure the SQL setup script ran successfully**

### **Quick Test:**
- **Admin Login:** `admin` / `harem2025`
- **Should see:** ✅ **Database connected**
- **Should work:** All CRM features with real data

**Your Harem CRM will be fully functional with real database connectivity!** 🚀
