# Almas Spices Store — Full Project Brief

## Project Overview

Three interconnected digital products for **Almas**, a premium B2B + B2C spices and herbs store in Morocco.

---

## Business Context

- **Store name:** Almas (meaning "diamonds" in Arabic)
- **Type:** Spices and herbs — wholesale (B2B) and retail (B2C)
- **Target B2B:** Restaurants, hotels, catering companies
- **Target B2C:** Individual home buyers
- **Primary market:** Morocco (Casablanca base)
- **Payment:** Cash on Delivery (primary)
- **Delivery:** Self-managed with Waze navigation
- **Languages:** Arabic, French, English

---

## Architecture — 3 Products

```
┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────────────┐
│  ALMAS WEBSITE       │   │  ALMAS RESTAURANT APP │   │  ALMAS ADMIN CRM     │
│  (Next.js)           │   │  (Flutter Android)    │   │  (Django Python)     │
│  Brand + Store       │   │  B2B ordering app     │   │  Web dashboard       │
│  Vercel              │   │  Codex building it    │   │  vercel.app          │
└──────────────────────┘   └──────────────────────┘   └──────────────────────┘
                                      │                          │
                                      └──────────┬───────────────┘
                                                 │
                                        Firebase / SQLite backend
```

---

## Product 1 — Almas Website (Next.js)

**Path:** `C:\Users\Elamr\Music\APPS\Android Apps\almas-website`
**Stack:** Next.js 14, TypeScript, Tailwind CSS
**Deploy:** Vercel

### Pages
- `/` — Homepage: hero, featured products, B2B section, B2C section, testimonials
- `/products` — Full catalog with category filter and search
- `/wholesale` — B2B page for restaurants & hotels (pricing tiers, inquiry form)
- `/about` — Brand story, values, stats
- `/contact` — Contact info, WhatsApp button, order inquiry form

### Design
- Colors: Gold (#C9A84C), Dark Navy (#1A1A2E), Cream (#F9F5EC)
- Fonts: Playfair Display (headings), Inter (body)
- WhatsApp floating button on all pages
- Mobile responsive

---

## Product 2 — Restaurant App (Flutter Android)

**Path:** `C:\Users\Elamr\Music\APPS\Android Apps\Almas`
**Stack:** Flutter (Dart), Firebase backend
**Status:** Being built by Codex

### Features
- Product catalog (browse, search, filter)
- Cart and ordering (Cash on Delivery)
- Order tracking (status updates)
- In-app chat with Almas store
- Restaurant GPS location + Waze navigation
- Push notifications
- Arabic/French language support

---

## Product 3 — Almas CRM (Django Web)

**Path:** `C:\Users\Elamr\Music\APPS\Android Apps\Almas_CRM`
**Stack:** Django 6, Python 3.13, SQLite → PostgreSQL
**Deploy:** Vercel → https://almas-crm.vercel.app
**Login:** almas / Almas2024!

### Features
- Restaurant client profiles (GPS + Waze button)
- Order management (confirm, dispatch, deliver)
- In-app chat per restaurant
- Delivery board with Waze navigation
- Product inventory management
- CRM: VIP/Regular/New/Inactive/Lead tags
- Notes and call logs per restaurant
- Churn alerts (14-day silence detection)
- Low stock alerts
- Reports: top clients, top products, revenue

### Database Note
- Currently using SQLite at `/tmp/db.sqlite3` on Vercel (ephemeral)
- Upgrade path: Neon PostgreSQL (free tier) + `dj-database-url`

---

## Restaurant Location + Waze Integration

- Each restaurant stores GPS coordinates (lat/lng)
- Admin app: "Open in Waze" button per restaurant profile
- Delivery board: "Navigate with Waze" per order card
- Waze deep link: `https://waze.com/ul?ll={lat},{lng}&navigate=yes`
- Fallback: Google Maps if Waze not installed

---

## Chat System

- Real-time in-app chat between store owner and each restaurant
- Two types: General chat + Order-linked chat
- WhatsApp as backup communication channel
- Firebase Firestore for Flutter app
- Django models for CRM web

---

## Payment Flow (Cash on Delivery)

1. Restaurant places order → Cash on Delivery selected
2. Admin confirms in CRM or Admin App
3. Driver delivers → collects cash
4. Driver marks "Paid & Delivered"
5. CRM shows daily cash collection summary

---

## Design System (shared across all products)

| Token | Value |
|---|---|
| Primary Gold | `#C9A84C` |
| Gold Light | `#E8C070` |
| Dark Navy | `#1A1A2E` |
| Darker | `#0D0D1A` |
| Cream | `#F9F5EC` |
| Warm Cream | `#F5EDD8` |
| WhatsApp Green | `#25D366` |

---

## Priority Build Order

### Phase 1 — Complete ✅
- [x] CRM Django web app (built + deployed on Vercel)
- [x] Almas brand website (Next.js — built, pending deploy)
- [x] Flutter restaurant app structure (Codex building)

### Phase 2 — Next
- [ ] Connect Almas website to Vercel
- [ ] Firebase setup for Flutter app
- [ ] Add persistent database (Neon PostgreSQL) to CRM
- [ ] POS integration research

### Phase 3 — Future
- [ ] Multi-language (Arabic RTL, French)
- [ ] Admin mobile app (Flutter)
- [ ] Loyalty/discount system
- [ ] POS integration (auto-reorder)
